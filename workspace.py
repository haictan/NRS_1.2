import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import lang_strings as la
import id_strings as id
import welcome
import workspace_principle
import workspace_adjust
import workspace_measure
import workspace_device
import workspace_read
import workspace_game
import workspace_data
import statebar

def create_layout():
    layout = html.Div(id=id.str_workspace)
    return layout
    
def register_callbacks(app):
    #注册所有工作区
    welcome.register_callbacks(app)
    workspace_adjust.register_callbacks(app)
    workspace_measure.register_callbacks(app)
    workspace_data.register_callback(app)
    #点击菜单栏更新工作区
