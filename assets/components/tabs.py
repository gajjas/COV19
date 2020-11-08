import dash_html_components as html
import dash_core_components as dcc

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'background-color': '#303030',
    'border-color': '#303030'

}

tab_selected_style = {
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#54B98F',
    'color': '#222',
    'padding': '6px',
    'border-color': '#303030'
}

tabs = html.Div(
    [
        dcc.Tabs(
            [
                dcc.Tab(label="State", style=tab_style, selected_style=tab_selected_style, value="state-tab"),
                dcc.Tab(label="County", style=tab_style, selected_style=tab_selected_style, value="county-tab"),
                dcc.Tab(label="College", style=tab_style, selected_style=tab_selected_style, value="college-tab"),
                # dcc.Tab(label="Info", style=tab_style, selected_style=tab_selected_style, value="info-tab")
            ],
            id = "tabs",
            value="state-tab",
            style=tabs_styles
        ) 
    ],
    className="mb-3"
)