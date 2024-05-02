import dash
from dash import dcc, html

# Crear una aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div([
    html.Div([
        html.H1("Resultado: 45"),
        html.H1("✔️"),
        html.H1("15%", style={'color': 'red', 'font-size': '20px'})
    ], style={'border': '2px solid black', 'padding': '10px'})
])




# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
