from dash import html
import dash_bootstrap_components as dbc
import newton_rings
import micrometer
import controller_measure
import datasheet_measure

def create_layout():
    device = html.Div([
        dbc.Row([
                dbc.Col([
                    newton_rings.create_layout(),
                    newton_rings.create_layout_measure_line()
                    ],
                    width=6,
                ),

                dbc.Col([
                    micrometer.create_layout(),
                    controller_measure.create_layout(),
                    datasheet_measure.create_layout(),
                    ],
                    width=6,
                ),
        ]),
    ],)

    table = html.Div([
        dbc.Row([
                dbc.Col([],width=12,)
        ]),
    ],)

    control = html.Div([
        dbc.Row([
                dbc.Col([],width=6,)
        ]),
    ],)

    layout = html.Div(
        [device,table,control],
        style={}
    )

    return layout

def register_callbacks(app):
    controller_measure.register_callbacks(app)
    datasheet_measure.register_callbacks(app)