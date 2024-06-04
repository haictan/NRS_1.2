from dash import html
import dash_bootstrap_components as dbc
import newton_rings
import controller_adjust
import device_diagram
import controller_aux

def create_layout():
    layout = html.Div([
        dbc.Row([
                dbc.Col(
                    [
                        newton_rings.create_layout(),
                        controller_aux.create_layout(),
                        
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        device_diagram.create_layout(),
                        controller_adjust.create_layout(),
                    ],
                    width=6,
                ),
        ]),
    ],
    # style={'width': '100%',
    #        'height': 'auto',
    #        #'overflow': 'auto'
    #        }
    )
    return layout

def register_callbacks(app):
    controller_adjust.register_callbacks(app)
    controller_aux.register_callbacks(app)