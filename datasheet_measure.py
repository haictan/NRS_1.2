from dash import html, dash_table
from dash.dependencies import Input, Output
from dash.dash_table.Format import Format, Scheme
import id_strings as id
import lang_strings as la
import datasheet_store as ds

def create_layout():

    title_style = {'textAlign': 'left', 'fontSize': '100%', 'marginTop': '10px'}
    label_style = {'textAlign': 'right', 'fontSize': '82%', 'textAlign': 'center'}
    row_style = {'marginTop': '10px'}

    datasheet = html.Div(
        [
            dash_table.DataTable(
                id=id.str_datasheet_measure,
                columns=[
                    {'name': ds.str_rings_num, 'id': ds.str_rings_num,},
                    {'name': ds.str_rings_pos_left, 'id': ds.str_rings_pos_left, "type": "numeric", "editable": True, 'format': Format(precision=3, scheme=Scheme.fixed)},
                    {'name': ds.str_rings_pos_right, 'id': ds.str_rings_pos_right, "type": "numeric", "editable": True, 'format': Format(precision=3, scheme=Scheme.fixed)},
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
                        'pointerEvents': 'auto',
                        'width': '30%'
                    },
                    {
                        'if': {'column_id': ds.str_rings_pos_right},
                        'pointerEvents': 'auto',
                        'width': '30%'
                    },
                    {
                        'if': {'column_id': ds.str_rings_diameter},
                        'pointerEvents': 'none',
                        'width': '25%'
                    }
                ],
                page_size=11,  # 每页显示5行
                #sort_action='native',  # 启用排序功能
                #filter_action='native',  # 启用过滤功能
                #row_selectable='multi',  # 允许选择多行
                #selected_rows=[]  # 初始选择的行
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

def register_callbacks(app):
    @app.callback(
    Output(id.str_datasheet_measure, 'data'),
    [Input(id.str_datasheet_measure, 'data')]
    )
    def update_average(data):
        for row in data:
            try:
                left = float(row[ds.str_rings_pos_left]) if row[ds.str_rings_pos_left] else None
                right = float(row[ds.str_rings_pos_right]) if row[ds.str_rings_pos_right] else None
                if left is not None and right is not None:
                    diameter = abs(right - left)
                    row[ds.str_rings_diameter] = diameter
                    row[ds.str_rings_diameter_2] = diameter * diameter
                else:
                    row[ds.str_rings_diameter] = ''
                    row[ds.str_rings_diameter_2] = 0
            except ValueError:
                row[ds.str_rings_diameter] = ''
                row[ds.str_rings_diameter_2] = 0
        ds.data = data
        return data