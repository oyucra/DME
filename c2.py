import dash
from dash import html

app = dash.Dash(__name__)

# URL del archivo SVG en GitHub
github_svg_url = "https://raw.githubusercontent.com/oyucra/DME/main/icon/tab_icon_125139.svg"

app.layout = html.Div(
    style={'display': 'flex', 'align-items': 'center'},
    children=[
    html.H4("85"),
    html.Div(
        html.H2("pruebaq"),
    ),
    html.Img(src=github_svg_url, style={'width': '5%', 'height': '5%'})
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
