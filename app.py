import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from flask import Flask

public_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
corona_data = pd.read_csv(public_url)

all_countries = sorted(corona_data['Country/Region'].unique())

df = pd.DataFrame()
for i, country in enumerate(all_countries):
    country_data = corona_data[corona_data['Country/Region'] == country]
    by_date = country_data.sum(axis=0).filter(like='/20')
    df[country] = by_date.transpose()

countries = {
    'asia': ['Korea, South','Japan','China','Singapore','Taiwan*','Thailand'],
    'europe_us': ['France','Germany','Spain','Switzerland','US','Italy']
}

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': 'Asia', 'value': 'asia'},
            {'label': 'Europe/US', 'value': 'europe_us'}
        ],
        value='asia'
    ),
    dcc.Graph(
        id='corona-cases',
        style={'height': '800px'}
    )
])

@app.callback(
    dash.dependencies.Output('corona-cases', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value')])
def update_figure(value):
    fig = go.Figure()
    for country in countries[value]:
        fig.add_trace(go.Scatter(x=df.index, y=df[country], name=country))
    fig.update_traces(mode='markers+lines')
    fig.update_layout(yaxis_type="log", title="Corona Cases per Country")
    return fig

if __name__ == "__main__":
    app.run_server(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))