from dash import html
import media_source as ms
import id_strings as id

def create_layout():
    video = html.Div([
    html.Video(
            controls=True,
            id=id.str_device_video,
            src=ms.vid_device, 
            style={"width": "100%",'height': 'auto', 'marginTop': '15px'}
        ),
    ],
    style={'textAlign': 'center',}
    )

    layout = html.Div([video])
    return layout