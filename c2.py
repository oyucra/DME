import dash
from dash import html

# Crear una aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación con un style personalizado
app.layout = html.Div(style={'backgroundColor': 'lightblue', 'padding': '20px'}, children=[
    html.H1('Título Principal', style={'color': 'red', 'textAlign': 'center'}),
    html.P('Este es un párrafo con un estilo personalizado.', style={'fontSize': '18px', 'fontWeight': 'bold'})
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
