from dash import html, dcc
import dash_bootstrap_components as dbc
import style_strings as ss
import media_source as ms
import principle_string as ps

def create_layout():

    pic_light = html.Div(
        [
            html.Img(src=ms.img_principle_light_path, style=ss.img_style),
            html.H2('图1 牛顿环干涉光路示意图', style=ss.img_title_style)
        ]
    )

    pic_rings = html.Div(
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
        style={
            'border': '2px solid #4477AA',  # 添加蓝色边框
            'text-align': 'justify',    # 文字两端对齐
            'color': '#4477AA',            # 文字变成蓝色
            'padding': '10px',
            'padding-bottom': '0px'
        }
    )

    tip_2 = html.Div(
        dcc.Markdown(ps.principle_tips_2),
        style={
            'border': '2px solid #4477AA',  # 添加蓝色边框
            'text-align': 'justify',    # 文字两端对齐
            'color': '#4477AA',            # 文字变成蓝色
            'padding': '10px',
            'padding-bottom': '0px'
        }
    )

    tip_3 = html.Div(
        dcc.Markdown(ps.principle_tips_3),
        style={
            'border': '2px solid yellow',
            'text-align': 'justify',    
            #'color': 'yellow', 
            'padding': '10px',
            'padding-bottom': '0px'
        }
    )

    intro = html.Div(
        dcc.Markdown(ps.principle_intro),
        style={
            'fontSize': '20px',
        }
    )

    cal = html.Div(
        dcc.Markdown(ps.principle_cal,mathjax=True),
        style={
            'border': '2px',
            'text-align': 'justify',    
            #'color': 'yellow', 
            'padding': '10px',
            'padding-bottom': '0px'
        }
    )

    empty=html.Div(
        [],
        style={
            'height':'100px'
        }
    )

    layout = html.Div(
        [
            dbc.Row(intro, style={'marginTop':'15px'}),
            dbc.Row([
                dbc.Col([pic_light,], width=5),
                dbc.Col([tips_1], width=3),
                dbc.Col([pic_geomatric,], width=4)
                    ],),
            dbc.Row([
                dbc.Col([empty,pic_rings,tip_3], width=5),
                dbc.Col([tip_2,cal], width=7),
            ]),
            html.Hr(style=ss.principle_line_style),
            # html.H2('牛顿环干涉测量透镜曲率半径'),
            # dbc.Row([
            #     dbc.Col(dcc.Markdown(ps.principle_geo,mathjax=True),),
            #     dbc.Col([pic_geomatric, ],),
            # ]),
            # html.Hr(),
            # dbc.Row([
            #     dbc.Col(dcc.Markdown(ps.principle_opd,mathjax=True),),
            #     dbc.Col(dcc.Markdown(ps.principle_interference_conditions,mathjax=True),)
            # ]),
            # html.Hr(),
            # dbc.Row(dcc.Markdown(ps.principle_method,mathjax=True))

        ]
    )
    

    return layout