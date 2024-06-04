import plotly.graph_objects as go
import numpy as np
from dash import html, dcc
from PIL import Image
from scipy.ndimage import rotate
import wavelength_to_rgb
import id_strings as id

def imread(path):
    img = Image.open(path).convert('RGBA')
    return np.array(img)

img_base = imread('device/base.png')
img_microscope = imread('device/microscope.png')
img_drum = imread('device/micrometer_drum.png')
img_reflector = imread('device/reflector.png')
img_lens = imread('device/lens.png')
img_light = imread('device/light.png')
img_light[:,:,3] = np.clip((1 - img_light[:,:,0]) * 2, 0, 1) #设置光源alpha通道


def show_image(img, fig, x, y, width, height):
    fig.add_trace(go.Image(
        z=img,
        x0=x,
        y0=y,
        dx=1,
        dy=1,
        hoverinfo='skip',
    ))

def microscope_diagram_plot(
        wavelength,
        radius_curvature,
        refractive_index,
        interference_range,
        reflector_angle,
        eyepiece_height,
        ):

    fig = go.Figure()

    show_image(img_base, fig, 0, 0, img_base.shape[1], img_base.shape[0])

    img_light_pos_x = 585
    img_light_pos_y = 310
    img_light_scale = 1
    light_color = wavelength_to_rgb.wavelength_to_rgb(wavelength)
    img_light[:,:,0] = light_color[0]
    img_light[:,:,1] = light_color[1]
    img_light[:,:,2] = light_color[2]
    show_image(
        img_light,
        fig,
        img_light_pos_x,
        img_light_pos_y,
        img_light_pos_x + img_light.shape[1] * img_light_scale * 0.8,
        img_light_pos_y + img_light.shape[0] * img_light_scale * 1.8,
    )

    microscope_move = (eyepiece_height - 30) * 0.7
    img_microscope_pos_x = 330
    img_microscope_pos_y = 70
    img_microscope_scale = 1
    show_image(
        img_microscope,
        fig,
        img_microscope_pos_x,
        img_microscope_pos_y - microscope_move,
        img_microscope_pos_x + img_microscope.shape[1] * img_microscope_scale,
        img_microscope_pos_y + img_microscope.shape[0] * img_microscope_scale - microscope_move,
    )

    img_drum_pos_x = 320
    img_drum_pos_y = 220
    img_drum_scale = 1
    img_drum_rotated = rotate(img_drum, microscope_move * 20, reshape=False)
    img_drum_rotated = np.clip(img_drum_rotated, 0, 1)
    show_image(
        img_drum_rotated,
        fig,
        img_drum_pos_x,
        img_drum_pos_y,
        img_drum_pos_x + img_drum.shape[1] * img_drum_scale,
        img_drum_pos_y + img_drum.shape[0] * img_drum_scale,
    )

    reflector_move = microscope_move
    img_reflector_pos_x = 370
    img_reflector_pos_y = 390
    img_reflector_scale = 0.7
    img_reflector_rotated = rotate(img_reflector, -reflector_angle, reshape=False)
    img_reflector_rotated = np.clip(img_reflector_rotated, 0, 1)
    show_image(
        img_reflector_rotated,
        fig,
        img_reflector_pos_x,
        img_reflector_pos_x + img_reflector.shape[1] * img_reflector_scale,
        img_reflector_pos_y + img_reflector.shape[0] * img_reflector_scale - reflector_move,
        img_reflector_pos_y - reflector_move
    )
    return fig

layout = html.Div([
    dcc.Graph(
        figure=go.Figure(),
        id=id.str_microscope_diagram,
        config={
            'displayModeBar': False,
            'showLink': False,
            'displaylogo': False,
        },
    )
])
