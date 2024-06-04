from dash import html, dash_table
from dash.dash_table.Format import Format, Scheme
import id_strings as id
import lang_strings as la
import datasheet_store as ds

def create_layout():
                
    title_style = {'textAlign': 'left', 'fontSize': '100%', 'marginTop': '10px'}
    label_style = {'textAlign': 'right', 'fontSize': '82%', 'textAlign': 'center'}

    datasheet = html.Div(
        [
            dash_table.DataTable(
                id=id.str_datasheet_analysis,
                columns=[
                    {'name': ds.str_rings_num, 'id': ds.str_rings_num,},
                    {'name': ds.str_rings_pos_left, 'id': ds.str_rings_pos_left, "type": "numeric", 'format': Format(precision=3, scheme=Scheme.fixed)},
                    {'name': ds.str_rings_pos_right, 'id': ds.str_rings_pos_right, "type": "numeric", 'format': Format(precision=3, scheme=Scheme.fixed)},
                    {'name': ds.str_rings_diameter, 'id': ds.str_rings_diameter,"type": "numeric", 'format': Format(precision=3, scheme=Scheme.fixed)},
                ],
                data=ds.data,
                style_table={'overflowX': 'auto'},  # 当表格内容超出容器宽度时，添加水平滚动条
                style_cell={
                    #'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                    'whiteSpace': 'normal',
                    'textAlign': 'center',
                },
                style_header = label_style,
                style_data_conditional=[
                    {
                        'if': {'column_id': ds.str_rings_num},
                        'pointerEvents': 'none',
                        'backgroundColor': '#f3f3f3',
                        'width': '15%'
                    },
                    {
                        'if': {'column_id': ds.str_rings_pos_left},
                        'pointerEvents': 'none',
                        'width': '30%'
                    },
                    {
                        'if': {'column_id': ds.str_rings_pos_right},
                        'pointerEvents': 'none',
                        'width': '30%'
                    },
                    {
                        'if': {'column_id': ds.str_rings_diameter},
                        'pointerEvents': 'none',
                        'width': '25%'
                    }
                ],
                page_size=11,  # 每页显示5行
            )
        ]
    )

    layout = html.Div(
        [
            html.H1(la.str_title_mea_datasheet, style=title_style),
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
