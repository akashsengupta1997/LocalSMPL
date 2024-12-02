import numpy as np
import pyrender
import trimesh

from configs.measurements import (
    VERTEX_LENGTH_MEAS_INDEXES,
    VERTEX_CIRCUMFERENCE_MEAS_INDEXES,
    JOINT_LENGTH_MEAS_INDEXES,
)


class Renderer:
    def __init__(
            self,
            faces,
            image_size=300,
            background_color=(1.0, 1.0, 1.0),
            camera_translation=np.array([0, -0.2, 2.0]),
    ):
        self.faces = faces
        self.image_size = image_size
        self.background_color = background_color

        self.scene = pyrender.Scene(
            bg_color=background_color, ambient_light=(0.3, 0.3, 0.3)
        )

        self.renderer = pyrender.OffscreenRenderer(self.image_size, self.image_size)

        camera = pyrender.OrthographicCamera(xmag=1.0, ymag=1.0)
        cam_pose = np.eye(4)
        cam_pose[:3, 3] = camera_translation
        self.scene.add(camera, pose=cam_pose)

        light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
        self.scene.add(light, pose=cam_pose)

        self.side_rot_mat = np.array(
            [
                [0., 0., 1.],
                [0., 1., 0.],
                [-1., 0., 0.]
            ]
        )

        self.front_mesh_node = None
        self.side_mesh_node = None

    def update_mesh_nodes(self, vertices):
        side_vertices = np.matmul(vertices, self.side_rot_mat.T)

        if self.front_mesh_node is None:
            assert self.side_mesh_node is None
            mesh = pyrender.Mesh.from_trimesh(
                trimesh.Trimesh(vertices, self.faces, process=False)
            )
            self.front_mesh_node = pyrender.Node(mesh=mesh)

            side_mesh = pyrender.Mesh.from_trimesh(
                trimesh.Trimesh(side_vertices, self.faces, process=False)
            )
            self.side_mesh_node = pyrender.Node(mesh=side_mesh)

        else:
            assert self.side_mesh_node is not None
            self.front_mesh_node.mesh.primitives[0].positions = vertices
            self.side_mesh_node.mesh.primitives[0].positions = side_vertices

    def render(self,  vertices):
        self.update_mesh_nodes(vertices)

        self.scene.add_node(self.front_mesh_node)
        front_img, _ = self.renderer.render(self.scene)
        imgs = {'front': front_img}
        self.scene.remove_node(self.front_mesh_node)

        self.scene.add_node(self.side_mesh_node)
        side_image, _ = self.renderer.render(self.scene)
        imgs["side"] = side_image
        self.scene.remove_node(self.side_mesh_node)

        return imgs


def initialise_meas_lines(ax_front, ax_side, vertices):

    vertex_len_plots = {'front': [], 'side': []}
    for id_pair in VERTEX_LENGTH_MEAS_INDEXES:
        vertex_len_plots['front'].extend(
            ax_front.plot(
                vertices[id_pair, 0],
                vertices[id_pair, 1],
                c='red'
            )
        )
        vertex_len_plots['side'].extend(
            ax_side.plot(
                vertices[id_pair, 2],
                vertices[id_pair, 1],
                c='red'
            )
        )

    vertex_circum_plots = {'front': [], 'side': []}
    for id_pair in VERTEX_CIRCUMFERENCE_MEAS_INDEXES:
        vertex_circum_plots['front'].extend(
            ax_front.plot(
                vertices[id_pair, 0],
                vertices[id_pair, 1],
                c='green'
            )
        )
        vertex_circum_plots['side'].extend(
            ax_side.plot(
                vertices[id_pair, 2],
                vertices[id_pair, 1],
                c='green'
            )
        )

    return {
        'vertex_length': vertex_len_plots,
        'vertex_circum': vertex_circum_plots,
    }


def update_meas_lines(meas_plots_dict, vertices):

    for plot_type, plots in meas_plots_dict.items():
        if plot_type == 'vertex_length':
            idxs = VERTEX_LENGTH_MEAS_INDEXES
        elif plot_type == 'vertex_circum':
            idxs = VERTEX_CIRCUMFERENCE_MEAS_INDEXES
        else:
            raise NotImplementedError

        for i, id_pair in enumerate(idxs):
            plots['front'][i].set_xdata(vertices[id_pair, 0])
            plots['front'][i].set_ydata(vertices[id_pair, 1])
            plots['side'][i].set_xdata(vertices[id_pair, 2])
            plots['side'][i].set_ydata(vertices[id_pair, 1])
