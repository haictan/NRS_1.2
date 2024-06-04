from dash import html, dash_table
from dash.dash_table.Format import Format, Scheme
import id_strings as id
import lang_strings as la
import datasheet_store as ds
import style_strings as ss

def create_layout():

    column_name = ds.str_rings_diameter_2
    diameter_data = [row[column_name] for row in ds.data]
    data_half_length = round(len(diameter_data) / 2)
    diameter_dd = []
    for i,data in enumerate(diameter_data):
        if i >= data_half_length:
            dd = diameter_data[i] - diameter_data[i-data_half_length]
            diameter_dd.append(dd)
    for i,row in enumerate(ds.data):
        if i < len(diameter_dd):
            row[ds.str_rings_diameter_dd] = diameter_dd[i]

    datasheet = html.Div(
        [
            dash_table.DataTable(
                id=id.str_datasheet_measure,
                columns=[
                    {'name': ds.str_rings_num, 'id': ds.str_rings_num,},
                    {'name': ds.str_rings_diameter, 'id': ds.str_rings_diameter, "type": "numeric", 'format': Format(precision=3, scheme=Scheme.fixed)},
                    {'name': ds.str_rings_diameter_2, 'id': ds.str_rings_diameter_2,"type": "numeric", 'format': Format(precision=3, scheme=Scheme.fixed)},
                    #{'name': ds.str_rings_diameter_dd, 'id': ds.str_rings_diameter_dd,"type": "numeric", 'format': Format(precision=3, scheme=Scheme.fixed)},

                ],
                data=ds.data,
                style_table={'overflowX': 'auto'},  # 当表格内容超出容器宽度时，添加水平滚动条
                style_cell={
                    #'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                    'whiteSpace': 'normal',
                    'textAlign': 'center',
                },
                style_header = ss.label_style,
                style_data_conditional=[
                    {
                        'if': {'column_id': ds.str_rings_num},
                        'pointerEvents': 'none',
                        'backgroundColor': '#f3f3f3',
                        'width': '15%'
                    },
                    {
                        'if': {'column_id': ds.str_rings_diameter},
                        'pointerEvents': 'none',
                        'width': '25%'
                    },
                    {
                        'if': {'column_id': ds.str_rings_diameter_2},
                        'pointerEvents': 'none',
                        'width': '25%'
                    },
                    {
                        'if': {'column_id': ds.str_rings_diameter_dd},
                        'pointerEvents': 'none',
                        'width': '25%'
                    },
                ],
                page_size=11,  # 每页显示5行
            )
        ]
    )

    layout = html.Div(
        [
            html.H1(la.str_title_mea_result, style=ss.title_style),
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

def register_callback(app):
    return None