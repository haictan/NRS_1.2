import ipywidgets as widgets
import lang_strings as la

title_text = widgets.Text(
    value = la.str_state_title,
    disabled = True,
)

mode_text = widgets.Text(
    value = la.str_menu_welcome,
    disabled = True,
    #layout = widgets.Layout(visibility = 'hidden')
)

busy_text = widgets.Text(
    value = la.str_state_unbusy,
    disabled = True,
    #layout = widgets.Layout(visibility = 'hidden')
)

center_layout = widgets.Layout(display='flex', justify_content='center', align_items='center')
state_info = widgets.HBox([mode_text, busy_text])
state_bar = widgets.VBox([title_text, state_info], layout = center_layout)

def busy():
    busy_text.value = la.str_state_busy

def unbusy():
    busy_text.value = la.str_state_unbusy