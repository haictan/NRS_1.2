from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import datetime
import lang_strings as la
import id_strings as id
import welcome
import workspace_principle
import workspace_adjust
import workspace_measure
import workspace_device
import workspace_read
import workspace_game
import workspace_data

def create_layout():
    title = html.Div(
        html.H1(
            la.str_state_title,
            id=id.str_state_title,
            style={'textAlign': 'center',
                    #'marginTop': '5px',
                    'fontSize': '150%',},
        ),
        id = id.str_state_title_layout,
    )
    #style_mode={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center','fontSize': '90%'},
    mode = dbc.Row(
        [
            dbc.Col(
                html.Div([ 
                    html.Span(la.str_state_time_description),
                    html.Span(la.str_state_time, id=id.str_state_time),
                    dcc.Interval(
                        id=id.str_state_interval,
                        interval=1*1000,  # in milliseconds
                        n_intervals=0),
                ],
                style={'textAlign':'left'}
                )
            ),

            dbc.Col(
                html.Div([
                    html.Span(la.str_state_mode_description),
                    html.Span(la.str_menu_welcome, id=id.str_state_mode)
                ],
                style={'textAlign':'center'}
                ),
            ),

            dbc.Col(
                html.Div([
                    html.Span(la.str_state_logo, id=id.str_state_logo),
                ],
                style={'textAlign':'right'}
                )
            )
        ],
        id = id.str_state_mode_layout
    )

    floating_button_bar = dbc.Button(
        la.str_state_floating_button_bar_off,
        id=id.str_state_floating_button_bar,
        n_clicks=0,
        style={
            "position": "fixed",
            "bottom": "150px",
            "right": "30px",
            "width": "100px",
            "height": "40px",
            "z-index": "1000",
            "padding": "10px 20px",
            "background-color": "#007bff",
            "color": "white",
            "border": "none",
            "border-radius": "50px",
            "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
            "font-size": "12px",
            "cursor": "pointer"
        }
    )

    floating_button_lan = dbc.Button(
        la.str_state_floating_button_lan_zh,
        id=id.str_state_floating_button_lan,
        n_clicks=0,
        style={
            "position": "fixed",
            "bottom": "100px",
            "right": "30px",
            "width": "100px",
            "height": "40px",
            "z-index": "1000",
            "padding": "10px 20px",
            "background-color": "#007bff",
            "color": "white",
            "border": "none",
            "border-radius": "50px",
            "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
            "font-size": "12px",
            "cursor": "pointer"
        }
    )

    floating_menu = html.Div(
        [
            floating_button_bar,
            #floating_button_lan
        ],
        id=id.str_state_floating_menu
    )

    layout = html.Div([
        title,
        mode,
        floating_menu
        ],
        id = id.str_state_layout
    )

    return layout

state_layout_show = True
state_last_mode = la.str_menu_principle

#储存滑块状态
state_rings_store = {
    'wavelength': 550,
    'radius_curvature': 1,
    'refractive_index': 1,
    'interference_range': 1.5,
    'reflector_angle': 30,
    'eyepiece_height': 25,
    'micrometer_value': 5,
    'resolution': 100,
    'resolution_measure': 800,
    'rings_destray': False,
    'state_mode': la.str_menu_adjust
}

state_rings = {
    'wavelength': 550,
    'radius_curvature': 1,
    'refractive_index': 1,
    'interference_range': 1.5,
    'reflector_angle': 30,
    'eyepiece_height': 25,
    'micrometer_value': 5,
    'resolution': 100,
    'resolution_measure': 800,
    'rings_destray': False,
    'state_mode': la.str_menu_measure
}

#储存上一次滑块输出，用于控制刷新频率
state_last_slider = {
    'wavelength': 0,
    'radius_curvature': 0,
    'refractive_index': 0,
    'interference_range': 0,
    'reflector_angle': 0,
    'eyepiece_height': 0,
    'micrometer_value': 0,
    'resolution': 0,
    'rings_destray': False,
}

def register_callbacks(app):
    @app.callback(
        Output(id.str_state_time, 'children'),
        Input(id.str_state_interval, 'n_intervals')
    )
    def update_time(n):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    
    @app.callback(
        Output(id.str_state_title_layout, 'style'),
        Input(id.str_state_floating_button_bar, 'n_clicks'),
        prevent_initial_call=True
    )
    def update_title_layout(n):
        if n%2:
            return {"display": "none"}
        else:
            return {}
        
    @app.callback(
    Output(id.str_state_floating_button_bar, 'children'),
    Input(id.str_state_floating_button_bar, 'n_clicks'),
    prevent_initial_call=True
    )
    def update_title_layout(n):
        if n%2:
            return la.str_state_floating_button_bar_on
        else:
            return la.str_state_floating_button_bar_off
    
    @app.callback(
        Output(id.str_state_mode_layout, 'style'),
        Input(id.str_state_floating_button_bar, 'n_clicks'),
        prevent_initial_call=True
    )
    def update_mode_layout(n):
        if n%2:
            return {"display": "none"}
        else:
            return {}
        
    # @app.callback(
    #     Output(id.str_state_floating_menu, 'style'),
    #     Input(id.str_state_mode, 'children'),
    #     prevent_initial_call=True
    #     )
    # def hidden_floating_menu(mode):
    #     print(f'welcome:{mode}')
    #     if mode == la.str_menu_welcome:
    #         return {"display": "none"}
    #     else:
    #         return {}
    
    @app.callback(
        Output(id.str_workspace, 'children'),
        Input(id.str_state_mode, 'children'),
        #prevent_initial_call=True
        )
    def update_workspace(mode):
        state_rings.update({'state_mode': mode})

        if mode == la.str_menu_principle:
            layout = workspace_principle.create_layout()
        elif mode == la.str_menu_adjust:
            layout = workspace_adjust.create_layout()
        elif mode == la.str_menu_measure:
            layout = workspace_measure.create_layout()
        elif mode == la.str_menu_device:
            layout = workspace_device.create_layout()
        elif mode == la.str_menu_read:
            layout = workspace_read.create_layout()
        elif mode == la.str_menu_game:
            layout = workspace_game.create_layout()
        elif mode == la.str_menu_data:
            layout = workspace_data.create_layout()
        else:
            layout = welcome.create_layout()
        return layout
