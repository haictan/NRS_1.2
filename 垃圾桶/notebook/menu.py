import ipywidgets as widgets
from IPython.display import display
import state_bar
import lang_strings as la

def menu_events(button):
    state_bar.mode_text.value = button.description

principle = widgets.Button(
    description = la.str_menu_principle,
    button_style = 'info',
    tooltip = la.str_menu_principle_description,
    icon='search'
)
principle.on_click(menu_events)

adjust = widgets.Button(
    description = la.str_menu_adjust,
    button_style='info',
    tooltip = la.str_menu_adjust_description,
    icon='search'
)
adjust.on_click(menu_events)

measure = widgets.Button(
    description = la.str_menu_measure,
    button_style = 'info',
    tooltip = la.str_menu_measure_description,
    icon = 'search'
)
measure.on_click(menu_events)

device = widgets.Button(
    description = la.str_menu_device,
    button_style ='info',
    tooltip= la.str_menu_device_description,
    icon='search'
)
device.on_click(menu_events)

read = widgets.Button(
    description = la.str_menu_read,
    button_style='info',
    tooltip = la.str_menu_read_description,
    icon='search'
)
read.on_click(menu_events)

game = widgets.Button(
    description = la.str_menu_game,
    button_style='info',
    tooltip = la.str_menu_game_description,
    icon='check'
)
game.on_click(menu_events)

center_layout = widgets.Layout(display='flex', justify_content='center', align_items='center')
menu = widgets.HBox([principle, adjust, measure, device, read, game], layout = center_layout)
