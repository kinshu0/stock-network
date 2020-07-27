import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from textwrap import dedent as d
import json

from webapp.back_end.graph_modeler import network_graph
from core_modules import client
# from graph_modeler import network_graph
# import client

from datetime import datetime as dt

# import the css template, and pass the css template into dash
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)
app.title = "Stock Correlation Network"

YEAR=[2010, 2019]
search="BAC"


# styles: for right side hover/click component
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    #########################Title
    html.Div([html.H1("Stock Network Graph")],
             className="row",
             style={'textAlign': "center"}),
    #############################################################################################define the row
    html.Div(
        className="row",
        children=[
            ##############################################left side two input components
            html.Div(
                className="two columns",
                children=[
                    # dcc.Markdown(d("""
                    #         **Time Range To Visualize**

                    #         Slide the bar to define year range.
                    #         """)),
                    dcc.Markdown(d("""
                            **Time Range To Visualize**

                            Slide the bar to define year range.
                            """)),
                    html.Div(
                        className="twelve columns",
                        children=[
                            dcc.RangeSlider(
                                id='my-range-slider',
                                min=2010,
                                max=2019,
                                step=1,
                                value=[2010, 2019],
                                marks={
                                    2010: {'label': '2010'},
                                    2011: {'label': '2011'},
                                    2012: {'label': '2012'},
                                    2013: {'label': '2013'},
                                    2014: {'label': '2014'},
                                    2015: {'label': '2015'},
                                    2016: {'label': '2016'},
                                    2017: {'label': '2017'},
                                    2018: {'label': '2018'},
                                    2019: {'label': '2019'}
                                }
                            ),
                            # dcc.DatePickerRange(
                            #     id='date-picker-range',
                            #     start_date=dt(2005, 1, 1),
                            #     end_date=dt.today()
                            # ),
                            html.Br(),
                            html.Div(id='output-container-range-slider')
                        ],
                        style={'height': '300px'}
                    ),
                    html.Div(
                        className="twelve columns",
                        children=[
                            dcc.Markdown(d("""
                            **Ticker To Search**

                            Input the Ticker to visualize.
                            """)),
                            dcc.Input(id="input1", type="text", placeholder="Ticker"),
                            html.Div(id="output")
                        ],
                        style={'height': '300px'}
                    )
                ]
            ),

            ############################################middle graph component
            html.Div(
                className="eight columns",
                children=[dcc.Graph(id="my-graph",
                                    figure=network_graph(YEAR, search))],
            ),

            #########################################right side two output component
            # html.Div(
            #     className="two columns",
            #     children=[
            #         html.Div(
            #             className='twelve columns',
            #             children=[
            #                 dcc.Markdown(d("""
            #                 **Hover Data**

            #                 Mouse over values in the graph.
            #                 """)),
            #                 html.Pre(id='hover-data', style=styles['pre'])
            #             ],
            #             style={'height': '400px'}),

            #         html.Div(
            #             className='twelve columns',
            #             children=[
            #                 dcc.Markdown(d("""
            #                 **Click Data**

            #                 Click on points in the graph.
            #                 """)),
            #                 html.Pre(id='click-data', style=styles['pre'])
            #             ],
            #             style={'height': '400px'})
            #     ]
            # )
        ]
    )
])

###################################callback for left side components
@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('my-range-slider', 'value'), dash.dependencies.Input('input1', 'value')])
    # dash.dependencies.Output('my-graph', 'figure'),
    # [
    #     # dash.dependencies.Input('my-range-slider', 'value'),
    #     dash.dependencies.Input('input1', 'value'),
    #     dash.dependencies.Input('date-picker-range', 'start_date'),
    #     dash.dependencies.Input('date-picker-range', 'end_date')
    # ])
def update_output(value, input1):
# def update_output(input1, start, end):
    YEAR = value
    # value = [start[:10].replace('-', ''), end[:10].replace('-', '')]

    search = input1
    return network_graph(value, input1)
    # to update the global variable of YEAR and search
################################callback for right side components



# @app.callback(
#     dash.dependencies.Output('hover-data', 'children'),
#     [dash.dependencies.Input('my-graph', 'hoverData')])

def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


# @app.callback(
#     dash.dependencies.Output('click-data', 'children'),
#     [dash.dependencies.Input('my-graph', 'clickData')])

def display_click_data(clickData):
    return json.dumps(clickData, indent=2)



if __name__ == '__main__':
    app.run_server(debug=True)
