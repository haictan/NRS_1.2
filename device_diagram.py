from dash import html
from scipy.ndimage import rotate
import id_strings as id
import statebar
import wavelength_to_rgb
import media_source as ms

def create_layout():
    img_base = html.Img(
    src=ms.img_device_base,
    style={'position': 'absolute','left': '0px','top': '0px', 'z-index': '1'}
    )

    microscope_move = (statebar.state_rings.get('eyepiece_height') - 30) * 0.7
    top = 70 - microscope_move
    style_scope={'position': 'absolute','left': '330px','top': f'{top}px','z-index': '2'}
    img_microscope = html.Img(
    id=id.str_device_microscope_eyepiece,
    src=ms.img_device_microscope,
    style=style_scope,
    )

    rotate_deg = - microscope_move * 20
    style_drum={'position': 'absolute','left': '320px','top': '220px','transform': f'rotate({rotate_deg}deg)','z-index': '3'}
    img_drum = html.Img(
    id=id.str_device_microscope_drum,
    src=ms.img_device_micrometer_drum,
    style=style_drum,
    )

    reflector_move = microscope_move
    top = 370 - reflector_move
    angle = statebar.state_rings.get('reflector_angle')
    style_reflector={'position': 'absolute','left': '348px','top': f'{top}px',
           'transform': f'rotate({angle}deg) scale(0.7)','z-index': '4'}
    img_reflector = html.Img(
    id=id.str_device_microscope_reflector,
    src=ms.img_device_reflector,
    style=style_reflector,
    )
    
    rgb = wavelength_to_rgb.wavelength_to_rgb(statebar.state_rings.get('wavelength'))
    style_lighter={
        'position': 'absolute',
        'left': '590px',
        'top': '330px',
        'width': '78px',
        'height': '195px',
        'border-radius': '25%',
        'background-image': f'radial-gradient(circle, rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 1), rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0))',
        'z-index': '5'
    } 
    lighter = html.Div(
        id=id.str_device_lighter,
        style=style_lighter,
    )

    device = html.Div([
        img_base,
        img_microscope,
        img_drum,
        img_reflector,
        lighter],
        style={
            #'position': 'relative',
            # 'width': '500x',
            # 'height': '300px',
            'transform': 'scale(0.55)',
            'transform-origin': 'top left',
            #'border': '1px solid black',
            #'overflow': 'hidden',
            },
        )
    
    layout = html.Div(
        device,
        style={
            #'position': 'relative',
            #'border': '1px solid black',
            'overflow': 'auto',
            'width': '70%',
            'height': '390px',
            #'alignItems': 'center',
            'margin': '0 auto',
            },

    )

    return layout