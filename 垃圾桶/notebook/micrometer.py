import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import widgets
import control_sliders as cs

def draw_micrometer(reading):
    #整体缩放比例
    gain = 1
    #主刻度参数
    main_scale_max = 10  # 假设最大读数10毫米
    main_scale_gain = 0.5  # 主刻度缩放倍数

    #副刻度参数
    micro_scale_gain = 7 #刻度距离放大倍数
    ticks_num = 50 #每圈刻度数量
    turn_length = 0.5 #每圈移动的长度（mm）

    # 图形属性
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.set_xlim(-1 * gain * main_scale_gain, (main_scale_max * main_scale_gain + 1) * gain)
    ax.set_ylim(-1.5 * gain, 1.5 * gain)
    ax.set_aspect(aspect = 'equal')
    #fig.constrained_layout()
    ax.axis('off')
    fontsize_fig = 10

    # 绘制主刻度（毫米）
    ax.hlines(0, 0, main_scale_max * main_scale_gain * gain, 'k', linewidth = 1)
    direction = 1
    for i in np.linspace(0, main_scale_max * main_scale_gain, 2 * main_scale_max + 1): # 0.5mm一个刻度
        ax.plot([i * gain, i * gain], [0, direction * 0.3 * gain], 'k', linewidth = 1)
        x_position_text = (i - fontsize_fig * gain / 200) * gain
        if direction > 0:
            y_position_text = 0.4 * gain
        # else:
        #     y_position_text = (-0.4 - fontsize_fig / 100) * gain
            ax.text(x_position_text, y_position_text, str(int(i / main_scale_gain)), fontsize = fontsize_fig * gain)
        direction = -direction #主刻度上下交替
    
    # 绘制副刻度
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
            x_position = reading * main_scale_gain
            y_position = j  - reading * micro_scale_gain
            lim = ax.get_ylim()
            gap = 0.4 #边缘留0.4空白，防止图形抖动
            if y_position > lim[0] + gap and y_position < lim[1] - gap:
                ax.plot(
                    [x_position * gain, (x_position + scale_length) * gain],
                    [y_position * gain, y_position * gain],
                    'k',
                    linewidth = line_width,
                )
                if text_draw: #绘制标签
                    ax.text((x_position + scale_length + 0.1) * gain, y_position * gain - fontsize_fig * gain / 200, str(count), fontsize = fontsize_fig * gain) 
            count = count + 1
    # 显示图形
    plt.show()

micrometer = widgets.interactive_output(
    draw_micrometer, {
        'reading': cs.micrometer_reading_slider
    }
)