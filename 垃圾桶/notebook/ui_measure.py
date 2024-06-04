import ipywidgets as widgets
import newton_rings
import micrometer
import control_sliders as cs

#内容居中
center_layout = widgets.Layout(display='flex', justify_content='center', align_items='center')
#视图布置
reading = widgets.VBox([micrometer.micrometer, cs.micrometer_reading_slider])
ui = widgets.HBox([newton_rings.rings, reading], layout = center_layout)