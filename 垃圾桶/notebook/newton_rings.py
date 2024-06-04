import matplotlib.pyplot as plt
import ipywidgets as widgets
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
from scipy.ndimage import gaussian_filter
import lang_strings as la
import control_sliders as cs
import wavelenth_to_rgb
import state_bar

# 科学计数法格式，用于格式化坐标轴
def scientific_formatter(x, pos):
    return f'{x*1e3:.2f}'



def newton_rings(wavelength, radius_curvature, refractive_index, interference_range, reflector_angle, eyepiece_height, micrometer_value, state):
    state_bar.busy()

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

    #print("调用 newton_rings: ", wavelength, radius_curvature, interference_range)
    
    # 创建显示区域
    resolution = 300  # resolution of the interference pattern
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

    if state == la.str_menu_measure:    # 测量状态隐藏刻度
        ax.set_xticks([])
        ax.set_yticks([])

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
    plt.title(la.str_newton_rings_pattern_title)
    plt.show()

    state_bar.unbusy()

# 绘制牛顿环
rings = widgets.interactive_output(
    newton_rings, {
    'wavelength': cs.wavelength_slider, 
    'radius_curvature': cs.radius_slider, 
    'refractive_index': cs.refractive_index_slider,
    'interference_range': cs.interference_range_slider,
    'reflector_angle': cs.reflector_angle_slider,
    'eyepiece_height': cs.eyepiece_height_slider,
    'micrometer_value': cs.micrometer_reading_slider,
    'state': state_bar.mode_text,
    }
)