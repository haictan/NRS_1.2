from dash import html, dash_table
from dash.dash_table.Format import Format, Scheme
import pandas as pd
import statebar
import id_strings as id
import lang_strings as la
import style_strings as ss

def create_layout():

    id_wavelength = la.str_ctr_slider_label_wavelength
    id_radius_curvature = la.str_ctr_slider_label_radius_curvature
    id_refractive_index = la.str_ctr_slider_label_refractive_index
    id_interference_range = la.str_ctr_slider_label_interference_range
    id_reflector_angle = la.str_ctr_slider_label_reflector_angle
    id_eyepiece_height = la.str_ctr_slider_label_eyepiece_height

    val_wavelength = statebar.state_rings.get('wavelength')
    val_radius_curvature = statebar.state_rings.get('radius_curvature')
    val_refractive_index = statebar.state_rings.get('refractive_index')
    val_interference_range = statebar.state_rings.get('interference_range')
    val_reflector_angle = statebar.state_rings.get('reflector_angle')
    val_eyepiece_height = statebar.state_rings.get('eyepiece_height')

    data_temp = {
        id_wavelength : [val_wavelength],
        id_radius_curvature : [val_radius_curvature],
        id_refractive_index : [val_refractive_index],
        id_interference_range : [val_interference_range],
        id_reflector_angle : [val_reflector_angle],
        id_eyepiece_height : [val_eyepiece_height],
    }
    df = pd.DataFrame(data_temp)
    data_system = df.to_dict('records')

    datasheet = html.Div(
        [
            dash_table.DataTable(
                id=id.str_datasheet_system,
                columns=[
                    {'name': id_wavelength, 'id': id_wavelength, "type": "numeric", 'format': Format(precision=1, scheme=Scheme.fixed)},
                    {'name': id_radius_curvature, 'id': id_radius_curvature, "type": "numeric", 'format': Format(precision=2, scheme=Scheme.fixed)},
                    {'name': id_refractive_index, 'id': id_refractive_index,"type": "numeric", 'format': Format(precision=2, scheme=Scheme.fixed)},
                    {'name': id_interference_range, 'id': id_interference_range,"type": "numeric", 'format': Format(precision=1, scheme=Scheme.fixed)},
                    {'name': id_reflector_angle, 'id': id_reflector_angle,"type": "numeric", 'format': Format(precision=0, scheme=Scheme.fixed)},
                    {'name': id_eyepiece_height, 'id': id_eyepiece_height,"type": "numeric", 'format': Format(precision=0, scheme=Scheme.fixed)},

                ],
                data=data_system,
                style_table={'overflowX': 'auto'},  # 当表格内容超出容器宽度时，添加水平滚动条
                style_cell={
                    #'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                    'whiteSpace': 'normal',
                    'textAlign': 'center',
                },
                style_header = ss.label_style,
                style_data_conditional=[
                    { 'if': {'column_id': id_wavelength}, 'pointerEvents': 'none', 'width': '12%'},
                    { 'if': {'column_id': id_radius_curvature}, 'pointerEvents': 'none', 'width': '10%'},
                    { 'if': {'column_id': id_refractive_index}, 'pointerEvents': 'none', 'width': '9%'},
                    { 'if': {'column_id': id_interference_range}, 'pointerEvents': 'none', 'width': '12%'},
                    { 'if': {'column_id': id_reflector_angle}, 'pointerEvents': 'none', 'width': '12%'},
                    { 'if': {'column_id': id_eyepiece_height}, 'pointerEvents': 'none', 'width': '10%'},

                ],
                page_size=2,  # 每页显示2行
            )
        ]
    )

    layout = html.Div(
        [
            html.H1(la.str_title_mea_system, style=ss.title_style),
            datasheet,
        ],
        style={#'textAlign': 'center',
               #'border': '1px solid black',
               'marginTop': '10px',
               #'width': '100%',
                #'height': '30%',
               },
    )

    return layout