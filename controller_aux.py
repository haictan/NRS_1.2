from dash import dcc, html, Output, Input
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import lang_strings as la
import id_strings as id
import newton_rings
import statebar

def create_layout():

    label_width = 1
    button_group_width = 11
    slider_updatemode = 'drag'

    row_style = {'display': 'flex','justifyContent': 'space-between','alignItems': 'center','marginTop': '5px'}
    title_style = {'textAlign': 'left', 'fontSize': '100%', 'marginTop': '10px'}
    label_style = {'textAlign': 'right', 'fontSize': '82%'}
    button_group_style = {'display': 'flex','justifyContent': 'space-between','alignItems': 'center',}
    button_size = 'mid'

    resolution_slider = dcc.Slider(
        id=id.str_ctr_aux_slider_resolution,
        min=50, max=300, step=1, value=statebar.state_rings.get('resolution'),
        marks={50:'50', 300:'300'},
        tooltip={'always_visible': False},
        updatemode = slider_updatemode,)
    layout_resolution_slider = dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_aux_slider_resolution),
                width = label_width,
                style=label_style
            ),
            dbc.Col(
                resolution_slider,
                width=button_group_width
            ),
        ], 
        style=row_style   
    )

    aux_func_button_group =  dbc.ButtonGroup([
        dbc.Button(la.str_ctr_aux_button_func_angle, id.str_ctr_aux_button_func_angle, n_clicks=0),
        dbc.Button(la.str_ctr_aux_button_func_height, id.str_ctr_aux_button_func_height, n_clicks=0),
        dbc.Button(la.str_ctr_aux_button_func_destray, id.str_ctr_aux_button_func_destray, n_clicks=0),
        dbc.Button(la.str_ctr_aux_button_func_reste, id.str_ctr_aux_button_func_reste, n_clicks=1,color="warning"),
        ],
        size=button_size,
        style=button_group_style
    )
    layout_func = dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_aux_button_func_group),
                width = label_width,
                style=label_style
            ),
            dbc.Col(
                aux_func_button_group,
                width=button_group_width
            ),
        ],  
        style=row_style   
    )

    ligth_source_button_group = dbc.ButtonGroup([
        dbc.Button(la.str_ctr_aux_button_light_na, id.str_ctr_aux_button_light_na, n_clicks=0),
        dbc.Button(la.str_ctr_aux_button_light_he, id.str_ctr_aux_button_light_he, n_clicks=0),
        dbc.Button(la.str_ctr_aux_button_light_bld, id.str_ctr_aux_button_light_bld, n_clicks=0),
        dbc.Button(la.str_ctr_aux_button_light_ghg, id.str_ctr_aux_button_light_ghg, n_clicks=0),
        ],
        size=button_size,
        style=button_group_style
    )

    layout_light_source = dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_aux_button_light_group),
                width = label_width,
                style=label_style
            ),
            dbc.Col(
                ligth_source_button_group,
                width=button_group_width
            ),
        ],
        style=row_style    
    )

    medium_button_group = dbc.ButtonGroup([
        dbc.Button(la.str_ctr_aux_button_medium_space, id.str_ctr_aux_button_medium_space, n_clicks=0),
        dbc.Button(la.str_ctr_aux_button_medium_water, id.str_ctr_aux_button_medium_water, n_clicks=0),
        dbc.Button(la.str_ctr_aux_button_medium_glass, id.str_ctr_aux_button_medium_glass, n_clicks=0),
        dbc.Button(la.str_ctr_aux_button_medium_sapphire, id.str_ctr_aux_button_medium_sapphire, n_clicks=0),
        ],
        size=button_size,
        style=button_group_style
    )
    layout_medium = dbc.Row(
        [
            dbc.Col(
                html.Label(la.str_ctr_aux_button_medium_group),
                width = label_width,
                style=label_style
            ),
            dbc.Col(
                medium_button_group,
                width=button_group_width,
            ),
        ],
        style=row_style
    )

    layout = html.Div(
        [
            html.H1(la.str_title_ctr_aux, style=title_style),
            layout_resolution_slider,
            layout_func,
            layout_light_source,
            layout_medium,
        ],
        style={
            #'textAlign': 'center',
            #'border': '1px solid black',
            'marginTop': '10px'},
    )
    return layout

def register_callbacks(app):

    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_aux_slider_resolution, 'value'),
        prevent_initial_call=True
    )
    def refresh_rings(value):
        statebar.state_rings.update({'resolution':value})
        return newton_rings.newton_rings_plot()

    @app.callback(
        Output(id.str_ctr_slider_wavelength, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_light_na, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_wavelength_na(n):
        return 589.0
    
    @app.callback(
        Output(id.str_ctr_slider_wavelength, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_light_he, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_wavelength_he(n):
        return 632.8
    
    @app.callback(
        Output(id.str_ctr_slider_wavelength, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_light_bld, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_wavelength_bld(n):
        return 450.0
    
    @app.callback(
        Output(id.str_ctr_slider_wavelength, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_light_ghg, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_wavelength_ghg(n):
        return 546.1
    
    @app.callback(
        Output(id.str_ctr_slider_refractive_index, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_medium_space, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_refractive_index_space(n):
        return 1
    
    @app.callback(
        Output(id.str_ctr_slider_refractive_index, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_medium_water, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_refractive_index_water(n):
        return 1.333
    
    @app.callback(
        Output(id.str_ctr_slider_refractive_index, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_medium_glass, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_refractive_index_glass(n):
        return 1.46
    
    @app.callback(
        Output(id.str_ctr_slider_refractive_index, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_medium_sapphire, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_refractive_sapphire(n):
        return 1.76
    
    @app.callback(
        Output(id.str_ctr_slider_reflector_angle, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_angle, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_refractive_sapphire(n):
        return 45
    
    @app.callback(
        Output(id.str_ctr_slider_eyepiece_height, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_height, 'n_clicks'),
        prevent_initial_call=True
    )
    def set_refractive_sapphire(n):
        return 40
    
    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_destray, 'n_clicks'),
        prevent_initial_call=True
    )
    def update_rings(n):
        if statebar.state_rings.get('rings_destray'):
            statebar.state_rings.update({'rings_destray':False})
        else:
            statebar.state_rings.update({'rings_destray':True})
        return newton_rings.newton_rings_plot()
    
    @app.callback(
        Output(id.str_ctr_slider_wavelength, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_reste, 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset(n):
        return statebar.state_rings_store.get('wavelength')
    
    @app.callback(
        Output(id.str_ctr_slider_radius_curvature, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_reste, 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset(n):
        return statebar.state_rings_store.get('radius_curvature')
    
    @app.callback(
        Output(id.str_ctr_slider_refractive_index, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_reste, 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset(n):
        return statebar.state_rings_store.get('refractive_index')
    
    @app.callback(
        Output(id.str_ctr_slider_interference_range, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_reste, 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset(n):
        return statebar.state_rings_store.get('interference_range')
    
    @app.callback(
        Output(id.str_ctr_slider_reflector_angle, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_reste, 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset(n):
        return statebar.state_rings_store.get('reflector_angle')
    
    @app.callback(
        Output(id.str_ctr_slider_eyepiece_height, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_reste, 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset(n):
        return statebar.state_rings_store.get('eyepiece_height')
    
    @app.callback(
        Output(id.str_ctr_aux_slider_resolution, 'value', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_reste, 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset(n):
        return statebar.state_rings_store.get('resolution')
    
    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_aux_button_func_reste, 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset(n):
        statebar.state_rings.update(statebar.state_rings_store)
        return newton_rings.newton_rings_plot()
