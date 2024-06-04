import plotly.graph_objects as go
import numpy as np
from dash import html, dcc
import id_strings as id


def micrometer_diagram(reading):
    main_scale_max = 10 # 最大读数10毫米
    #main_scale_gain = 0.5 # 主刻度缩放倍数
    micro_scale_gain = 7 # 刻度距离放大倍数
    ticks_num = 50 # 每圈刻度数量
    turn_length = 0.5 # 每圈移动的长度（mm）

    fig = go.Figure()

    # 绘制主刻度线
    fig.add_trace(go.Scatter(
        x=[0, main_scale_max],
        y=[0, 0],
        mode='lines',
        line=dict(color='black', width=1)
    ))

    # 绘制主刻度刻度
    direction = 1
    for i in np.linspace(0, main_scale_max , 2 * main_scale_max + 1):
        fig.add_shape(type="line",
                      x0=i, y0=0, x1=i, y1=direction * 0.3,
                      line=dict(color="black", width=1))
        if direction > 0:
            fig.add_annotation(x=i, y=direction * 0.4,
                            text=str(int(i)),
                            showarrow=False,
                            yshift=10 * direction)
        direction = -direction

    # 绘制副刻度
    main_position = round(1 / turn_length) * round(reading)
    for i in range(main_position - 2, main_position + 2):
        for count, j in enumerate(np.linspace(i * turn_length * micro_scale_gain,
                                              (i + 1) * turn_length * micro_scale_gain, ticks_num + 1)):
            
            x_position = reading
            y_position = j - reading * micro_scale_gain

            if y_position >  -turn_length * micro_scale_gain / 2 and y_position <  turn_length * micro_scale_gain / 2:

                if count % 10 == 0 and count != 50:
                    scale_length = 0.4
                    line_width = 2
                    text_draw = True
                else:
                    scale_length = 0.2
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

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=15, b=0),
        xaxis_fixedrange=True,  # 禁止缩放和平移
        yaxis_fixedrange=True,
        hovermode=False,
        showlegend=False,
        #width=800,
        height=250,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    return fig


def create_layout():

    layout = html.Div([
            dcc.Graph(
                figure=micrometer_diagram(2.88),
                id=id.str_micrometer_diagram,
                config={
                    'displayModeBar': False,
                },  
            ),
            ],
            style={'height': '500px',}
        )
    return layout

