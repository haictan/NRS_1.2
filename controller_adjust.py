from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
import id_strings as id
import statebar
import lang_strings as la
import newton_rings
import wavelength_to_rgb

def create_layout():

    label_width = 2
    slider_width = 10

    #slider_updatemode = 'mouseup'
    slider_updatemode = 'drag'
    gutters = "g-1"

    title_style = {'textAlign': 'left', 'fontSize': '100%', 'marginTop': '10px'}
    label_style = {'textAlign': 'right', 'fontSize': '82%'}
    row_style = {'marginTop': '10px'}

    wavelength= dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_slider_label_wavelength),
                width = label_width,
                style=label_style
            ),
            dbc.Col(
                dcc.Slider(
                    id=id.str_ctr_slider_wavelength,
                    min=380.0, max=750.0, step=0.1, value=statebar.state_rings.get('wavelength'),
                    marks={380: '380', 750: '750'},
                    tooltip={'always_visible': True,},
                    updatemode = slider_updatemode,
                ),
                width = slider_width,
            ),
        ],
        className=gutters,
        style=row_style,
    )

    radius = dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_slider_label_radius_curvature),
                width = label_width,
                style=label_style,
            ),
            dbc.Col(
                dcc.Slider(
                    id=id.str_ctr_slider_radius_curvature,
                    min=0.5, max=2.5, step=0.01, value=statebar.state_rings.get('radius_curvature'),
                    marks={0.5:'0.5', 2.5:'2.5'},
                    tooltip={'always_visible': True},
                    updatemode = slider_updatemode,
                ),
                width = slider_width,
            ),
        ],
        className=gutters,
        style=row_style,
    )

    refractive = dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_slider_label_refractive_index),
                width = label_width,
                style=label_style,
            ),
            dbc.Col(
                dcc.Slider(
                    id=id.str_ctr_slider_refractive_index,
                    min=1.0, max=2.0, step=0.01, value=statebar.state_rings.get('refractive_index'),
                    marks={1:'1', 2:'2'},
                    tooltip={'always_visible': True},
                    updatemode = slider_updatemode,
                ),
                width = slider_width,
            ),
        ],
        className=gutters,
        style=row_style,
    )

    range = dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_slider_label_interference_range),
                width = label_width,
                style=label_style,
            ),
            dbc.Col(
                dcc.Slider(
                    id=id.str_ctr_slider_interference_range,
                    min=1.0, max=4.0, step=0.1, value=statebar.state_rings.get('interference_range'),
                    marks={1:'1',4:'4'},
                    tooltip={'always_visible': True},
                    updatemode = slider_updatemode,
                ),
                width = slider_width,
            ),
        ],
        className=gutters,
        style=row_style,   
    )

    reflector = dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_slider_label_reflector_angle),
                width = label_width,
                style=label_style,
            ),
            dbc.Col(
                dcc.Slider(
                    id=id.str_ctr_slider_reflector_angle,
                    min=0.0, max=90, step=1, value=statebar.state_rings.get('reflector_angle'),
                    marks={0:'0', 90:'90'},
                    tooltip={'always_visible': True},
                    updatemode = slider_updatemode,
                ),
                width = slider_width,
            ),
        ],
        className=gutters,
        style=row_style,
    )

    eyepiece = dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_slider_label_eyepiece_height),
                width = label_width,
                style=label_style,
            ),
            dbc.Col(
                dcc.Slider(
                    id=id.str_ctr_slider_eyepiece_height,
                    min=0, max=100, step=1, value=statebar.state_rings.get('eyepiece_height'),
                    marks={0:'0', 100:'100'},
                    tooltip={'always_visible': True},
                    updatemode = slider_updatemode,
                ),
                width = slider_width,
            ),
        ],
        className=gutters,
        style=row_style,
    )

    layout = html.Div(
        [
            html.H1(la.str_title_ctr_slider, style=title_style),
            wavelength,
            reflector,
            eyepiece,
            refractive,
            radius,
            range,
        ],
        style={#'textAlign': 'center',
               #'border': '1px solid black',
               'marginTop': '10px',
               #'width': '100%',
                #'height': '30%',
               },
    )
    return layout

def register_callbacks(app):
    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_slider_wavelength, 'value'),
        prevent_initial_call=True
    )
    def update_rings(value):
        statebar.state_rings.update({'wavelength': value,})
        return newton_rings.newton_rings_plot()

    
    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_slider_radius_curvature, 'value'),
        prevent_initial_call=True
    )
    def update_rings(value):
        statebar.state_rings.update({'radius_curvature': value,})
        return newton_rings.newton_rings_plot()
    
    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_slider_refractive_index, 'value'),
        prevent_initial_call=True
    )
    def update_rings(value):
        statebar.state_rings.update({'refractive_index': value,})
        return newton_rings.newton_rings_plot()
    
    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_slider_interference_range, 'value'),
        prevent_initial_call=True
    )
    def update_rings(value):
        statebar.state_rings.update({'interference_range': value,})
        return newton_rings.newton_rings_plot()
    
    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_slider_reflector_angle, 'value'),
        prevent_initial_call=True
    )
    def update_rings(value):
        statebar.state_rings.update({'reflector_angle': value,})
        return newton_rings.newton_rings_plot()
    
    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_slider_eyepiece_height, 'value'),
        prevent_initial_call=True
    )
    def update_rings(value):
        statebar.state_rings.update({'eyepiece_height': value,})
        return newton_rings.newton_rings_plot()

    @app.callback(
            Output(id.str_device_microscope_eyepiece, 'style'),
            Input(id.str_ctr_slider_eyepiece_height, 'value'),
        )
    def refresh_microscope(value):
        microscope_move = (value - 30) * 0.7
        top = 70 - microscope_move
        style={'position': 'absolute','left': '330px','top': f'{top}px','z-index': '2'}
        return style
    
    @app.callback(
            Output(id.str_device_microscope_reflector, 'style'),
            [Input(id.str_ctr_slider_eyepiece_height, 'value'),
             Input(id.str_ctr_slider_reflector_angle, 'value'),]
        )
    def refresh_reflector(height, angle):
        reflector_move = (height - 30) * 0.7
        top = 370 - reflector_move
        style={'position': 'absolute','left': '348px','top': f'{top}px','transform': f'rotate({angle}deg) scale(0.7)','z-index': '4'}
        return style
    
    @app.callback(
            Output(id.str_device_microscope_drum, 'style'),
            Input(id.str_ctr_slider_eyepiece_height, 'value'),
        )
    def refresh_drum(value):
        microscope_move = (value - 30) * 0.7
        rotate_deg = - microscope_move * 20
        style={'position': 'absolute','left': '320px','top': '220px','transform': f'rotate({rotate_deg}deg)','z-index': '3'}
        return style
    
    @app.callback(
            Output(id.str_device_lighter, 'style'),
            Input(id.str_ctr_slider_wavelength, 'value'),
        )
    def refresh_lighter(value):
        rgb = wavelength_to_rgb.wavelength_to_rgb(value)
        style={
            'position': 'absolute',
            'left': '590px',
            'top': '330px',
            'width': '78px',
            'height': '195px',
            'border-radius': '25%',
            'background-image': f'radial-gradient(circle, rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 1), rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0))',
            'z-index': '5'
        }
        return style
   