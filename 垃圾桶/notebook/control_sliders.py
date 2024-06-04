import ipywidgets as widgets

# 创建滑块控件
slider_width = '520px'
slider_width_unread = '445px'
slider_button_width = '65px'

wavelength_slider = widgets.FloatSlider(
    value=550,
    min=380,
    max=750,
    step=0.1,
    description='波长(nm):',
    readout_format='.1f'
)
wavelength_slider.layout.width = slider_width

radius_slider = widgets.FloatSlider(
    value=1.00,
    min=0.50,
    max=2.00,
    step=0.01,
    description='曲率半径(m):',
    #continuous_update=False,
)
radius_slider.layout.width = slider_width

refractive_index_slider = widgets.FloatSlider(
    value=1.00,
    min=1.00,
    max=2.00,
    step=0.01,
    description='介质折射率:',
    readout_format='.2f'
)
refractive_index_slider.layout.width = slider_width

interference_range_slider = widgets.FloatSlider(
    value=1.50,
    min=0.10,
    max=6.00,
    step=0.01,
    description='视场(mm):'
)
interference_range_slider.layout.width = slider_width

reflector_angle_slider = widgets.FloatSlider(
    value=20.00,
    min=0.00,
    max=90.00,
    step=0.01,
    description='反射镜角度:',
    readout=False,
    #continuous_update=False,
)
reflector_angle_slider.layout.width = slider_width_unread

#一键设置最佳角度
reflector_angle_button = widgets.Button(
    description='最佳',
    tooltip = '设定反射镜角度最佳值',
    layout = widgets.Layout(width = slider_button_width)
)

def on_reflector_angle_button_clicked(b):
    reflector_angle_slider.value = 45

reflector_angle_button.on_click(on_reflector_angle_button_clicked)
    
eyepiece_height_slider = widgets.FloatSlider(
    value=30.0,
    min=0.0,
    max=100.0,
    step=0.1,
    description='目镜高度:',
    readout=False,
    #continuous_update=False,
)
eyepiece_height_slider.layout.width = slider_width_unread

#一键设置最佳高度
eyepiece_height_button = widgets.Button(
    description='最佳',
    tooltip = '设定镜筒高度最佳值',
    layout = widgets.Layout(width = slider_button_width)
)

def on_eyepiece_height_button_clicked(b):
    eyepiece_height_slider.value = 40

eyepiece_height_button.on_click(on_eyepiece_height_button_clicked)

reflector_angle_control = widgets.HBox([reflector_angle_slider, reflector_angle_button])
eyepiece_height_control = widgets.HBox([eyepiece_height_slider, eyepiece_height_button])

#牛顿环控制滑块组合
ring_control_sliders = widgets.VBox([
    wavelength_slider,
    radius_slider,
    refractive_index_slider,
    interference_range_slider,
    reflector_angle_control,
    eyepiece_height_control,
    ]
)

#测微鼓轮读数滑块
micrometer_reading_slider = widgets.FloatSlider(
    value=5,
    min=0,
    max=10,
    step=0.001,
    description='读数:',
    readout_format='.3f'
)
micrometer_reading_slider.layout.width = slider_width