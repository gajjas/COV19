import dash
import dash_html_components as html

# Initialise the app
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div(

)



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
