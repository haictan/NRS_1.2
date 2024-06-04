import dash
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import statebar
import lang_strings as la
import id_strings as id

button_labels = {
    id.str_menu_welcome: la.str_menu_welcome,
    id.str_menu_principle: la.str_menu_principle,
    id.str_menu_adjust: la.str_menu_adjust,
    id.str_menu_measure: la.str_menu_measure,
    id.str_menu_device: la.str_menu_device,
    id.str_menu_read: la.str_menu_read,
    id.str_menu_game: la.str_menu_game,
    id.str_menu_data: la.str_menu_data
}

def create_layout():
    button_group = html.Div(
        dbc.ButtonGroup([
            dbc.Button(button_labels.get(id.str_menu_principle), id=id.str_menu_principle, n_clicks=0),
            dbc.Button(button_labels.get(id.str_menu_adjust), id=id.str_menu_adjust, n_clicks=0),
            dbc.Button(button_labels.get(id.str_menu_measure), id=id.str_menu_measure, n_clicks=0),
            
            dbc.Button(button_labels.get(id.str_menu_read), id=id.str_menu_read, n_clicks=0, style={"display": "none"}),
            dbc.Button(button_labels.get(id.str_menu_game), id=id.str_menu_game, n_clicks=0, style={"display": "none"}),

            dbc.Button(button_labels.get(id.str_menu_data), id=id.str_menu_data, n_clicks=0),
            dbc.Button(button_labels.get(id.str_menu_device), id=id.str_menu_device, n_clicks=0),
            ],
            id=id.str_menu_buttongroup,
            size="lg",
            style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'marginTop': '5px'},
        ),
        id = id.str_menu_button_group_layout,
    )

    layout = html.Div(button_group)
    return layout

def register_callbacks(app):
    #更新状态栏
    @app.callback(
        Output(id.str_state_mode, 'children', allow_duplicate=True),
        [Input(id.str_menu_principle,  'n_clicks'),
        Input(id.str_menu_adjust,  'n_clicks'),
        Input(id.str_menu_measure,  'n_clicks'),
        Input(id.str_menu_device, 'n_clicks'),
        Input(id.str_menu_read, 'n_clicks'),
        Input(id.str_menu_game, 'n_clicks'),
        Input(id.str_menu_data, 'n_clicks')],
        prevent_initial_call=True
        )
    def update_state_bar(bt1, bt2, bt3, bt4, bt5, bt6, bt7):
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = id.str_menu_welcome
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        button_label = button_labels.get(button_id, "Unknown Option")
        statebar.state_last_mode = button_label
        return button_label
    
    @app.callback(
        Output(id.str_menu_button_group_layout, 'style'),
        Input(id.str_state_floating_button_bar, 'n_clicks'),
        prevent_initial_call=True
    )
    def update_menu_button_group_layout(n):
        if n%2:
            return {"display": "none"}
        else:
            return {}