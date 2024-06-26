import dash
from dash import dcc, html
import dash_leaflet as dl
from dash.dependencies import Input, Output
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Autenticación con Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('google_credentials.json', scopes=scope)
client = gspread.authorize(creds)

# ID de la hoja de cálculo y nombre de la hoja
spreadsheet_id = '1q2U_TtqR_ohBFenYr6Iq3ADS_lFTNpD8x9qnQO4ROuE'
sheet_name_v1 = 'v1'
sheet_name_v2 = 'v2'

# Cargar los datos desde las hojas de cálculo
sheet_v1 = client.open_by_key(spreadsheet_id).worksheet(sheet_name_v1)
data_v1 = sheet_v1.get_all_values()
df_v1 = pd.DataFrame(data_v1[1:], columns=data_v1[0])

sheet_v2 = client.open_by_key(spreadsheet_id).worksheet(sheet_name_v2)
data_v2 = sheet_v2.get_all_values()
df_v2 = pd.DataFrame(data_v2[1:], columns=data_v2[0])

# Crear la instancia de la aplicación Dash
app = dash.Dash(__name__)

# URL de la imagen
imagen_url = "https://raw.githubusercontent.com/oyucra/DME/main/img/LogoV1.png"

# URL del archivo SVG en GitHub
ico_ficha = "https://raw.githubusercontent.com/oyucra/DME/main/icon/tab_icon_125139.svg"



# Define un ícono (por ejemplo, un icono de punto de exclamación)
icono = html.I(className="fas fa-exclamation-circle")

# Obtener los valores únicos del campo NombreEntidad para el Dropdown en v1
nombre_entidad_options_v1 = [{'label': entidad, 'value': entidad} for entidad in df_v1['NombreEntidad'].unique()]

# Filtrar las celdas no vacías en el campo 'INFORME emitido por la DME'
df_informe = df_v1[df_v1['INFORME emitido por la DME'] != '']

# Obtener la cantidad de celdas no vacías
cantidad_celdas_no_vacias = len(df_informe)

# Obtener los valores únicos del campo NombreEntidad para el Dropdown en v2
nombre_entidad_options_v2 = [{'label': entidad, 'value': entidad} for entidad in df_v2['NombreEntidad'].unique()]

# Diseño del tablero de control con el gráfico de barras, el mapa y el combobox

app.layout = html.Div(
    children=[
        html.Div(
            className='main-container',
            style={'display': 'flex', 'align-items': 'center','justify-content': 'space-between'},  # Alinear elementos verticalmente
            children=[
                # Panel Logo
                html.Div(
                    style={'margin-right': 'auto', 'display': 'flex', 'align-items': 'center'},  # Ajusta el espaciado a la izquierda del texto
                    children=[
                        html.Img(src=imagen_url, style={'width': '4%'}),
                            html.Div(
                                children=[
                                    html.H1("Panel de seguimiento a la evaluación de fichas tecnicas - DME",
                                    style={'text-align':'center', 'color': 'white','font-size':'20px','marginBottom': '2px'}),
                                    html.H3("Fecha Actualizacion:",style={'font-size':'15px','marginTop': '2px','color': 'yellow'})
                                ],
                            ),    
                    ],
                    
                ),
                
                # Cuadro de resultados
                html.Div(
                    id='resultado-conteo-container',  # Contenedor interno para el padding
                    children=[
                        html.Div(
                            #className='s-resultado',
                            id='resultado-conteo',
                            children=[
                            #style={'display': 'flex', 'align-items': 'center'}, 
                                html.Img(src=ico_ficha,style={'width': '20%', 'height': '20%'}),
                                html.H1(cantidad_celdas_no_vacias,style={'fontSize': '25px'})  # Mostrar la cantidad de celdas no vacías
                            ],
                            style={'margin-left': 'auto', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center','background-color': 'lightblue','margin': '0 0px'}  # Alinea a la derecha        
                        ),    
                    ],
                #    style={'margin-left': 'auto', 'padding': '1px'}  # Agrega padding y color de fondo al contenedor interno
                ),
            ],
        ),
        


        html.Div(children='''
            Visualización de datos desde Google Sheets.
        '''),

        # combobox para v1
        html.Div(
            className='control-container',
            style={'marginRight': '20px'},  # Ajustar el margen entre los controles
            children=[
                dcc.Dropdown(
                    id='nombre-entidad-dropdown-v1',
                    options=nombre_entidad_options_v1,
                    value=None,
                    placeholder='Selecciona una entidad'
                )
            ]
        ),

        # Contenedor principal usando Flexbox 
        html.Div(
            className='main-container',
            style={'display': 'flex', 'flexDirection': 'row'},
            children=[
                # Contenedor de la gráfica de barras para v1
                html.Div(
                    id='bar-chart-container-v1',
                    className='bar-chart-container',
                    style={'border': '2px solid white', 'padding': '10px', 'flex': '40%'},
                    children=[
                        html.Button('NombreTipoProceso', id='button-nombre-tipoproceso-v1', n_clicks=0, style={'marginBottom': '10px'}),
                        html.Button('Tipo', id='button-tipo-v1', n_clicks=0),
                        dcc.Graph(
                            id='bar-chart-v1',
                            config={'displayModeBar': False},  # Oculta la barra de herramientas del gráfico
                            style={'color': 'white'}  # Aplica el color blanco al texto del gráfico de barras
                        )
                    ]
                ),

                # Contenedor adicional entre el gráfico de barras y el mapa
                html.Div(
                    id='additional-container',
                    style={'flex': '20%'},
                    children=[
                        # Aquí puedes agregar cualquier contenido adicional
                        html.H3("Contenido Adicional"),
                        html.P("Este es un contenedor adicional entre el gráfico de barras y el mapa."),
                    ]
                ),
                # Contenedor del mapa para v2
                html.Div(
                    id='map-container-v2',
                    className='map-container',
                    style={'border': '2px solid white', 'padding': '10px', 'flex': '20%', 'marginTop': '20px', 'marginLeft': '20px'},
                    children=[
                        dl.Map(
                            id='map-v2',
                            style={'width': '100%', 'height': '400px'},
                            center=[-9.189967, -75.015152],  # Coordenadas de Lima
                            zoom=4.5,
                            children=[
                                dl.TileLayer(),
                                dl.Marker(id='marker-v2', position=(0, 0), children=[
                                    dl.Tooltip(id='tooltip-v2')
                                ])  # posición inicial del marcador con tooltip
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    [Output('bar-chart-v1', 'figure')],
    [Input('button-nombre-tipoproceso-v1', 'n_clicks'),
     Input('button-tipo-v1', 'n_clicks'),
     Input('nombre-entidad-dropdown-v1', 'value')]
)

def update_graph_v1(n_clicks_nombre_tipoproceso, n_clicks_tipo, selected_entidad):
    ctx = dash.callback_context
    if not ctx.triggered:
        selected_field = 'NombreTipoProceso'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'button-nombre-tipoproceso-v1':
            selected_field = 'NombreTipoProceso'
        else:
            selected_field = 'Tipo'

    # Filtrar el DataFrame por la entidad seleccionada
    filtered_df = df_v1 if selected_entidad is None else df_v1[df_v1['NombreEntidad'] == selected_entidad]

    # Filtrar las celdas no vacías en el campo 'INFORME emitido por la DME'
    df_informe = filtered_df[filtered_df['INFORME emitido por la DME'] != '']

    # Calcular la cantidad de valores registrados en el campo 'INFORME emitido por la DME' por cada 'NombreTipoRegimen'
    informe_counts = df_informe.groupby(selected_field)['INFORME emitido por la DME'].count().reset_index()

    # Lista de subestados que queremos contar
    subestados_a_contar = ['REVISADO', 'EVALUADO', 'OBSERVADO EN EVALUACION', 'SUBSANADO EN EVALUACION', 'EVALUACION EN PROCESO']

    # Calcular el recuento de cada tipo de régimen
    count_by_selected_field = filtered_df[selected_field].value_counts()

    # Calcular la cantidad de registros para cada campo seleccionado
    count_by_subestado = filtered_df[filtered_df['SubEstado'].isin(subestados_a_contar)].groupby(selected_field).size()

    # Configurar estilo del texto y fondo del gráfico
    fig = {
    'data': [
        {'x': count_by_selected_field.index, 'y': count_by_selected_field.values, 'type': 'bar', 'name': selected_field, 'marker': {'color':'rgba(175, 215, 231, 0.7)'}},
        {'x': count_by_subestado.index, 'y': count_by_subestado.values, 'type': 'bar', 'name': 'Cantidad de Subestados','marker':{'color':'rgba(0, 102, 153, 0.7)'},'width':0.6},
        {'x': informe_counts[selected_field], 'y': informe_counts['INFORME emitido por la DME'], 'type': 'bar', 'name': 'Informes DME emitidos','marker':{'color':'rgba(0, 3, 128, 0.7)'}, 'width':0.4}
    ],
    'layout': {
        'title': 'Comparación de cantidad de datos',
        'plot_bgcolor': 'rgba(0,0,0,0)',  # Hacer el fondo del gráfico transparente
        'paper_bgcolor': 'rgba(0,0,0,0)',  # Hacer el fondo del papel transparente
        'font': {'color': 'white'},  # Establecer el color del texto en blanco
        'legend': {'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        'barmode': 'overlay'  # Permitir que las barras se superpongan
    }
}

    return [fig]


@app.callback(
    [Output('map-v2', 'center'),
     Output('marker-v2', 'position'),
     Output('tooltip-v2', 'children')],  # Agregar salida para tooltip
    [Input('nombre-entidad-dropdown-v1', 'value')]
)
def update_map_v2(selected_entity):
    if selected_entity is not None:
        entity_data = df_v2[df_v2['NombreEntidad'] == selected_entity]
        # Tomar la primera ubicación de la EPS seleccionada
        lat = float(entity_data.iloc[0]['Latitud'])
        lon = float(entity_data.iloc[0]['Longitud'])
        # Obtener los valores de "tipo" y "Cfichas"
        tipo = entity_data.iloc[0]['tipo']
        cfichas = entity_data.iloc[0]['Cfichas']
        # Crear texto para el tooltip
        tooltip_text = f'Tipo: {tipo}, Cfichas: {cfichas}'
        return ([lat, lon], (lat, lon), tooltip_text)  # Devolver solo el centro del mapa, la posición del marcador y el tooltip
    else:
        # Si no se ha seleccionado ninguna entidad, centrar el mapa en Lima
        return ([-9.189967, -75.015152], (0, 0), '')  # Devolver tooltip vacío cuando no se selecciona ninguna entidad

if __name__ == '__main__':
    #app.run_server(debug=True, host='0.0.0.0')
    app.run_server(debug=True)
