from dash import html, dcc
import dash_bootstrap_components as dbc
import lang_strings as la
import style_strings as ss   

def create_layout():
    lad = html.Div(
        dbc.Row([
            dbc.Col(
                [
                    html.H1(la.str_title_form_base_r, style=ss.title_style),
                    dbc.Row([
                        dcc.Markdown('''
                                     $$
                                     R = \\frac{n(D_j^2-D_i^2)}{4(j-i)\\lambda}
                                     $$
                                     ''', 
                                    mathjax=True,className='mathjax'),
                    ],style = {'textAlign': 'center'}),
                ]
            ),
            dbc.Col(
                [
                    html.H1(la.str_title_form_base_n, style=ss.title_style),
                    dbc.Row([
                        dcc.Markdown('''
                                     $$
                                     n = \\frac{4R(j-i)\\lambda}{D_j^2-D_i^2}
                                     $$
                                     ''',
                                     mathjax=True,className='mathjax'),
                    ],style = {'textAlign': 'center'}),
                ]
            )
        ])
    )

    layout = html.Div(
    [
        lad,
    ],
    style={#'textAlign': 'center',
            #'border': '1px solid black',
            'marginTop': '10px',
            #'width': '100%',
            #'height': '30%',
            },
    )

    return layout