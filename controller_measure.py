from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
import id_strings as id
import lang_strings as la
import statebar
import micrometer
import newton_rings

meter_value_display = False

def create_layout():

    label_width = 1
    slider_width = 8

    gutters = "g-0"

    title_style = {'textAlign': 'left', 'fontSize': '100%', 'marginTop': '10px'}
    label_style = {'textAlign': 'center', 'fontSize': '82%'}
    button_style_ad = {'marginLeft': '2px', 'fontSize': '82%', 'width': '35%'}
    button_style_func = {'marginLeft': '2px', 'fontSize': '82%', 'width': '45%',}
    row_style = {'marginTop': '10px'}
    fix_style={
        #'display': 'flex', 
        #'justifyContent': 'space-between', 
        #'alignItems': 'center',
        #'padding': '0 15px'
        }

    coarse = dbc.Row(
                [
                    dbc.Col(
                        [ html.Label(la.str_ctr_measure_label_coarse),],
                        width = label_width,
                        style=label_style
                    ),
                    dbc.Col(
                        dcc.Slider(
                            id=id.str_ctr_slider_micrometer_value,
                            min=0.0, max=10.0, step=0.001, value=statebar.state_rings.get('micrometer_value'),
                            marks={0:'0', 10:'10'},
                            tooltip=None,
                            updatemode='mouseup',
                    ),
                    width=slider_width,
                    ),
                    dbc.Col(
                            [
                                html.Div([
                                    
                                    dbc.Button(la.str_ctr_measure_button_value_display,
                                                id=id.str_ctr_measure_button_value_display,
                                                n_clicks=0, style=button_style_func,color="success"),
                                    dbc.Button(la.str_ctr_measure_button_reset,
                                                id=id.str_ctr_measure_button_reset,
                                                n_clicks=0, style=button_style_func, color="warning"),
                                ])
                            ],
                    ),
                ],
                className=gutters,
                style=row_style,
            )
    
    fine = dbc.Row(
            [
                dbc.Col(
                    [ html.Label(la.str_ctr_measure_label_fine),],
                    width = label_width,
                    style=label_style
                ),
                dbc.Col(
                    [
                        html.Div([
                            html.Span('0.1:', style=label_style),
                            dbc.Button("-", id=id.str_ctr_measure_button_0_de, n_clicks=0, style=button_style_ad,color="success"),
                            dbc.Button("+", id=id.str_ctr_measure_button_0_add, n_clicks=0, style=button_style_ad,color="success"),
                        ])
                    ],
                    style={'marginLeft': '15px'}

                ),
                dbc.Col(
                    [
                        html.Div([
                                html.Span('0.01:', style=label_style),
                                dbc.Button("-", id=id.str_ctr_measure_button_00_de, n_clicks=0, style=button_style_ad,color="success"),
                                dbc.Button("+", id=id.str_ctr_measure_button_00_add, n_clicks=0, style=button_style_ad,color="success"),
                            ])
                    ]
                ),
                dbc.Col(
                    [
                        html.Div([
                            html.Span('0.001:', style=label_style),
                            dbc.Button("-", id=id.str_ctr_measure_button_000_de, n_clicks=0, style=button_style_ad,color="success"),
                            dbc.Button("+", id=id.str_ctr_measure_button_000_add, n_clicks=0, style=button_style_ad,color="success"),
                        ])
                    ]
                ),    
            ],
            className=gutters,
            style=row_style,
        )
    
    layout = html.Div(
        [
            html.H1("读数鼓轮调节", style=title_style),
            coarse,
            fine,
        ],
        style={'marginBottom': '20px'}
    )
    return layout

def register_callbacks(app):

    @app.callback(
        Output(id.str_micrometer_diagram, 'figure', allow_duplicate=True),
        Input(id.str_ctr_slider_micrometer_value, 'value'),
        prevent_initial_call=True
    )
    def refresh_diagram(value):
        return micrometer.micrometer_diagram(value)
    
    @app.callback(
        Output(id.str_rings, 'figure', allow_duplicate=True),
        Input(id.str_ctr_slider_micrometer_value, 'value'),
        prevent_initial_call=True
    )
    def refresh_rings(value):
        statebar.state_rings.update({'micrometer_value': value})
        return newton_rings.newton_rings_measure()
    
    @app.callback(
        Output(id.str_rings_mid_line, 'figure',),
        Input(id.str_ctr_slider_micrometer_value, 'value'),
        prevent_initial_call=True
    )
    def refresh_mid_line(value):
        statebar.state_rings.update({'micrometer_value': value})
        return newton_rings.newton_rings_measure_mid_line()
    
    @app.callback(
        Output(id.str_ctr_slider_micrometer_value, 'value', allow_duplicate=True),
        Input(id.str_ctr_measure_button_0_add, 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_micrometer(n):
        meter = statebar.state_rings.get('micrometer_value')
        if meter <= 9.9:
            meter = meter + 0.1
            statebar.state_rings.update({'micrometer_value': meter})
        return meter
    
    @app.callback(
        Output(id.str_ctr_slider_micrometer_value, 'value', allow_duplicate=True),
        Input(id.str_ctr_measure_button_0_de, 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_micrometer(n):
        meter = statebar.state_rings.get('micrometer_value')
        if meter >= 0.1:
            meter = meter - 0.1
            statebar.state_rings.update({'micrometer_value': meter})
        return meter
    
    @app.callback(
        Output(id.str_ctr_slider_micrometer_value, 'value', allow_duplicate=True),
        Input(id.str_ctr_measure_button_00_add, 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_micrometer(n):
        meter = statebar.state_rings.get('micrometer_value')
        if meter <= 9.99:
            meter = meter + 0.01
            statebar.state_rings.update({'micrometer_value': meter})
        return meter
    
    @app.callback(
        Output(id.str_ctr_slider_micrometer_value, 'value', allow_duplicate=True),
        Input(id.str_ctr_measure_button_00_de, 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_micrometer(n):
        meter = statebar.state_rings.get('micrometer_value')
        if meter >= 0.01:
            meter = meter - 0.01
            statebar.state_rings.update({'micrometer_value': meter})
        return meter
    
    @app.callback(
        Output(id.str_ctr_slider_micrometer_value, 'value', allow_duplicate=True),
        Input(id.str_ctr_measure_button_000_add, 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_micrometer(n):
        meter = statebar.state_rings.get('micrometer_value')
        if meter <= 9.999:
            meter = meter + 0.001
            statebar.state_rings.update({'micrometer_value': meter})
        return meter
    
    @app.callback(
        Output(id.str_ctr_slider_micrometer_value, 'value', allow_duplicate=True),
        Input(id.str_ctr_measure_button_000_de, 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_micrometer(n):
        meter = statebar.state_rings.get('micrometer_value')
        if meter >= 0.001:
            meter = meter - 0.001
            statebar.state_rings.update({'micrometer_value': meter})
        return meter
    
    @app.callback(
        Output(id.str_ctr_slider_micrometer_value, 'value', allow_duplicate=True),
        Input(id.str_ctr_measure_button_reset, 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_micrometer(n):
        meter = 5
        statebar.state_rings.update({'micrometer_value': meter})
        return meter
    
    @app.callback(
        Output(id.str_ctr_slider_micrometer_value, 'tooltip'),
        Input(id.str_ctr_measure_button_value_display, 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_micrometer(n):
        global meter_value_display
        if meter_value_display:
            tooltip = None
            meter_value_display = False
        else:
            tooltip={'always_visible': True}
            meter_value_display = True
        return tooltip

