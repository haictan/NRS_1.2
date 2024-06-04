import numpy as np
import copy
from dash import html, dcc
import plotly.graph_objects as go
from scipy.ndimage import gaussian_filter
import wavelength_to_rgb
import statebar
import lang_strings as la
import id_strings as id

measure_prepared = False
measure_data = None
ring_plot_height = 500
ring_mid_line_plot_height = 200

def newton_rings_intensity():
    # 获取状态
    state_rings = statebar.state_rings
    wavelength = state_rings.get('wavelength') * 1e-9   #单位统一为 米
    interference_range = state_rings.get('interference_range') * 1e-3
    resolution = state_rings.get('resolution')
    radius_curvature = state_rings.get('radius_curvature')
    refractive_index = state_rings.get('refractive_index')
    eyepiece_height = state_rings.get('eyepiece_height')
    reflector_angle = state_rings.get('reflector_angle')
    destray = state_rings.get('rings_destray')
    mode = state_rings.get('state_mode')
 
    # 创建显示区域
    area_left = -interference_range
    area_right = interference_range
    area_bottom = -interference_range
    area_top = interference_range
    
    # 测量状态下横轴扩大5倍，分辨率提升
    if mode == la.str_menu_measure:
        resolution = statebar.state_rings.get('resolution_measure')
        x_cord = np.linspace(5 * area_left, 5 * area_right, 5 * resolution)
        y_cord = np.linspace(area_bottom, area_top, resolution)
    else:
        x_cord = np.linspace(area_left, area_right, resolution)
        y_cord = np.linspace(area_bottom, area_top, resolution)
    X, Y = np.meshgrid(x_cord, y_cord)

    # 像素位置半径
    r = np.sqrt(X**2 + Y**2)  

    # 介质薄膜厚度
    #d = radius_curvature - np.sqrt(radius_curvature**2 - r**2) #此计算式没有上略d**2高阶项
    d = r**2 / (2 * radius_curvature)

    # 光程差
    delta = 2 * refractive_index * d + (wavelength / 2)
    
    # 相位差
    phase = 2 * np.pi * delta / wavelength

    # 光强(0-1)
    intensity = 0.5 * (1 + np.cos(phase))

    # 显微镜高度偏移影响条纹 规定高度为40最清晰 镜筒高度30-100
    height_shift = np.abs(40 - eyepiece_height) 
    if height_shift < 30:
        intensity = ((30 - height_shift)/30 + 0.01)/1.01 * intensity 
    else:
        intensity = 0.01/1.01 * intensity #高度偏移30后，干涉条纹几乎消失

    # 模拟基础环境光
    if not destray:
        intensity_base = 0.5 
        intensity = intensity + intensity_base
        if np.max(intensity) > 1:
            intensity = intensity / np.max(intensity)
    
    # 反射镜角度影响条纹光强
    intensity = intensity * (np.sin(np.deg2rad(2 * reflector_angle)) + 0.2)/1.2

    # 记录光强范围（高斯模糊会改变数据范围，提前记录用于恢复范围）
    intensity_max = np.max(intensity)
    intensity_min = np.min(intensity)
    if height_shift > 10:
        sigma_index = 10 * resolution / 100
    else:
        sigma_index = height_shift * resolution / 100
    intensity = gaussian_filter(intensity, sigma = (sigma_index)) #镜筒高度影响清晰度 
    intensity = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity)) #高斯模糊后归一化
    intensity = intensity * (intensity_max - intensity_min) + intensity_min #恢复光强范围

    return [x_cord, y_cord, intensity]

#生成图形对象
def create_fig_rings(data):
    x_cord = data[0]
    y_cord = data[1]
    intensity = data[2]

    wavelength = statebar.state_rings.get('wavelength') 
    rgb_color = wavelength_to_rgb.wavelength_to_rgb(wavelength) 
    color_scale = [[0, 'rgba' + str(rgb_color+(0,))], [1, 'rgba' + str(rgb_color + (1,))]]

    #绘制牛顿环
    fig = go.Figure(data=go.Heatmap(
        z = intensity * 100, #光强用百分比表示
        x=x_cord * 1e3,  # 单位转换为毫米
        y=y_cord * 1e3,
        zmin = 0,
        zmax = 100,
        colorscale=color_scale,
        showscale=False,
        hovertemplate=la.str_newton_rings_pattern_hovertemplate
    ))

  # 更新布局设置
    fig.update_layout(
        #title=la.str_newton_rings_pattern_title,
        xaxis=dict(scaleanchor="y", scaleratio=1,showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(scaleanchor="x", scaleratio=1,showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=15, b=0),
        plot_bgcolor='black',
        xaxis_fixedrange=True,  # 禁止缩放和平移
        yaxis_fixedrange=True,
        height=ring_plot_height,
    )
    return fig


# 调整状态下调用
def newton_rings_plot():
    global measure_prepared
    measure_prepared = False

    data = newton_rings_intensity()

    fig = create_fig_rings(data)

    fig.update_layout(hovermode='closest')
    return fig

#测量状态下调用
def newton_rings_measure_prepare():
    global measure_prepared
    global measure_data
    if not measure_prepared:
        measure_data = newton_rings_intensity()
        measure_prepared = True

    data = copy.deepcopy(measure_data)
    x_cord = data[0]
    y_cord = data[1]
    intensity = data[2]

    reading = statebar.state_rings.get('micrometer_value') - statebar.state_rings_store.get('micrometer_value')
    interference_range = statebar.state_rings.get('interference_range')
    resolution = statebar.state_rings.get('resolution_measure')
    pixel_area = 2 * interference_range / resolution #每个像素对应的长度 mm
    trans_pixel = round(reading / pixel_area)

    x_cord_plot = x_cord[2 * resolution + trans_pixel - 1 : 3 * resolution + trans_pixel]   #横向有5个resolution
    y_cord_plot = y_cord
    intensity_plot = intensity[:, 2 * resolution + trans_pixel - 1 : 2 * resolution + resolution + trans_pixel]
    data_plot = [x_cord_plot, y_cord_plot, intensity_plot]
    return data_plot

def newton_rings_measure():
    data_plot = newton_rings_measure_prepare()
    fig = create_fig_rings(data_plot)

    #绘制十字线
    x_cord = data_plot[0]
    y_cord = data_plot[1]
    resolution = statebar.state_rings.get('resolution_measure')

    line_v_x = x_cord[round(resolution/2)]*1e3
    line_v_y = y_cord[resolution-1]*1e3
    line_h_x_l = x_cord[0]*1e3
    line_h_x_r = x_cord[resolution-1]*1e3

    fig.add_shape(type='line',
                x0=line_v_x, y0=-line_v_y, x1=line_v_x, y1=line_v_y,
                line=dict(color="black", width=2))
    fig.add_shape(type='line',
                x0=line_h_x_l, y0=0, x1=line_h_x_r, y1=0,
                line=dict(color="black", width=2))

    fig.update_layout(hovermode=False)
    return fig

def newton_rings_measure_mid_line():
    data_plot = newton_rings_measure_prepare()
    x_cord = data_plot[0]
    intensity_plot = data_plot[2]

    resolution = statebar.state_rings.get('resolution_measure')
    intensity_plot_mid_line = intensity_plot[ round(resolution/2), : ]

    fig = go.Figure()

    wavelength_nm = statebar.state_rings.get('wavelength')
    [r, g, b] = wavelength_to_rgb.wavelength_to_rgb(wavelength_nm) 
    fig = go.Figure(go.Scatter(
        x=x_cord * 1e3,  # 单位转换为毫米
        y=intensity_plot_mid_line,
        mode='lines',
        line=dict(color=f'rgb({r},{g},{b})')
    ))

    line_v_x = x_cord[round(resolution/2)]*1e3
    fig.add_shape(type='line',
                x0=line_v_x, y0=-0.1, x1=line_v_x, y1=1.1,
                line=dict(color='white', width=2))

    # 计算暗纹位置
    wavelength = wavelength_nm * 1e-9
    radius_curvature = statebar.state_rings.get('radius_curvature')
    refractive_index = statebar.state_rings.get('refractive_index')
    r_sequence = np.arange(-100,101,5) #条纹序号
    r_dark = [0.0] * r_sequence.size
    for i,j in enumerate(r_sequence):
        if r_sequence[i] < 0:
            r_dark[i] = - np.sqrt(abs(j) * radius_curvature * wavelength / refractive_index) * 1e3
        else:
            r_dark[i] = np.sqrt(abs(j) * radius_curvature * wavelength / refractive_index) * 1e3

    # 调整横轴比例
    scaleratio_x =  statebar.state_rings_store.get('interference_range') / statebar.state_rings.get('interference_range') * 1.16
    fig.update_layout(
        #title=la.str_newton_rings_pattern_title,
        xaxis=dict(
            scaleanchor="y",
            scaleratio=scaleratio_x,
            #scaleratio=1,
            zeroline=False,
            griddash='dashdot',
            ticks='inside',
            tickvals=r_dark,
            ticktext=r_sequence,
        ),
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            zeroline=False,
            griddash='dashdot',
            ticks='inside',
            ticklabelposition="inside",
            dtick=0.5,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='black',
        xaxis_fixedrange=True,  # 禁止缩放和平移
        yaxis_fixedrange=True,
        hovermode=False,
        height=ring_mid_line_plot_height,
    )
    return fig

def set_rings_fig():
    if statebar.state_rings.get('state_mode') == la.str_menu_adjust:
        fig = newton_rings_plot()
    elif statebar.state_rings.get('state_mode') == la.str_menu_measure:
        fig = newton_rings_measure()
    else:
        fig = go.Figure()
    return fig

def create_layout():
    layout = html.Div([
            dcc.Graph(
                figure=set_rings_fig(),
                id=id.str_rings,
                config={
                    'displayModeBar': False,
                },  
            ),
            ],
            style={'height': f'{ring_plot_height}px',}
        )
    return layout

# 光强曲线
def create_layout_measure_line():
    title_style = {'textAlign': 'left', 'fontSize': '100%', 'marginTop': '10px'}
    layout = html.Div([
            html.H1(la.str_title_mea_mid_line, style=title_style),
            dcc.Graph(
                figure=newton_rings_measure_mid_line(),
                id=id.str_rings_mid_line,
                config={
                    'displayModeBar': False,
                },  
            ),
            ],
            style={'height': f'{ring_mid_line_plot_height}px','width': '100%'}
        )
    return layout