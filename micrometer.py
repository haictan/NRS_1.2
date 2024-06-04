import plotly.graph_objects as go
import numpy as np
import copy
from dash import html, dcc
import id_strings as id
import lang_strings as la
import statebar

base_drawn = False
base_fig = None

main_scale_max = 10 # 最大读数10毫米
micro_scale_gain = 7 # 刻度距离放大倍数
turn_length = 0.5 # 每圈移动的长度（mm）
ticks_num = 50 # 每圈刻度数量

y_lim_buttom_draw = -turn_length * micro_scale_gain / 2 + 1
y_lim_top_draw = turn_length * micro_scale_gain / 2 - 1
x_lim_left_draw = 0
x_lim_right_draw = main_scale_max

y_lim_buttom = y_lim_buttom_draw - 0.1
y_lim_top = y_lim_top_draw + 0.1
x_lim_left = x_lim_left_draw - 0.1
x_lim_right = x_lim_right_draw + 1.1

#绘制包含主刻度和边框的内容，
def base_diagram():

    fig = go.Figure()

    #绘制透明边框，防止画面抖动
    fig.add_shape(
        type="rect",
        x0=x_lim_left, y0=y_lim_buttom, x1=x_lim_right, y1=y_lim_top,
        line=dict(
            color="black",
            width=1,
        ),
        opacity=0,
    )

    fig.add_shape(
        type="rect",
        x0=x_lim_left, y0=y_lim_buttom_draw + 0.1, x1=x_lim_right, y1=y_lim_top_draw - 0.1,
        line=dict(
            color="black",
            width=1,
        ),
        #fillcolor='white'
    )
   
    # 绘制主刻度线
    fig.add_trace(go.Scatter(   
        x=[0, main_scale_max],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=1)
    ))

    # 绘制主刻度刻度
    direction = 1
    tick_line = 0.3
    annotation_pos = tick_line + 0.1
    for i in np.linspace(0, main_scale_max , 2 * main_scale_max + 1):
        fig.add_shape(type="line",
                      x0=i, y0=0, x1=i, y1=direction * tick_line,
                      line=dict(color="black", width=1))
        if direction > 0:
            fig.add_annotation(x=i, y=annotation_pos,
                            text=str(int(i)),
                            showarrow=False,
                            yshift=10)
        direction = -direction

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_fixedrange=True,  # 禁止缩放和平移
        yaxis_fixedrange=True,
        hovermode=False,
        showlegend=False,
        height=200,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    return fig
    

def micrometer_diagram(reading):
    global base_fig
    global base_drawn
    if not base_drawn:  #首次绘制基础图形
        base_fig = base_diagram()
        base_drawn = True

    fig = copy.deepcopy(base_fig)

    #绘制副刻度边框
    fig.add_shape(
        type="rect",
        x0=reading, y0=y_lim_buttom_draw - 0.05, x1=x_lim_right, y1=y_lim_top_draw + 0.05,
        line=dict(
            color="black",
            width=1,
        ),
        fillcolor='white'
    )
    # 绘制副刻度
    main_position = round(1 / turn_length) * round(reading)
    for i in range(main_position - 2, main_position + 2):
        for count, j in enumerate(np.linspace(i * turn_length * micro_scale_gain,
                                              (i + 1) * turn_length * micro_scale_gain, ticks_num + 1)):
            
            x_position = reading
            y_position = j - reading * micro_scale_gain

            if y_position >  y_lim_buttom_draw and y_position <  y_lim_top_draw:

                if count % 10 == 0 and count != 50:
                    scale_length = 0.6
                    line_width = 2
                    text_draw = True
                else:
                    scale_length = 0.3
                    line_width = 1
                    text_draw = False

                fig.add_shape(type="line",
                            x0=x_position, y0=y_position,
                            x1=x_position + scale_length, y1=y_position,
                            line=dict(color="black", width=line_width))

                if text_draw:
                    fig.add_annotation(x=x_position + scale_length + 0.1, y=y_position,
                                    text=str(count),
                                    showarrow=False,
                                    xshift=10)
    return fig


def create_layout():
    title_style = {'textAlign': 'left', 'fontSize': '100%', 'marginTop': '10px'}
    layout = html.Div([
            html.H1(la.str_title_mea_micrometer, style=title_style),
            dcc.Graph(
                figure=micrometer_diagram(statebar.state_rings.get('micrometer_value')),
                id=id.str_micrometer_diagram,
                config={
                    'displayModeBar': False,
                },  
            ),
            ],
            style={'height': '200x',}
        )
    return layout