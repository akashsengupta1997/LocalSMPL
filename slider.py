import argparse
import numpy as np
import os
import torch

import sys
if sys.platform == 'darwin':
    import matplotlib
    matplotlib.use('MACOSX')
import matplotlib.pyplot as plt

from loguru import logger
from matplotlib.widgets import Slider
from smplx import SMPLLayer

from configs import paths
from utils.vis_utils import (
    Renderer, initialise_meas_lines, update_meas_lines
)
from configs.measurements import ALL_MEAS_NAMES_NO_SYMM


def update_scatter(new_vertices, new_joints):
    scatter_front.set_offsets(np.c_[new_vertices[:, 0], new_vertices[:, 1]])
    scatter_side.set_offsets(np.c_[new_vertices[:, 2], new_vertices[:, 1]])
    update_meas_lines(meas_plots, new_vertices, new_joints)
    fig.canvas.draw_idle()

def update_render(new_vertices):
    new_imgs = renderer.render(vertices=new_vertices)
    img_front.set_data(new_imgs['front'])
    img_side.set_data(new_imgs['side'])
    fig.canvas.draw_idle()

def update_slider(val, meas_idx, slider):
    meas_deltas[0, meas_idx] = slider.val

    # -------- LOCAL SEMANTIC SMPL SHAPE --------
    new_betas = orig_betas + torch.matmul(meas_deltas, meas2betas_model)
    smpl_out = smpl_model(betas=new_betas)
    new_vertices = smpl_out.vertices[0].numpy()
    new_joints = smpl_out.joints[0].numpy()

    if args.no_render:
        update_scatter(new_vertices, new_joints)
    else:
        update_render(new_vertices)

def create_slider(slider_pos, slider_label):
    ax_slider = fig.add_axes(slider_pos, facecolor='lightgoldenrodyellow')

    # Define the slider
    slider = Slider(
        ax=ax_slider,
        label=slider_label,
        valmin=-0.04,  # Min value in meters
        valmax=0.04,   # Max value in meters
        valinit=0.0,   # Initial value in meters
        valfmt="%.1f cm"  # Display in centimeters
    )

    # Adjust slider display to show values in centimeters
    def update_valtext(val):
        slider.valtext.set_text(f"{val * 100:.1f} cm")  # Convert to centimeters

    # Connect the update function to the slider
    slider.on_changed(update_valtext)

    return slider


def create_widget(measurements):
    slider_height = 0.03
    sliders = []
    for i, meas in enumerate(measurements):
        assert meas in ALL_MEAS_NAMES_NO_SYMM, f'{meas} is not a valid measurement.'

        slider_pos = (
            0.3, 0.25 - i * (slider_height + 0.01), 0.4, slider_height
        )
        slider = create_slider(slider_pos, meas)

        meas_idx = ALL_MEAS_NAMES_NO_SYMM.index(meas)
        slider.on_changed(
            lambda val, slider=slider, meas_idx=meas_idx:
            update_slider(val, meas_idx, slider)
        )
        sliders.append(slider)

    return sliders


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--gender',
        '-G',
        type=str,
        default='neutral',
        choices=('neutral', 'male', 'female')
    )
    parser.add_argument(
        '--measurements',
        '-M',
        type=str,
        nargs='+',
        required=True,
        help='Measurements to visualise on slider.'
    )
    parser.add_argument(
        '--no_render',
        action='store_true',
        help='Display scatter plot instead of render.'
    )
    parser.add_argument(
        '--base_shape',
        type=int,
        default=0,
        choices=(0, 1, 2),
        help='Choose out of a few pre-defined base SMPL body shapes.',
    )
    parser.add_argument(
        '-resolution',
        '-R',
        type=int,
        default=300,
        help='Resolution of renders - use lower values for better performance.'
    )
    args = parser.parse_args()

    logger.info(f'Using {matplotlib.get_backend()} backend for matplotlib.')

    meas2betas_model = np.load(os.path.join(paths.LOCAL_SMPL, f'meas2betas_{args.gender}.npy'))
    meas2betas_model = torch.from_numpy(meas2betas_model).float()
    logger.info(
        f'Loaded {args.gender} measurements-to-betas regressor with shape: {meas2betas_model.shape}.'
    )
    smpl_model = SMPLLayer(
        paths.SMPL,
        num_betas=meas2betas_model.shape[1],
        gender=args.gender
    )
    logger.info(
        f'Loaded {args.gender} SMPL model with {smpl_model.num_betas} shape betas.'
    )

    logger.info(f'Using pre-defined base shape {args.base_shape}.')
    orig_betas = torch.zeros(1, meas2betas_model.shape[1])
    if args.base_shape == 1:
        orig_betas[:, 1] = -4.
    elif args.base_shape == 2:
        orig_betas[:, 0] = -0.2
        orig_betas[:, 1] = 2.
        orig_betas[:, 3] = -2.

    meas_deltas = torch.zeros(1, meas2betas_model.shape[0])

    renderer = Renderer(faces=smpl_model.faces, image_size=args.resolution)
    fig, (ax_front, ax_side) = plt.subplots(1, 2, figsize=(10, 6))

    # Initial render
    smpl_out = smpl_model(betas=orig_betas)
    vertices = smpl_out.vertices[0].numpy()
    joints = smpl_out.joints[0].numpy()
    if args.no_render:
        scatter_front = ax_front.scatter(vertices[:, 0], vertices[:, 1], s=0.1)
        scatter_side = ax_side.scatter(vertices[:, 2], vertices[:, 1], s=0.1)
        meas_plots = initialise_meas_lines(ax_front, ax_side, vertices, joints)
        ax_front.set_aspect('equal', adjustable='box')
        ax_side.set_aspect('equal', adjustable='box')
    else:
        imgs = renderer.render(vertices=vertices)
        img_front = ax_front.imshow(imgs['front'])
        img_side = ax_side.imshow(imgs['side'])

    ax_front.axis('off')
    ax_front.set_title('Front View')
    ax_side.axis('off')
    ax_side.set_title('Side View')
    plt.subplots_adjust(bottom=0.35)

    # Run slider widget
    sliders = create_widget(args.measurements)

    plt.show()
