import plotly.graph_objects as go
import numpy as np
from scipy.ndimage import gaussian_filter
import lang_strings as la
import wavelenth_to_rgb

def intensity(
        wavelength,
        radius_curvature,
        refractive_index,
        interference_range,
        reflector_angle,
        eyepiece_height,
        micrometer_value):
    # 单位统一为 米
    wavelength = wavelength * 1e-9
    interference_range = interference_range * 1e-3
    micrometer_value = micrometer_value * 1e-3

    #设定游标初始位置
    micrometer_center = 5 * 1e-3 #初始位置在5毫米处
    micrometer_translate = micrometer_value - micrometer_center
    
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
    
    # 相位差
    phase = 2 * np.pi * (2 * refractive_index * d + (wavelength / 2)) / wavelength

    # 光强(0-1)
    intensity = 0.5 * (1 + np.cos(phase))
    intensity = gaussian_filter(intensity, sigma = (np.abs(40 - eyepiece_height))) #镜筒高度影响清晰度 镜筒高度30-100 规定40最清晰
    intensity = intensity * np.sin(np.deg2rad(2 * reflector_angle)) #反射镜角度影响光强
    return intensity

# 根据波长设置颜色
wavelength = 500 * 1e-9
rgb_color = wavelenth_to_rgb.wavelength_to_rgb(wavelength * 1e9) 
colormap = [(rgb_color + (0.2,)), (rgb_color + (1,))]  # (R, G, B, alpha)

#绘制牛顿环
fig = go.Figure(data=go.Image(z=intensity(500,1,1,2,45,40,5)))
fig.update_layout(
    title=la.str_newton_rings_pattern_title,
    xaxis_nticks=36, yaxis_nticks=36,
    xaxis_showgrid=False, yaxis_showgrid=False,
    xaxis_zeroline=False, yaxis_zeroline=False
)
fig.show()