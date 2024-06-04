from IPython.display import display, clear_output
import ipywidgets as widgets
import control_sliders as cs
import newton_rings
import device_diagram


rings_control = widgets.VBox([newton_rings.rings, cs.ring_control_sliders])
microscope_lens = widgets.VBox([device_diagram.microscope, device_diagram.lens])

center_layout = widgets.Layout(display='flex', justify_content='center', align_items='center')
ui = widgets.HBox([rings_control, microscope_lens], layout = center_layout)
