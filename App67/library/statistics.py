import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go

from app import app
from library.elements_all import dropdown

import plotly.express as px
from plotly.subplots import make_subplots

##############################
# Load Data
##############################
df_all = pd.read_csv('data/df_all.csv')


def get_desercion_variables(df_in, year, in_mun_code):
    df_filtered = df_in[df_in['code_municip'] == in_mun_code]
    df_year = df_filtered[df_filtered['year_cohort'] == year]

    # desercion
    tempval = df_year['desertion_perc'].to_numpy()[0]
    value_desercion = str(np.round(tempval, 2)) + ' %'
    y_plot = df_year[[
        'me_desercion_transicion',
        'me_desercion_primaria',
        'me_desercion_media',
        'me_desercion_secundaria',
    ]].to_numpy()

    derc_perc = [np.round(x * tempval / sum(y_plot[0]), 2) for x in y_plot[0]]

    return value_desercion, derc_perc


def get_cobertura_variables(df_in, year, in_mun_code):
    df_filtered = df_in[df_in['code_municip'] == in_mun_code]
    df_year = df_filtered[df_filtered['year_cohort'] == year]
    # cobertura
    tempval_2 = df_year['me_cobertura_neta'].to_numpy()[0]
    value_cobertura = str(np.round(tempval_2, 2)) + ' %'
    y_plot_2 = df_year[[
        'me_cobertura_neta_transicion',
        'me_cobertura_neta_primaria',
        'me_cobertura_neta_media',
        'me_cobertura_neta_secundaria',
    ]].to_numpy()
    cob_perc = y_plot_2[0]
    return cob_perc


def get_scatter_df(df_in, var1, var2, year):
    df_year = df_in[df_in['year_cohort'] == year]
    df_final = df_year[[var1, var2, 'name_dept', 'code_dept', 'name_municip', 'code_municip', 'region']]

    var1 = 'desertion_perc'
    var2 = 'me_tasa_matriculacion_5_16'
    scatter_df = get_scatter_df(df_all, var1, var2, 2019)

    region_to_number = {
        'Andina': 1,
        'Caribe': 2,
        'Amazonica': 3,
        'Pacifica': 4,
        'Orinoquia': 5,
    }

    def change_to_code(region):
        return region_to_number[region]

    scatter_df['reg_code'] = scatter_df['region'].apply(change_to_code)

    return scatter_df


def make_donut_desertion_fig(name_municipio, name_depto, year, label_desercion, derc_perc):
    labels = ['Transición', 'Primaria', 'Media', 'Secundaria']
    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=derc_perc,
                                 hole=.5,
                                 hoverinfo="label+value"
                                 )
                                 ])
    fig.update_layout(title_text="Deserción Total Población Escolar: " + label_desercion)
    return fig


def make_bar_cobertura_fig(name_municipio, name_depto, cob_perc):
    labels = ['Transición', 'Primaria', 'Media', 'Secundaria']
    fig = go.Figure(data=[go.Bar(x=labels,
                                 y=cob_perc,
                                 )])
    fig.update_layout(title_text="Cobertura Total Población Escolar: " )
    return fig


def figure_desertion_year(df_all, selected_code):
    df_mun = df_all[df_all['code_municip'] == selected_code]
    result_fig = go.Figure(data=go.Scatter(x=df_mun['year_cohort'],
                                           y=df_mun['desertion_perc']
                                           ),
                           )

    result_fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    result_fig.update_layout(title_text="Deserción 2011-2019")

    return result_fig


def make_correlation_fig(scatter_df):
    figure_t = go.Figure(data=go.Scatter(
        x=scatter_df['desertion_perc'],
        y=scatter_df['me_tasa_matriculacion_5_16'],
        text=scatter_df['region'] + ' - ' + scatter_df['name_dept'] + ' - ' + scatter_df['name_municip'],
        mode='markers',
            marker=dict(
                size=16,
                color=scatter_df['reg_code'],  # set color equal to a variable
                colorscale='Jet',  # one of plotly colorscales
                showscale=False
            )
            ))
    figure_t.update_layout(title='Population of USA States')
    return figure_t


##### Call Figures

selected_code = 5001

selected_year = 2019

df_mun = df_all[df_all['code_municip'] == selected_code]
name_municipio = df_mun.iloc[[0]]['name_dept'].to_numpy()
name_depto = df_mun.iloc[[0]]['name_municip'].to_numpy()

label_desercion, derc_perc = get_desercion_variables(
    df_in=df_all,
    year=selected_year,
    in_mun_code=selected_code,
)

cob_perc = get_cobertura_variables(
    df_in=df_all,
    year=selected_year,
    in_mun_code=selected_code,
)

# var1 = 'desertion_perc'
# var2 = 'me_tasa_matriculacion_5_16'
# scatter_df = get_scatter_df(df_all, var1, var2, 2019)
# Corr_fig = make_correlation_fig(scatter_df)

PieFig = make_donut_desertion_fig(
    name_municipio=name_municipio,
    name_depto=name_depto,
    year=selected_year,
    label_desercion=label_desercion,
    derc_perc=derc_perc,
)

BarFig = make_bar_cobertura_fig(
    name_municipio=name_municipio,
    name_depto=name_depto,
    cob_perc=cob_perc,
    # value_cobertura=value_cobertura
)

Years_fig = figure_desertion_year(
    df_all=df_all,
    selected_code=selected_code
)

##############################
# Layout
##############################

explore_municipio = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H3(""),
                    align="start",
                    width=2
                ),
                dbc.Col(
                    html.H3("Explorar Deserción y Cobertura por Municipio"),
                    align="center",
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div(dropdown.dropdown_year), width=2
                ),
                dbc.Col(
                    dcc.Graph(figure=PieFig, id='Pie_d'), width=3
                ),
                dbc.Col(
                    dcc.Graph(figure=Years_fig, id='Years_d'), width=4
                ),
                dbc.Col(
                    dcc.Graph(figure=BarFig, id='Bar_c'), width=3
                ),
            ],
            align="center",
        ),
    ]
)

explore_correlation = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H3(""),
                    align="start",
                    width=2
                ),
                dbc.Col(
                    html.H3("Explorar Correlación entre Variables"),
                    align="start",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(""), width=1
                ),
                dbc.Col(
                    html.Div("Dropdown Select Variables"), width=1
                ),
                dbc.Col(
                    dcc.Graph(figure=Years_fig, id='Years2'), width=10
                ),
            ],
            align="center",
        ),
    ]
)


dbc.Col(html.Div("One of three columns"), width=3),
statistics = html.Div(
    [
        dbc.Row(
            explore_correlation
        ),

        dbc.Row(dbc.Col(
            html.Div("")
        )),

        dbc.Button(
            "Explorar Deserción y Cobertura por Municipio",
            id="collapse-button",
            className="mb-3",
            color="secondary",
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody(
                explore_municipio
            )),
            id="collapse",
        ),

    ]
)


##############################
# Callbacks
##############################


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



