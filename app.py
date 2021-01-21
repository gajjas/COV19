import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table as dt
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go
import requests
import datetime
import time
from plotly.subplots import make_subplots
from urllib.request import urlopen
import json
import numpy as np
from flask_caching import Cache
import os

# Components
from assets.components.tabs import tabs

#Layouts
from assets.components.layouts.plotLayout import customLayout

#Environment Variables
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv('NYTIMES_API_KEY')
token = os.getenv('MAPBOX_TOKEN')

df = pd.read_csv("https://api.covidtracking.com/v1/states/daily.csv", dtype={"fips": str})
df2 = pd.read_csv("us-countiesv4.csv", dtype={"fips": str})
TIMEOUT = 86400
college_df = pd.read_csv('college_data.csv')

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/darkly/bootstrap.min.css"])
server = app.server
cache = Cache(app.server, config={
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'app-cache'
})

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def timeConverter(s):
    s = str(s)
    y = int(s[0:4])
    mon = int(s[4:6])
    d = int(s[6:8])
    dtime = datetime.datetime(year=y, month=mon, day=d)
    return time.mktime(dtime.timetuple())

def timeC(t):
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d")

@cache.memoize(timeout=1200)
def get_news(state=''):
    query_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=headline:('coronavirus')&api-key=" + apikey +"&sort=newest"

    data = requests.get(query_url).json()['response']['docs']
    news = set()
    for article in data:
        news.add((article['headline']['main'], article['abstract'], article['web_url']))
    return [
        dbc.Card(
            dbc.CardBody(
                [
                    html.A(children=x[0], id='link',
                    href=x[2], target='_blank'),
                    html.H6(x[1]),
                    html.I('Source: NYTimes'),
                ]
            )) for x in news]


# def getMarks(minUnix, maxUnix):
#     for i, date

# Initialise the app

@cache.memoize(timeout=TIMEOUT)
def collegeMap():
    fig = px.scatter_mapbox(college_df, lat="lat", lon="long", hover_data={'lat': False, 'long': False, 'college': True, 'cases': True}, color_discrete_sequence=["#54B98F"], zoom=3, height=1000)
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token, mapbox_zoom=3.1, mapbox_center = {"lat": 38, "lon": -96})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout({"height":463})
    return dcc.Graph(figure=fig)

def plot(var):
    data = df[['date', var]]
    data.date = pd.to_datetime(df['date'], format="%Y%m%d")
    data = data.groupby('date', as_index=False)[var].sum()
    x = data.date.tolist()
    y = data[var].tolist()
    return x, y
    
def graphObject(b, titl, row, col, height):
    fig = make_subplots(
        rows=row, cols=col,
        subplot_titles=(titl))

    fig.update_layout(customLayout)
    fig.update_layout({"height":height})

    for i, v in enumerate(b):
        x, y = plot(v)
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy'),
                row=(i // col) + 1, col=(i % col) + 1)
    
    return dbc.Col(dcc.Graph(figure=fig), width=12)

def countyPlot(var):
    data = df2[['date', var]]
    data.date = pd.to_datetime(df2['date'], format="%Y%m%d")
    data = data.groupby('date', as_index=False)[var].sum()
    x = data.date.tolist()
    y = data[var].tolist()
    return x, y

def countyGraphObject(b, titl, row, col, height):
    fig = make_subplots(
        rows=row, cols=col,
        subplot_titles=(titl))

    fig.update_layout(customLayout)
    fig.update_layout({"height":height})

    for i, v in enumerate(b):
        x, y = countyPlot(v)
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy'),
                row=(i // col) + 1, col=(i % col) + 1)
    
    return dbc.Col(dcc.Graph(figure=fig), width=12)

state_content = html.Div([
        html.Div([
                dbc.Row(
                    dbc.Col([
                            dbc.Select(
                                options=[
                                    {'label': 'Cases per day', 'value': 'positiveIncrease'},
                                    {'label': 'Cumulative Hosiptalizations', 'value': 'hospitalizedCumulative'},
                                    {'label': 'Deaths per day', 'value': 'deathIncrease'},
                                    {'label': 'Total confirmed deaths', 'value': 'death'},         
                                    {'label': 'Current Patients in ICU', 'value':'inIcuCurrently'},
                                    {'label': 'Ventilators Currently Used', 'value':'onVentilatorCurrently'},
                                    {'label': 'Total Recovered', 'value':'recovered'}
                                ],
                                value="positiveIncrease",
                                id = "searchBar",
                                style={
                                    "backgroundColor":"#303030",
                                    "color":"#ffffff",
                                }
                            )
                        ],
                        width={"size": 6, "offset": 3},

                    ),
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P(get_news())
                            ]
                        ),
                    ),
                    width=2,
                    style={
                        'height': '495px',
                        "overflowY": "scroll"
                    }
                ),
                dbc.Col([
                    html.Div(
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(id = "state-map"),
                                )
                            )
                        ),
                        className="mb-3"
                    ),
                    dbc.Row(
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dcc.Slider(
                                                        min= timeConverter(df.date.min()),
                                                        max= timeConverter(df.date.max()),
                                                        step= 86400,
                                                        value= timeConverter(df.date.max()),
                                                        updatemode="drag",
                                                        id="slider",
                                                        className="mt-0 mb-0 py-0"
                                                    )
                                                ],
                                                className="mt-0 mb-0 py-3",
                                            ),
                                        ),
                                        width=9,
                                        className="my-0"
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.P(id="slideDate", style={"fontSize":"12px", "text-align": "center"}, className="my-0")
                                                ],
                                                className="mt-0 mb-0 py-3"
                                            ),
                                        ),
                                        width=3,
                                        className="my-0"
                                    )
                                ]
                            )
                        )
                    )],
                    width=8
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(id='datatable')
                            ],
                            style={'overflowY':'scroll', 'overflowX':'hidden','height': '495px'}
                        ),
                    ), 
                    width=2
                )
            ]
        ),
        html.Div(id="Graphs", children=[
            dbc.Card(
                [
                    dbc.CardBody(
                        html.H4("General Information"),
                        className="p-0"
                    ),
                ],
                style={
                    "textAlign":"center"
                },
                className="my-4 p-2"
            ),
            dbc.Row(
                [
                    graphObject(["positiveIncrease","deathIncrease", "recovered"], ["Daily Cases", "Daily Deaths", "Total Recovered"], 1, 3, 500),
                ]

            ),
            dbc.Card(
                [
                    dbc.CardBody(
                        html.H4("Hospital Information"),
                        className="p-0"
                    ),
                ],
                style={
                    "textAlign":"center"
                },
                className="my-4 p-2"
            ),
            dbc.Row(
                [
                    graphObject(["hospitalizedCumulative","hospitalizedCurrently", "hospitalizedIncrease", "inIcuCumulative", "inIcuCurrently", "onVentilatorCumulative", "onVentilatorCurrently", "deathConfirmed", "deathProbable"], ["Total Hospitalized", "Currently Hospitalized", "Daily Hospitalizations", "Total ICU Patients", "Current ICU Patients", "Ventilator Required Patients", "Patients on Ventilators", "Confirmed Deaths", "Probable Deaths"], 3, 3, 1500)
                ]
            ),
            dbc.Card(
                [
                    dbc.CardBody(
                        html.H4("Test Information"),
                        className="p-0"
                    ),
                ],
                style={
                    "textAlign":"center"
                },
                className="my-4 p-2"
            ),
            dbc.Row(
                [
                    graphObject(["positiveTestsPeopleAntibody", "positiveCasesViral", "positiveTestsPeopleAntigen", "negativeTestsPeopleAntibody", "negative", "totalTestResults"], ["Positive Antibody Tests", "Positive PCR Tests", "Positive Antigen Tests", "Negative Antibody Tests", "Negative PCR Tests", "Total Test Reults"], 2, 3, 1000),
                ]
            ),
        ])
    ]
)

county_content = html.Div([
        html.Div([
                dbc.Row(
                    dbc.Col([
                            dbc.Select(
                                options=[
                                    {'label': 'Cases per day', 'value': 'cases'},
                                    {'label': 'Deaths per day', 'value': 'deaths'},
                                ],
                                value="cases",
                                id = "searchBar-county",
                                style={
                                    "backgroundColor":"#303030",
                                    "color":"#ffffff",
                                }
                            )
                        ],
                        width={"size": 6, "offset": 3},

                    ),
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P(get_news())
                            ]
                        ),
                    ),
                    width=2,
                    style={
                        'height': '495px',
                        "overflowY": "scroll"
                    }
                ),
                dbc.Col([
                    html.Div(
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(id = "county-map"),
                                )
                            )
                        ),
                        className="mb-3"
                    ),
                    dbc.Row(
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dcc.Slider(
                                                        min= timeConverter(df2.date.min()),
                                                        max= timeConverter(df2.date.max()),
                                                        step= 86400,
                                                        value= timeConverter(df2.date.max()),
                                                        updatemode="drag",
                                                        id="slider-county",
                                                        className="mt-0 mb-0 py-0"
                                                    )
                                                ],
                                                className="mt-0 mb-0 py-3",
                                            ),
                                        ),
                                        width=9,
                                        className="my-0"
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.P(id="slideDate-county", style={"fontSize":"12px", "text-align": "center"}, className="my-0")
                                                ],
                                                className="mt-0 mb-0 py-3"
                                            ),
                                        ),
                                        width=3,
                                        className="my-0"
                                    )
                                ]
                            )
                        )
                    )],
                    width=8
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(id='datatable-county')
                            ],
                            style={'overflowY':'scroll', 'overflowX':'hidden','height': '495px'}
                        ),
                    ), 
                    width=2
                )
            ]
        ),
        html.Div(id="Graphs-county", children=[
            dbc.Card(
                [
                    dbc.CardBody(
                        html.H4("General Information"),
                        className="p-0"
                    ),
                ],
                style={
                    "textAlign":"center"
                },
                className="my-4 p-2"
            ),
            dbc.Row(
                [
                    countyGraphObject(["cases","deaths"], ["Total Cases", "Total Deaths"], 1, 2, 500),                        
                ]
            ),
        ])
    ]
)

college_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P(get_news())
                            ]
                        ),
                    ),
                    width=3,
                    style={
                        'height': '495px',
                        "overflowY": "scroll"
                    }
                ),
                dbc.Col(
                    [
                        html.Div(
                            dbc.Row(
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                collegeMap()
                                            ],
                                            id = "college-map"
                                        ),
                                    )
                                )
                            ),
                            className="mb-3",
                        ),
                    ],
                    width=9
                )
            ]
        )
    
    ]
)


@app.callback(Output("slideDate", "children"),[Input("slider","value")])
def printDate(value):
    return timeC(value)

@app.callback(Output("slideDate-county", "children"),[Input("slider-county","value")])
def printCountyDate(value1):
    return timeC(value1)

@cache.memoize(timeout=TIMEOUT)
@app.callback(Output("state-map", "children"), [Input("searchBar", "value"), Input("slider","value")])
def figure(value, d):
    d = int(datetime.datetime.fromtimestamp(d).strftime("%Y%m%d"))
    data = df.loc[df['date'] == d][['date', 'state', value]]
    data['state'] = data['state'].map(states)
    with open('us-states.json') as json_file:
        geo = json.load(json_file)

    fig = go.Figure(go.Choroplethmapbox(geojson=geo, locations=data.state, z=data[value],
                                        colorscale="algae",marker_line_width=0.5))
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token,
                    mapbox_zoom=3.1, mapbox_center = {"lat": 39.82, "lon": -96})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='#303030', plot_bgcolor='#303030', font={'color': '#d3d3d3'})

    return dcc.Graph(figure=fig)

@cache.memoize(timeout=TIMEOUT)
@app.callback(Output("county-map", "children"), [Input("searchBar-county", "value"), Input("slider-county","value")])
def countyFigure(value1, d1):
    d1 = int(datetime.datetime.fromtimestamp(d1).strftime("%Y%m%d"))
    with urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as response:
        counties = json.load(response)


    data2 = df2.loc[df2['date'] == d1]  
    fig2 = go.Figure(go.Choroplethmapbox(geojson=counties, locations=data2.fips, z=data2[value1], text=data2.county,
    hovertemplate = '<b>County: </b> <b>%{text}</b>'+
                                                '<br><b>' + value1 + ': </b> %{z}<br>' +
                                                '<extra></extra>', 
                                            colorscale="algae",marker_line_width=0.5))
    fig2.update_layout(mapbox_style="dark", mapbox_accesstoken=token,
                    mapbox_zoom=3.1, mapbox_center = {"lat": 39.82, "lon": -96})
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor='#303030', plot_bgcolor='#303030', font={'color': '#d3d3d3'}, )
    fig2.update_traces(showscale=False)
    return dcc.Graph(figure = fig2)


@app.callback(Output("content", "children"), [Input("tabs", "value")])
def switch_tab(at):
    if at == "state-tab":
        return state_content
    elif at == "county-tab":
        return county_content
    elif at == "college-tab":
        return college_content
    return html.P("This shouldn't ever be displayed...")

@cache.memoize(timeout=TIMEOUT)
@app.callback(Output("datatable", "children"), [Input("searchBar", "value"), Input("slider","value")])
def figureDatatable(value, d):
    d = int(datetime.datetime.fromtimestamp(d).strftime("%Y%m%d"))
    df = pd.read_csv("https://api.covidtracking.com/v1/states/daily.csv", dtype={"fips": str})
    Input("slider","value")
    data = df.loc[df['date'] == d][['state', value]]
    return dt.DataTable(
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        style_cell={"backgroundColor":"#303030", "textAlign":"center"},
        style_data_conditional=[{"if":{"state":"active"}, "backgroundColor":"#222", "border":"3px solid #222"}]
    )

@cache.memoize(timeout=TIMEOUT)
@app.callback(Output("datatable-county", "children"), [Input("searchBar-county", "value"), Input("slider-county","value")])
def countyDatatable(value1, d1):
    d1 = int(datetime.datetime.fromtimestamp(d1).strftime("%Y%m%d"))
    Input("slider","value")
    data2 = df2.loc[df2['date'] == d1][['state', value1]]
    return dt.DataTable(
        columns=[{"name": i, "id": i} for i in data2.columns],
        data=data2.to_dict('records'),
        style_cell={"backgroundColor":"#303030", "textAlign":"center"},
        style_data_conditional=[{"if":{"state":"active"}, "backgroundColor":"#222", "border":"3px solid #222"}]
    )


# Define the app
app.layout = html.Div([
    html.Div([html.H2("Mask On")], id="title", className="mt-0 mb-3",style={"textAlign": "center", "font-family": "courier new"}),
    html.Div([
        tabs,
        html.Div(id="content")
    ],id="MapSection", className="w-100",style={"align":"center"})
], style={"margin": "auto", "width": "100%","padding": "20px", "align":"center"})



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
