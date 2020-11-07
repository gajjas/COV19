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

# Components
from assets.components.tabs import tabs

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

# Initialise the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

state_content = html.Div([
    html.Div([
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                            {'label': 'Confirmed Deaths', 'value': 'deathConfirmed'},
                            {'label': 'Cases', 'value': 'positiveIncrease'},
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
                            html.H1("NEWS")
                        ]
                    ),
                ),
                width=2
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(id = "state-map"),
                )
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H1("TABLE")
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


@app.callback(Output("state-map", "children"), [Input("searchBar", "value")])
def figure(value):
    df = pd.read_csv("https://api.covidtracking.com/v1/states/daily.csv", dtype={"fips": str})
    data = df.loc[df['date'] == 20201106][['date', 'state', value]]
    data['state'] = data['state'].map(states)
    data = data.drop([3, 8, 12, 27, 42, 50]).reset_index(drop=True)
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