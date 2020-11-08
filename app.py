import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table as dt
from dash.dependencies import Input, Output
token = 'pk.eyJ1IjoiYmlnYm9iYnkxMjMiLCJhIjoiY2toN3NmbGsyMGZ4ODJ5cjdiZjAwaXB4NiJ9.3dwyhMsg_ed5AL2jictDnQ'
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go
import requests
import datetime
import time

# Components
from assets.components.tabs import tabs

df = pd.read_csv("https://api.covidtracking.com/v1/states/daily.csv", dtype={"fips": str})

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

# def getMarks(minUnix, maxUnix):
#     for i, date

# Initialise the app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/darkly/bootstrap.min.css"])

state_content = html.Div([
    html.Div([
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
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
                        id = "searchBar"
                    ),
                    width={"size": 6, "offset": 3}
                ),
            )
        ],
        className="mb-3"
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P("NEWS", id='news')
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
                                                html.P(id="slideDate", style={"fontSize":"12px"}, className="my-0")
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
                        ]
                    ),
                ), 
                width=2
            )
        ]
    )
    ]
)

county_content = dbc.Card(
    dbc.CardBody(
        [
        ]
    ),
    className="w-100",
)

@app.callback(Output("slideDate", "children"),[Input("slider","value")])
def printDate(value):
    return timeC(value)

@app.callback(Output("state-map", "children"), [Input("searchBar", "value"), Input("slider","value")])
def figure(value, d):
    d = int(datetime.datetime.fromtimestamp(d).strftime("%Y%m%d"))
    data = df.loc[df['date'] == d][['date', 'state', value]]
    data['state'] = data['state'].map(states)
    with open('us-states.json') as json_file:
        geo = json.load(json_file)

    fig = go.Figure(go.Choroplethmapbox(geojson=geo, locations=data.state, z=data[value],
                                        colorscale="reds",marker_line_width=0.5))
    fig.update_layout(mapbox_style="light", mapbox_accesstoken=token,
                    mapbox_zoom=3.1, mapbox_center = {"lat": 39.82, "lon": -96})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return dcc.Graph(figure=fig)


@app.callback(Output("content", "children"), [Input("tabs", "value")])
def switch_tab(at):
    if at == "state-tab":
        return state_content
    elif at == "county-tab":
        return county_content
    return html.P("This shouldn't ever be displayed...")

@app.callback(Output("datatable", "children"), [Input("searchBar", "value"), Input("slider","value")])
def figureDatatable(value, d):
    d = int(datetime.datetime.fromtimestamp(d).strftime("%Y%m%d"))
    df = pd.read_csv("https://api.covidtracking.com/v1/states/daily.csv", dtype={"fips": str})
    Input("slider","value")
    data = df.loc[df['date'] == d][['state', value]]
    return dbc.Table.from_dataframe(data, striped=True, bordered=True, hover=True)

@app.callback(Output("news", "children"), [Input("tabs", "value")])
def get_news(state=''):
    apikey = 'DlpBuDZRNirtABswzICFiQAFiTMWlobU'
    search = state + 'covid'
    query_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=headline:('coronavirus')&api-key={apikey}&sort=newest"

    data = requests.get(query_url).json()['response']['docs']
    news = []
    for article in data:
        news.append([article['headline']['main'], article['web_url']])
    return [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P(x[0]),
                    html.A(children='Source: NYTimes', id='link',
                    href=x[1], target='_blank'),
                ]
            )) for x in news]

# Define the app
app.layout = html.Div([
    html.Div([html.H2("Cov Data")], id="title", className="mt-0",style={"textAlign": "center"}),
    html.Div([
        tabs,
        html.Div(id="content")
    ],id="MapSection", className="w-100",style={"align":"center"})
], style={"margin": "auto", "width": "100%","padding": "20px", "align":"center"})



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)