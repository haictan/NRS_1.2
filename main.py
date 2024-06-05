import dash
from dash import html
import dash_bootstrap_components as dbc
import statebar
import menu
import workspace
import templates.index_string as template

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)

# 使用自定义 HTML 模板
app.index_string = template.index_string

# 构建Dash布局
app.layout = html.Div([
    statebar.create_layout(),
    menu.create_layout(),
    workspace.create_layout(),
    ],
    style={
        'max-width': '1200px',  # 设置网页的最大宽度
        'margin': '0 auto',     # 水平居中
        'padding': '20px'       # 内边距以增加与窗口边缘的距离
    }
)
#注册回调函数
statebar.register_callbacks(app)
menu.register_callbacks(app)
workspace.register_callbacks(app)

if __name__ == '__main__':
    #app.run_server(host='192.168.1.104', port=8866, debug=False)
    app.run_server(debug=True)
    #app.run_server()