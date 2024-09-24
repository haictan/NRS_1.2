from dash import html, dcc
import dash_bootstrap_components as dbc
import math
import lang_strings as la
import style_strings as ss
import datasheet_store as ds

def create_layout():

    diameter_dd = []
    for i,row in enumerate(ds.data):
        if i < round(len(ds.data_temp.get(ds.str_rings_diameter_dd)) / 2):
            diameter_dd.append(row[ds.str_rings_diameter_dd])

    ring_num  = ds.data_temp.get(ds.str_rings_num)
    ring_num_len_half = round(len(ring_num) / 2)
    dd_formula = []
    for i,dd in enumerate(diameter_dd):
        d = 'd_{' + f'{i+1}' + '}'
        Dj = 'D_{' + ring_num[i + ring_num_len_half] + '}^2'
        Di = 'D_{' + ring_num[i] + '}^2'
        dd = f'{diameter_dd[i]:.3f}'
        dd_formula.append(dcc.Markdown('$'+ d + '=' + Dj + '-' + Di + '=' + dd + '$', 
                                mathjax=True,className='mathjax'),)
    
    dd_len = len(diameter_dd)
    dd_ave = sum(diameter_dd) / dd_len
    dd_ave_str = f'{dd_ave:.3f}'
    dd_ave_formual = dcc.Markdown('$$\\bar{d}=' + dd_ave_str + '$$',
                        mathjax=True,className='mathjax'),

    delta_d2 = [(x - dd_ave)**2 for x in diameter_dd]
    Ua = math.sqrt(sum(delta_d2)/(dd_len*(dd_len-1)))
    Ua_str = f'{Ua:.3f}'
    
    Ua_formula = dcc.Markdown('$$U_a=\\sqrt{\\frac{\\sum_{i=1}^{n}(d_i-\\bar{d})^2}{n(n-1)}}=' + Ua_str + '$$',
                    mathjax=True,className='mathjax'),

    lad = html.Div(
        [
            html.H1(la.str_title_form_dd, style=ss.title_style),
            dbc.Row([
                dbc.Col(dd_formula),
                dbc.Col([
                    dbc.Row(dd_ave_formual),
                    dbc.Row(Ua_formula)
                ]),
            ])
        ]
    )

    layout = html.Div(
    [
        lad,
    ],

    )

    return layout