#Basics Requirements
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

#Recall app
from app import app
from library import maps, statistics, clustering, benchmarking



tab_bar = html.Div(className="tab-bar",
    children=[
        dbc.Tabs(
            [
                dbc.Tab(label="General", tab_id="tab-1"),
                dbc.Tab(label="Mapas", tab_id="tab-2"),
                dbc.Tab(label="Estadísticas", tab_id="tab-3"),
                dbc.Tab(label="Clustering", tab_id="tab-4"),
                dbc.Tab(label="Benchmarking", tab_id="tab-5"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return html.P('Tab1')
    elif at == "tab-2":
        return maps.map
    elif at == "tab-3":
        return statistics.statistics
    elif at == "tab-4":
        return clustering.clustering
    elif at == "tab-5":
        return benchmarking.benchmarking
    return html.P("This shouldn't ever be displayed...")