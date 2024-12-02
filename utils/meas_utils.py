import numpy as np
import torch

from configs import measurements


def get_meas_from_verts(vertices, joints):
    """
    Get body measurements (as defined in configs/measurements.py) from 
    batch of SMPL T-pose vertex meshes and SMPL 3D joint locations.
    
    :param vertices: (B, 6890, 3) Tensor containing a batch of SMPL vertex meshes in T-pose.
    :param joints: (B, K, 3) Tensor containing a batch of 3D joint locations in T-pose.
    :return: meas: (B, M) Tensor containing a batch of body measurements.
    """
    joint_len_meas_select = joints[:, measurements.JOINT_LENGTH_MEAS_INDEXES, :]
    joint_len_meas = torch.norm(
        joint_len_meas_select[:, :, 0, :] - joint_len_meas_select[:, :, 1, :],
        dim=-1
    )  # (B, num joint length measurements)

    vertex_len_meas_select = vertices[:, measurements.VERTEX_LENGTH_MEAS_INDEXES, :]
    vertex_len_meas = torch.norm(
        vertex_len_meas_select[:, :, 0, :] - vertex_len_meas_select[:, :, 1, :],
        dim=-1
    )  # (B, num vertex length measurements)

    vertex_circum_meas = []
    for vertex_ids in measurements.VERTEX_CIRCUMFERENCE_MEAS_INDEXES:
        vertex_circum_meas_select = vertices[:, vertex_ids, :]  # (B, num verts for measure, 3)
        rolled = torch.roll(
            vertex_circum_meas_select, shifts=1, dims=1
        )
        meas = torch.sum(
            torch.norm(vertex_circum_meas_select - rolled, dim=-1), dim=-1
        )  # (B,)
        vertex_circum_meas.append(meas)
    vertex_circum_meas = torch.stack(vertex_circum_meas, dim=-1)  # (B, num circum measures)

    meas = torch.cat(
        [joint_len_meas, vertex_len_meas, vertex_circum_meas],
        dim=-1
    )  # (B, num measurements)

    return meas

