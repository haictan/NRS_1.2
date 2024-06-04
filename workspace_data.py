from dash import html
import dash_bootstrap_components as dbc
import datasheet_result
import datasheet_system
import formula_base
import formula_dd
import formula_r
import formula_n

def create_layout():
    layout = html.Div(
        dbc.Row(
            [
                dbc.Col(
                [
                    datasheet_system.create_layout(),
                    datasheet_result.create_layout(),
                    formula_base.create_layout(),
                ],
                width=6,
                ),
                dbc.Col(
                [
                   formula_dd.create_layout(),
                   formula_r.create_layout(),
                   formula_n.create_layout(),
                ],
                width=6,
                ),
            ] 
        )
    )
    return layout

def register_callback(app):
    datasheet_result.register_callback(app)