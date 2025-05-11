from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

semana_cols = ['Semana_01', 'Semana_02', 'Semana_03', 'Semana_04', 'Semana_05', 'Semana_06']
df = pd.DataFrame({
    'Ejecutivo': [
        'GONZALEZ MORENO CAMILA DE LA PAZ', 'GONZÁLEZ HERNÁNDEZ CAROLINA FRANCISCA',
        'PEREZ ORDOÑEZ IRALYS ELENA', 'GAETE MENA JAIME ANTONIO',
        'YAÑEZ ILABACA MATIAS IGNACIO', 'VARGAS LIZANA SANDRA',
        'ARREDONDO AROS ANGELICA SOLEDAD', 'UGARTE GOMEZ FERNANDA IVETTE',
        'ROMERO BALDEON IVONNE PATRICIA', 'VALLECILLA CABEZAS LINA FERNANDA',
        'PROMEDIO 262'
    ],
    'Semana_01': [918, 820, 1100, 745, 916, 875, 835, 857, 955, 807, 874],
    'Semana_02': [820, 587, 1026, 726, 807, 795, 635, 666, 950, 705, 729],
    'Semana_03': [953, 650, 1021, 680, 744, 603, 515, 661, 896, 678, 742],
    'Semana_04': [726, 586, 766, 639, 754, 411, 530, 628, 857, 608, 654],
    'Semana_05': [650, 480, 749, 672, 592, 0, 490, 128, 584, 570, 654],
    'Semana_06': [804, 586, 839, 699, 702, 503, 530, 148, 905, 578, 658]
})

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    html.H2("TMO por Ejecutivo y Semana", className="text-center text-primary mb-4"),
    dbc.Row([
        dbc.Col([
            html.Label("Buscar Ejecutivo:", className="fw-bold mt-2"),
            dcc.Input(
                id='busqueda_ejecutivo',
                type='text',
                placeholder='Filtrar por nombre...',
                debounce=True,
                style={"width": "100%", "margin-bottom": "10px"}
            ),
            html.Label("Seleccionar Ejecutivo(s):", className="fw-bold"),
            html.Div([
                dcc.Checklist(
                    id='selector_ejecutivo',
                    options=[{'label': x, 'value': x} for x in df['Ejecutivo'].unique()],
                    value=[df['Ejecutivo'].iloc[2]],
                    inputStyle={"margin-right": "8px"},
                    labelStyle={"display": "block", "margin-bottom": "6px"}
                )
            ], style={"height": "500px", "overflowY": "scroll", "border": "1px solid #ccc", "padding": "10px"})
        ], width=3),

        dbc.Col([
            dcc.Graph(id='grafico_llamadas')
        ], width=9)
    ])
], fluid=True)

@app.callback(
    Output('selector_ejecutivo', 'options'),
    Input('busqueda_ejecutivo', 'value')
)
def filtrar_lista_ejecutivos(filtro):
    if not filtro:
        return [{'label': x, 'value': x} for x in df['Ejecutivo'].unique()]
    filtrado = [x for x in df['Ejecutivo'].unique() if filtro.lower() in x.lower()]
    return [{'label': x, 'value': x} for x in filtrado]

@app.callback(
    Output('grafico_llamadas', 'figure'),
    Input('selector_ejecutivo', 'value')
)
def actualizar_grafico(ejecutivos):
    datos = df[df['Ejecutivo'].isin(ejecutivos)] if ejecutivos else df.iloc[[]]

    fig = go.Figure()
    for semana in semana_cols:
        fig.add_trace(go.Bar(
            x=datos['Ejecutivo'],
            y=datos[semana],
            name=semana,
            width=0.15
        ))

    fig.update_layout(
        barmode='group',
        xaxis_title='Ejecutivo',
        yaxis_title='TMO',
        title='TMO por Ejecutivo y Semana',
        template='plotly_white',
        bargap=0.35,
        xaxis_tickangle=-45
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
