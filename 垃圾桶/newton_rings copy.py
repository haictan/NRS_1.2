import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from dash import html
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
from scipy.ndimage import gaussian_filter
import lang_strings as la
import id_strings as id
import wavelenth_to_rgb
import statebar

# 格式化坐标轴
def scientific_formatter(x, pos):
    return f'{x*1e3:.2f}'

def newton_rings_plot(
        wavelength,
        radius_curvature,
        refractive_index,
        interference_range,
        reflector_angle,
        eyepiece_height,
        micrometer_value,
        state):

    statebar.busy()

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    ax.xaxis.set_major_formatter(FuncFormatter(scientific_formatter))
    ax.yaxis.set_major_formatter(FuncFormatter(scientific_formatter))
    
    # 单位统一为 米
    wavelength = wavelength * 1e-9
    interference_range = interference_range * 1e-3
    micrometer_value = micrometer_value * 1e-3

    #设定游标初始位置
    micrometer_center = 5 * 1e-3 #初始位置在5毫米处
    micrometer_translate = micrometer_value - micrometer_center
 
    # 创建显示区域
    resolution = 250 # resolution of the interference pattern
    area_left = -interference_range + micrometer_translate
    area_right = interference_range + micrometer_translate
    area_bottom = -interference_range
    area_top = interference_range
    x = np.linspace(area_left, area_right, resolution)
    y = np.linspace(area_bottom, area_top, resolution)
    X, Y = np.meshgrid(x, y)

    # 条纹半径
    r = np.sqrt(X**2 + Y**2)

    # 薄膜厚度
    #d = radius_curvature - np.sqrt(radius_curvature**2 - r**2) #此计算式没有上略d**2高阶项
    d = r**2 / (2 * radius_curvature)
    
    # 计算每个位置的相位差
    #phase = 2 * np.pi / wavelength * (np.sqrt(radius_curvature**2 - r**2) - radius_curvature + r)
    phase = 2 * np.pi * (2 * refractive_index * d + (wavelength / 2)) / wavelength

    # 光强(0-1)
    intensity = 0.5 * (1 + np.cos(phase))
    intensity = gaussian_filter(intensity, sigma = (np.abs(40 - eyepiece_height))) #镜筒高度影响清晰度 镜筒高度30-100 规定40最清晰
    intensity = intensity * np.sin(np.deg2rad(2 * reflector_angle)) #反射镜角度影响光强

    # 根据波长设置颜色
    rgb_color = wavelenth_to_rgb.wavelength_to_rgb(wavelength * 1e9) 
    colormap = [(rgb_color + (0.2,)), (rgb_color + (1,))]  # (R, G, B, alpha)
    wmap = LinearSegmentedColormap.from_list("wave_color", colormap)

    #绘制牛顿环
    ax.set_yticks([])
    if state == la.str_menu_measure:    # 测量状态隐藏刻度
        ax.set_xticks([])
  

    ax.imshow(
        intensity,
        extent=(
            area_left,
            area_right,
            area_bottom,
            area_top,
            ),
        cmap = wmap,
        vmin = 0,
        vmax = 1,
        )

    #测量状态绘制十字叉丝
    if state == la.str_menu_measure:
        # 计算 x轴 和 y轴 的中心点
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        ax.hlines(y_center, xlim[0], xlim[1], color='black', linewidth = resolution/300)
        ax.vlines(x_center, ylim[0], ylim[1], color='black', linewidth = resolution/300)

    plt.axis('on')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    #plt.tight_layout()
    #plt.title(la.str_newton_rings_pattern_title)
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    plt.close()
    img_buf.seek(0)
    img_string = base64.b64encode(img_buf.read()).decode('ascii')

    statebar.unbusy()

    return img_string

#img_string=newton_rings_plot(500,1,1,3,45,40,5,la.str_menu_adjust)

layout = html.Div([
    html.Img(
        #src='data:image/png;base64,{}'.format(img_string),
        src=None,
        style={
            'height': 'auto',
            'width': 'auto',
            'max-width': '100%',
            'max-height': '100%',
        },
        id=id.str_rings
    ),
])