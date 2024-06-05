from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import media_source as ms
import lang_strings as la
import id_strings as id
import statebar

def create_layout():
    img_cover = html.Img(
    src=ms.img_cover,
    style={'position': 'absolute','left': '0px','top': '0px','width': '1600px', 'height':'1000px', 'z-index': '1'}
    )

    floating_button_enter = dbc.Button(
        la.str_welcome_floating_button_enter,
        id=id.str_welcome_floating_button_enter,
        n_clicks=0,
        style={
            "position": "fixed",
            "bottom": "100px",
            "left": "120px",
            "z-index": "1000",
            "padding": "10px 20px",
            "background-color": "#007bff",
            "color": "white",
            "border": "none",
            "border-radius": "50px",
            "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
            "font-size": "20px",
            "cursor": "pointer"
        }
    )

    floating_button_exit = html.Button(
        la.str_welcome_floating_button_exit,
        id=id.str_welcome_floating_button_exit,
        style={
            "position": "fixed",
            "bottom": "100px",
            "left": "230px",
            "z-index": "1000",
            "padding": "10px 20px",
            "background-color": "#007bff",
            "color": "white",
            "border": "none",
            "border-radius": "50px",
            "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
            "font-size": "20px",
            "cursor": "pointer"
        }
    )

    layout = html.Div(
        [
            img_cover,
            floating_button_enter,
            #floating_button_exit
        ],
        # style={
        #     'alignItems': 'center',
        #     },
    )
    return layout

def register_callbacks(app):
    #更新状态栏
    @app.callback(
        Output(id.str_state_mode, 'children', allow_duplicate=True),
        Input(id.str_welcome_floating_button_enter,  'n_clicks'),
        prevent_initial_call=True
        )
    def enter(n):
        return statebar.state_last_mode