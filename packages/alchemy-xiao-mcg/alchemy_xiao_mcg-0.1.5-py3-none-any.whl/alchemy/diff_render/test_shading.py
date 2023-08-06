import os
import cv2
import torch
import numpy as np
from scipy.io import loadmat

import sys
root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(root_folder, 'avatar'))

from Face import BFMDecoder

from pytorch3d.structures import Meshes
from pytorch3d.renderer import (
    OpenGLPerspectiveCameras,
    look_at_view_transform,
    RasterizationSettings,
    MeshRenderer,
    MeshRasterizer,
    TexturesVertex
)

from sh_shading import SoftPerVertexSHShader


def setup_renderer(device='cuda'):
    camera_R, camera_T = look_at_view_transform(eye=((0, 0, 10.),), at=((0, 0, 0.),), up=((0, 1, 0),))
    camera = OpenGLPerspectiveCameras(device=device, R=camera_R, T=camera_T, znear=0.01, zfar=50., fov=12.5936, degrees=True)

    # Rasterization Settings
    raster_settings = RasterizationSettings(
        image_size=224,
        blur_radius=0.0,
        faces_per_pixel=1,
        perspective_correct=True,
        bin_size=None,
        max_faces_per_bin=None
    )

    renderer = MeshRenderer(
        rasterizer=MeshRasterizer(
            cameras=camera,
            raster_settings=raster_settings
        ),
        shader=SoftPerVertexSHShader(
            device=device,
            cameras=camera,
        )
    )

    return renderer


coeff = torch.tensor(loadmat('./test_assets/frame0.mat')['coeff'], dtype=torch.float32, device='cuda')
print(coeff.shape)
light = torch.reshape(coeff[:, 227:254], (1, 3, 9))
light = torch.transpose(light, 1, 2)
rot = coeff[:, 224:227]
rot = rot[:, [2, 1, 0]]
print(rot)


face_decoder = BFMDecoder().cuda()
decoder_out = face_decoder.forward(coeff[:, :80], coeff[:, 80:144], coeff[:, 144:224], rot, coeff[:, 254:257])

renderer = setup_renderer()
textures = TexturesVertex(verts_features=decoder_out['vertice_color'])
mesh = Meshes(verts=decoder_out['vertice'], faces=decoder_out['faces'].expand(1, -1, 3), textures=textures)
mesh_images = renderer(mesh, lights=light)[..., 0:3]
mesh_images = mesh_images.detach().squeeze().cpu().numpy()
cv2.imwrite('result.png', mesh_images[..., ::-1])
