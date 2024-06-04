import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.ndimage import rotate
import control_sliders as cs
import state_bar
import wavelenth_to_rgb

img_base = mpimg.imread('device/base.png')
img_row = img_base.shape[0]
img_col = img_base.shape[1]

img_light = mpimg.imread('device/light.png')
img_light_row = img_light.shape[0]
img_light_col = img_light.shape[1]
img_light[:,:,3] = np.clip((1 - img_light[:,:,0]) * 2, 0, 1)

img_microscope = mpimg.imread('device/microscope.png')
img_microscope_row = img_microscope.shape[0]
img_microscope_col = img_microscope.shape[1]

img_drum = mpimg.imread('device/micrometer_drum.png')
img_drum_row = img_drum.shape[0]
img_drum_col = img_drum.shape[1]

img_reflector = mpimg.imread('device/reflector.png')
img_reflector_row = img_reflector.shape[0]
img_reflector_col = img_reflector.shape[1]

img_lens = mpimg.imread('device/lens.png')
img_lens_row = img_lens.shape[0]
img_lens_col = img_lens.shape[1]


def microscope_diagram(reflector_angle, eyepiece_height, wavelength):
    state_bar.busy()

    fig, microscope = plt.subplots(figsize=(5, 5))
    microscope.set_xlim(0,img_col)
    microscope.set_ylim(img_row,0)

    microscope.set_aspect('equal')
    microscope.axis('off')

    microscope.imshow(img_base)

    img_light_pos_x = 585
    img_light_pos_y = 310
    img_light_scale = 1
    light_color = wavelenth_to_rgb.wavelength_to_rgb(wavelength)
    img_light[:,:,0] = light_color[0]
    img_light[:,:,1] = light_color[1]
    img_light[:,:,2] = light_color[2]
    microscope.imshow(img_light,
                  extent=[
                      img_light_pos_x,
                      img_light_pos_x + img_light_col * img_light_scale * 0.8,
                      img_light_pos_y + img_light_row * img_light_scale * 1.8,
                      img_light_pos_y]
                      )

    microscope_move = (eyepiece_height - 30) * 0.7
    img_microscope_pos_x = 330
    img_microscope_pos_y = 70
    img_microscope_scale = 1
    microscope.imshow(img_microscope,
                  extent=[
                      img_microscope_pos_x,
                      img_microscope_pos_x + img_microscope_col * img_microscope_scale,
                      img_microscope_pos_y + img_microscope_row * img_microscope_scale - microscope_move,
                      img_microscope_pos_y - microscope_move]
                      )

    img_drum_pos_x = 320
    img_drum_pos_y = 220
    img_drum_scale = 1
    img_drum_rotated = rotate(img_drum, microscope_move * 20, reshape=False)
    img_drum_rotated = np.clip(img_drum_rotated, 0, 1)
    microscope.imshow(img_drum_rotated,
                  extent=[
                      img_drum_pos_x,
                      img_drum_pos_x + img_drum_col * img_drum_scale,
                      img_drum_pos_y + img_drum_row * img_drum_scale,
                      img_drum_pos_y]
                      )

    reflector_move = microscope_move
    img_reflector_pos_x = 370
    img_reflector_pos_y = 390
    img_reflector_scale = 0.7
    img_reflector_rotated = rotate(img_reflector, -reflector_angle, reshape=False)
    img_reflector_rotated = np.clip(img_reflector_rotated, 0, 1)
    microscope.imshow(img_reflector_rotated,
                  extent=[
                      img_reflector_pos_x,
                      img_reflector_pos_x + img_reflector_col * img_reflector_scale,
                      img_reflector_pos_y + img_reflector_row * img_reflector_scale - reflector_move,
                      img_reflector_pos_y - reflector_move]
                      )

    plt.title('Microscope')
    plt.show()

    state_bar.unbusy()

def lens_diagram(radius, refractive_index):
    state_bar.busy()

    fig, lens = plt.subplots(figsize=(5, 3))
    lens.set_xlim(0,img_lens_col)
    lens.set_ylim(img_lens_row,0)

    lens.set_aspect('equal')
    lens.axis('off')

    lens.imshow(img_lens)

    plt.title('Lens')
    plt.show()

    state_bar.unbusy()

microscope = widgets.interactive_output(
    microscope_diagram, {
    'reflector_angle': cs.reflector_angle_slider,
    'eyepiece_height': cs.eyepiece_height_slider,
    'wavelength':cs.wavelength_slider,
    }
)

lens = widgets.interactive_output(
    lens_diagram, {
    'radius': cs.radius_slider,
    'refractive_index': cs.refractive_index_slider,
    }
)