# Importation des bibliothèques nécessaires
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Chargement des données SpaceX dans un DataFrame pandas
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Configuration de la disposition de l'application
app.layout = html.Div([
    html.H1('Tableau de bord des lancements SpaceX', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': i, 'value': i} for i in ['ALL SITES', 'CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40']],
                 value='ALL', placeholder="Sélectionnez un site de lancement", searchable=True),
    html.Br(),
    dcc.Graph(id='success-pie-chart'),
    html.Br(),
    html.P("Plage de masse utile (kg):"),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload], 
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}),
    dcc.Graph(id='success-payload-scatter-chart'),
])

# Fonction de rappel pour mettre à jour le graphique en secteurs
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))
def update_pie_chart(site):
    df = spacex_df[spacex_df['Launch Site'] == site] if site != 'ALL' else spacex_df
    fig = px.pie(df, names='Launch Site', values='class', title='Réussites de lancement')
    return fig

# Fonction de rappel pour mettre à jour le graphique de dispersion
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])
def update_scatter_chart(site, payload_range):
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if site != 'ALL':
        df = df[df['Launch Site'] == site]
    fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return fig

# Lancement de l'application
if __name__ == '__main__':
    app.run_server()
