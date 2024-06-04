import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import widgets
from IPython.display import display

gain = 1 #整体缩放比例
main_scale_max = 10  # 假设最大读数10毫米
micro_scale_gain = 8 #刻度距离放大
ticks_num = 50 #每圈刻度数量
turn_length = 0.5 #每圈移动的长度（mm）

fig, ax = plt.subplots(figsize=(15, 3))
ax.set_xlim(-1 * gain, (main_scale_max/2 + 0.5) * gain)
ax.set_ylim(-1 * gain, 1 * gain)
ax.set_aspect('equal')
ax.axis('off')  # 关闭坐标轴

def main_scale():
    ax.hlines(0, 0, main_scale_max * gain, 'k', linewidth = 1)
    direction = 1
    for i in np.linspace(0, main_scale_max, 2 * main_scale_max + 1): # 0.5mm一个刻度
        ax.plot([i * gain, i * gain], [0 * gain, direction * 0.3 * gain], 'k', linewidth = 1)
        direction = -direction #主刻度上下交替


def sub_scale(reading):
    main_position = round(1 / turn_length) * round(reading) #中心圈序号
    for i in range(main_position - 2, main_position + 2): #重复绘制副刻度实现循环效果 i表示第i圈
        count = 0
        for j in np.linspace(i * turn_length * micro_scale_gain, (i + 1) * turn_length * micro_scale_gain, ticks_num + 1):
            if count % 10 == 0 and count != 50:
                scale_length = 0.4
                line_width = 2
                text_draw = True
            else:
                scale_length = 0.2
                line_width = 1
                text_draw = False
            x_position = reading
            y_position = j  - reading * micro_scale_gain
            lim = ax.get_ylim()
            if y_position > lim[0] and y_position < lim[1]:
                ax.plot(
                    [x_position * gain, (x_position + scale_length) * gain],
                    [y_position * gain, y_position * gain],
                    'k',
                    linewidth = line_width,
                )
                if text_draw: #绘制标签
                    ax.text((x_position + scale_length) * gain + 0.1, y_position * gain - (12 / 2) / 100, str(count), fontsize = 12) 
            count = count + 1


def draw(reading):
    main_scale()
    sub_scale(reading)
    
# 创建滑块用于模拟测微计读数输入
reading_slider = widgets.FloatSlider(
    value=0,
    min=0,
    max=10,
    step=0.001,
    description='读数:',
    readout_format='.3f'
    #continuous_update=False
)
reading_slider.layout.width = '1000px'

micrometer = widgets.interactive_output(
    draw, {
        'reading': reading_slider
    }
)


