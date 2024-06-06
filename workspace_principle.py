from dash import html, dcc
import dash_bootstrap_components as dbc
import style_strings as ss
import media_source as ms
import principle_string as ps

def create_layout():
    gen = dcc.Markdown(ps.principle_intro),

    pic_light = html.Div(
        [
            html.Img(src=ms.img_principle_light_path, style=ss.img_style),
            html.H2('图1 牛顿环干涉光路示意图', style=ss.img_title_style)
        ]
    )

    pic_rins = html.Div(
        [
            html.Img(src=ms.img_principle_rings_pattern, style=ss.img_style),
            html.H2('图2 牛顿环图样', style=ss.img_title_style),
        ]
    )
    
    
    pic_geomatric = html.Div(
        [
            html.Img(src=ms.img_principle_geomatric, style=ss.img_style),
            html.H2('图3 几何关系示意图', style=ss.img_title_style),
        ]
    )
 
    tips_1 = html.Div(
        dcc.Markdown(ps.principle_tips_1),
        style={}
    )

    layout = html.Div(
        [
            html.H2('干涉现象与牛顿环的形成', style={'marginTop': '15px'}),
            dbc.Row(gen),
            dbc.Row([
                        dbc.Col([pic_light,]),
                        dbc.Col(dcc.Markdown(ps.principle_tips_1), width=2),
                        dbc.Col([pic_geomatric ,])
                    ],),
            html.Hr(style=ss.principle_line_style),
            html.H2('牛顿环干涉测量透镜曲率半径'),
            dbc.Row([
                dbc.Col(dcc.Markdown(ps.principle_geo,mathjax=True),),
                dbc.Col([pic_geomatric, ],),
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col(dcc.Markdown(ps.principle_opd,mathjax=True),),
                dbc.Col(dcc.Markdown(ps.principle_interference_conditions,mathjax=True),)
            ]),
            html.Hr(),
            dbc.Row(dcc.Markdown(ps.principle_method,mathjax=True))

        ]
    )
    

    return layout