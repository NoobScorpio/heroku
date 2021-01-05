import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dbm
import plotly.graph_objs as go
import re
import dash
import dash_bootstrap_components as dbc
from APIS import invoices
# from APIS import items
from APIS import payments
# from APIS import reports
# from APIS import taxRate
import traceback
# Set up the app
FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FA])
server = app.server


def errorMessage():
    return [dbc.Col(
        [
            html.I(className="far fa-window-close fa-3x",style={'color':'red '}),
            html.H5('This Chart cannot be generated due to inaccurate data'),
        ],
        style={ 
        'margin': 'auto',
        'width': '100%',
        'background-color': 'white',
        'padding': '10px',
        'text-align':'center'
        }),
        ]

def invoicesCall():
    try:
        return invoices.init()
    except Exception as e:
        print(e)
        traceback.print_exc()
        return errorMessage()

def itemsCall():
    try:
        return items.init()
    except Exception as e:
        print(e)
        traceback.print_exc()
        return errorMessage()

def paymentsCall():
    try:
        return payments.init()
       
    except Exception as e:
        print(e)
        traceback.print_exc()
        return errorMessage()

def reportsCall():
    try:
        return reports.init()
       
    except Exception as e:
        print(e)
        traceback.print_exc()
        return errorMessage()

def taxCall():
    try:
        return taxRate.init()
       
    except Exception as e:
        print(e)
        traceback.print_exc()
        return errorMessage()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):

    if pathname == '/':
        return html.Div([
            dbc.Navbar(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.I(className="fas fa-chart-bar fa-4x", style={'color': 'white'})),
                            dbc.Col(dbc.NavbarBrand("Bi Dashboard", className="ml-1",
                                                    style={'font-size': '22px', 'font-weight': 'bold'})),
                        ],
                        align="center",
                        no_gutters=True,
                    ),

                ],
                color="black",
                dark=True,
            ),
            
            dbc.Row([html.Div(
                invoicesCall(),
                className="p-3 col col-sm-12 col-md-6 col-lg-4"),

            html.Div(
                itemsCall(),
                className="p-3 col col-sm-12 col-md-6 col-lg-4"),

            html.Div(
                paymentsCall(),
                className="p-3 col col-sm-12 col-md-6 col-lg-4")]),

            

            dbc.Row([
                html.Div(
                reportsCall(),
            className="p-3 col col-sm-12 col-md-6 col-lg-4"),
            html.Div(
                taxCall(),
                className="p-3 col col-sm-12 col-md-6 col-lg-4"),
                html.Div(
                reportsCall(),
            className="p-3 col col-sm-12 col-md-6 col-lg-4"),])
        ],style={'background-color':'#DCDCDF','height':'100%'})


if __name__ == '__main__':
    app.run_server(debug=False,port=5000,host="0.0.0.0")
