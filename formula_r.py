from dash import html, dcc
import dash_bootstrap_components as dbc
import math
import statebar
import lang_strings as la
import style_strings as ss
import datasheet_store as ds

def create_layout():

    wavelength = statebar.state_rings.get('wavelength')
    radius_curvature = statebar.state_rings.get('radius_curvature')
    refractive_index = statebar.state_rings.get('refractive_index')

    ring_num  = ds.data_temp.get(ds.str_rings_num)
    ring_num_len_half = round(len(ring_num) / 2)
    m_n = int(ring_num[ring_num_len_half]) - int(ring_num[0])

    diameter_dd = []
    for i,row in enumerate(ds.data):
        if i < round(len(ds.data_temp.get(ds.str_rings_diameter_dd)) / 2):
            diameter_dd.append(row[ds.str_rings_diameter_dd])
    
    dd_len = len(diameter_dd)
    dd_ave = sum(diameter_dd) / dd_len

    R = refractive_index * dd_ave / (4 * m_n * wavelength)

    formula_r = dcc.Markdown('$R = \\frac{n\\bar{d}}{4(j-i)\\lambda}=' + f'{R:.2f}' + 'm$', 
                            mathjax=True,className='mathjax'),
    
    ra = abs(R - radius_curvature)
    formula_r_aerr = dcc.Markdown('$\\delta_a = |R-R_真|=' + f'{ra:.2f}' + 'm$', 
                            mathjax=True,className='mathjax')
    
    rr = ra / radius_curvature * 100
    formula_r_rerr = dcc.Markdown('$\\delta_r = \\frac{\\delta_a}{R_真}\\times100\\%=' + f'{rr:.0f}' + '\\%$', 
                            mathjax=True,className='mathjax')

    layout = html.Div(
        dbc.Row([
                html.H1(la.str_title_form_cal_r, style=ss.title_style),
                dbc.Row(formula_r,),
                dbc.Row(formula_r_aerr,),
                dbc.Row(formula_r_rerr,),
            ]),
    )

    return layout