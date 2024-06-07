from dash import html, dcc
import dash_bootstrap_components as dbc
import math
import statebar
import lang_strings as la
import style_strings as ss
import datasheet_store as ds

def create_layout():

    wavelength = statebar.state_rings.get('wavelength') * 1e-9  #转换为米
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
    dd_ave = dd_ave * 1e-6 #转换为米平方

    if dd_ave == 0:
        n=0
    else:
        n = (4 * m_n * wavelength * radius_curvature) / dd_ave

    formula_n = dcc.Markdown('$n = \\frac{4R(j-i)\\lambda}{\\bar{d}} =' + f'{n:.2f}' + '$', 
                            mathjax=True,className='mathjax'),
    
    ra = abs(n - refractive_index)
    formula_n_aerr = dcc.Markdown('$\\delta_a = |n-n_真|=' + f'{ra:.2f}' + '$', 
                            mathjax=True,className='mathjax')
    
    rr = ra / refractive_index * 100
    formula_n_rerr = dcc.Markdown('$\\delta_r = \\frac{\\delta_a}{n_真}\\times100\\%=' + f'{rr:.0f}' + '\\%$', 
                            mathjax=True,className='mathjax')

    layout = html.Div(
        dbc.Row([
                html.H1(la.str_title_form_cal_n, style=ss.title_style),
                dbc.Row(formula_n,),
                dbc.Row(formula_n_aerr,),
                dbc.Row(formula_n_rerr,),
            ]),
    )

    return layout