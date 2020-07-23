# Basics Requirements
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

# Recall app
from app import app
from library import def_data

# ------------------------------
# CONTENTS
# 1. Sidebar style
# 2. SQL queries
# 3. Accordion
# ------------------------------

# ------------------------------
# 1. SIDEBAR STYLE
# ------------------------------
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": '140px',
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# ------------------------------
# 2. SQL queries
# ------------------------------
# 2.1 Query variables
df_vars = def_data.runQuery("""select * from public.var_definition order by group_id;""")

# ------------------------------
# 3. Accordion
# ------------------------------
var_groups = list(df_vars['group_id'].unique())
cardBody = []
for gr in var_groups:
    tempCardBody = []
    options = []
    for var_id in df_vars[df_vars['group_id'] == gr]['var_id']:
        options.append( {'label': '  ' + list(df_vars[df_vars['var_id']==str(var_id)]['label'])[0], 'value': str(var_id)} )
    tempCardBody.append(dbc.CardBody(dcc.Checklist(options=options,style={"font-size": "small"}),style={'height': '200px', 'overflowY': 'auto'}))
    cardBody.insert(gr, tempCardBody)

def make_item(i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H6(
                    dbc.Button(
                        list(df_vars[df_vars['group_id']==i]['group'].unique())[0],
                        color="link",
                        id=f"group-{i}-toggle", size="sm" #,block=True
                    )
                ),style={"height":"30px","padding": "0","margin": "0"}
            ),
            dbc.Collapse(
                cardBody[i-1],
                id=f"collapse-{i}",
            ),
        ]
    )

accordion_items = []
for gr in var_groups:
    accordion_items.append(make_item(gr))

accordion = html.Div(
    accordion_items, className="accordion"
)

# ------------------------------
# 3.1 Accordion Callbacks
# ------------------------------
@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in var_groups],
    [Input(f"group-{i}-toggle", "n_clicks") for i in var_groups],
    [State(f"collapse-{i}", "is_open") for i in var_groups],
)
def toggle_accordion(*args):
    ctx = dash.callback_context

    n = args[0:int(len(args)/2)]
    n = list(n)
    is_open = args[int(len(args)/2):]
    for i in range(len(n)):
        if n[i] is None:
            n[i] = 0

    if not ctx.triggered:
        return [False for i in var_groups]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    toggle = [False for i in range(len(is_open))]
    for i in var_groups:
        if button_id == 'group-' + str(i) + '-toggle': # and n[i]:
            toggle[i-1] = not is_open[i-1]
    return toggle


# ------------------------------
# SIDEBAR LAYOUT
# ------------------------------
area_drop = dcc.Dropdown(
    options=[
        {'label': 'Andina', 'value': 'Andina'},
        {'label': 'Amazónica', 'value': 'Amazónica'},
        {'label': 'Caribe', 'value': 'Caribe'},
        {'label': 'Orinoquía', 'value': 'Orinoquía'},
        {'label': 'Pacífica', 'value': 'Pacífica'}
    ],
    value='Andina'
)

# ------------------------------
# SIDEBAR LAYOUT
# ------------------------------

sidebar = html.Div(
    [
        dbc.Button("Run DEA", block=True, color='primary'), #style={"background-color":"#011f4b"}
        html.P('Instrucciones?'),
        html.Hr(),
        area_drop,
        html.Hr(),
        accordion,
    ],
    style=SIDEBAR_STYLE,
)