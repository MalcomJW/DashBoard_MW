#imports

import dash

#dcc is dash cor comp
from dash import dcc, html
#callback deco
from dash.dependencies import Output, Input
import pandas as pd
#map build via exp
import plotly.express as px
#dbc das boot comp
import dash_bootstrap_components as dbc


df =pd.read_csv("assets/2019.csv")
#app is our object
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



#app is held within the container
app.layout = dbc.Container([
    html.Div(className='app-header', children=[
        html.H1("Happiness around the World", className='display-3')
    ]),

    #dropdown box options
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="metric-dropdown",
                options=[
                    {'label': 'Happiness Score', 'value': 'Score'},
                    {'label': 'GDP per capita', 'value': 'GDP per capita'},
                    {'label': 'Social Support', 'value': 'Social support'},
                    {'label': 'Healthy Life expectancy', 'value': 'Healthy life expectancy'},
                    {'label': 'Freedom to make life choices', 'value': 'Freedom to make life choices'},
                    {'label': 'Generosity', 'value': 'Generosity'},
                    {'label': 'Perceptions of corruption', 'value': 'Perceptions of corruption'},

                ],
                value='Score',
                style={'width': '100%'}

            )

        ], width={'size':6, 'offset':3}, className='drop-container')

    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='world-map'), width=12)
    ]),
    #Countries
    dbc.Row([
        dbc.Col([
            #id data Clasnam stylin
            html.Div(id='data-insights', className='data-insights'),
            html.Div(id='top-bottom-countries', className='top-bottom-countries')
            #width 80% screen
        ], width=8),
        dbc.Col([html.Div(id='country-details', className='country-details')], width=4)
    ])

], fluid=True)


#callback Flaskroute
#map callback >dropdowninput > map result
@app.callback(
    #need id and comp prop
    Output('world-map', 'figure'),
    Input('metric-dropdown', 'value')

)
def update_map(selected_metric):
    fig = px.choropleth(
        df,
        locations='Country or region',
        locationmode='country names',
        color=selected_metric,
        hover_name="Country or region",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"World Hapiness Index:{selected_metric}"
    )
    #r right t top l left b bottom
    fig.update_layout(margin={"r":0,"t":40, "l":0, "b":40})
    return fig

#topbot country
@app.callback(
    Output('data-insights', 'children'),
    Input('metric-dropdown', 'value')
)
def update_insights(selected_metric):
    highest = df.loc[df[selected_metric].idxmax()]
    lowest = df.loc[df[selected_metric].idxmin()]
    insights =[
        html.H3(f"Highest:{selected_metric}:{highest['Country or region']} ({highest[selected_metric]})"),
        html.H3(f"Lowest:{selected_metric}:{lowest['Country or region']} ({lowest[selected_metric]})"),
    ]

    return insights

#top and bottom numbers
@app.callback(
    Output('top-bottom-countries', 'children'),
    Input('metric-dropdown',    'value')
)
# nlargest top 5 nsmallest bottom 5
def update_top_bottom(selected_metric):
    top_countries = df.nlargest(5, selected_metric)
    bottom_countries = df.nsmallest(5, selected_metric)
    #iterating through top and bottom countries. UL unordered list. LI list item
    #FOR to go through the rows.
    top_countries_list = html.Ul([html.Li(f"{'Country or Region'}: {row[selected_metric]}")
                                  for _, row in top_countries.iterrows()])
    bottom_countries_list = html.Ul([html.Li(f"{'Country or Region'}: {row[selected_metric]}")
                                  for _, row in bottom_countries.iterrows()])
    return html.Div([
        html.Div([html.H3("Top 5 Countries"), top_countries_list], className="top-bottom-selection"),
        html.Div([html.H3("Bottom 5 Countries"), bottom_countries_list], className="top-bottom-selection")
    ], className='top-bottom-container')

#country click
@app.callback(
    Output('country-details', 'children'),
    Input('world-map', 'clickData')
)

def display_country_details(clickData):
    if clickData:
        country_name = clickData['points'][0]['location']
        country_data = df[df["Country or region"] == country_name]

        if not country_data.empty:
            country = country_data.iloc[0]
            details = [
                html.H3(f"Details for {country_name}"),
                html.P(f"Overall Rank: {country['Overall rank']}"),
                html.P(f"Score: {country['Score']}"),
                html.P(f"GDP per Capita: {country['GDP per capita']}"),
                html.P(f"Social Support: {country['Social support']}"),
                html.P(f"Healthy life Expectancy: {country['Healthy life expectancy']}"),
                html.P(f"Freedom to Make Life Choices: {country['Freedom to make life choices']}"),
                html.P(f"Generosity: {country['Generosity']}"),
                html.P(f"Perceptions of Corruption: {country['Perceptions of corruption']}")
            ]

            return html.Div(details, className='country-details-section')
    return html.Div("Click country for details", className='country-details-section')




if __name__=="__main__":
    app.run_server(debug=True)
