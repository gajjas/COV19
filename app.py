import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output

# Initialise the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Tab 1", tab_id="tab-1"),
                dbc.Tab(label="Tab 2", tab_id="tab-2"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    return html.P("This shouldn't ever be displayed...")

# Define the app
app.layout = html.Div([
    html.Div("Cov Data", id="title"),
    html.Div([
        tabs

    ],id="MapSection"),
    html.Div([],id="generic-section"),
    html.Div([],id="hospital-div")
], style={"margin": "auto", "width": "50%","padding": "10px"})



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    token = 'pk.eyJ1IjoiYmlnYm9iYnkxMjMiLCJhIjoiY2toN3NmbGsyMGZ4ODJ5cjdiZjAwaXB4NiJ9.3dwyhMsg_ed5AL2jictDnQ'
import pandas as pd
import plotly.express as px
import json

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




df = pd.read_csv("./all-states-history.csv", dtype={"fips": str})
death_data = df.loc[df['date'] == '2020-11-06'][['date', 'state', 'death']]
death_data['state'] = death_data['state'].map(states)
print(death_data)


with open('us-states.json') as json_file:
    data = json.load(json_file)

import plotly.graph_objects as go

fig = go.Figure(go.Choroplethmapbox(geojson=data, locations=death_data.state, z=death_data.death,
                                    colorscale="blues",marker_line_width=0))
fig.update_layout(mapbox_style="light", mapbox_accesstoken=token,
                  mapbox_zoom=4, mapbox_center = {"lat": 39.82, "lon": -98.58})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
