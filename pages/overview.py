from dash import dcc
from dash import html
import plotly.graph_objs as go

from utils import Header, make_dash_table


def create_layout(data, app):
    # Page layouts
    bank_spending_data = data['bank_data']['summary']
    bank_balance_data = data['bank_data']['daily_summary']
    brokerage_data = data['brokerage_data']['summary']
    portfolio_trend = data['brokerage_data']['trend']
    return html.Div(
        [

            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 1:  Balance
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Bank Balance",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=bank_balance_data['date'],
                                                    y=bank_balance_data['balance'],
                                                    line={"color": "#97151c"},
                                                    mode="lines",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                bargap=0.35,
                                                font={
                                                    "family": "Raleway", "size": 10},
                                                height=200,
                                                width=700,
                                                hovermode="closest",
                                                margin={
                                                    "r": 50,
                                                    "t": 20,
                                                    "b": 20,
                                                    "l": 50,
                                                },
                                                showlegend=False,
                                                title="",
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [-0.5, 4.5],
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                    "tickmode": "linear",
                                                    "tick0": bank_balance_data['date'][10],
                                                    "dtick": 60,
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [0, 22.9789473684],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),


                    # Row 2: Spending 
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Cash Flow",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-2",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=bank_spending_data['date'],
                                                    y=(-1.0) * \
                                                    bank_spending_data['spending'],
                                                    marker={
                                                        "color": "#97151c",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="Spending",
                                                ),
                                                go.Bar(
                                                    x=bank_spending_data['date'],
                                                    y=bank_spending_data['income'],
                                                    marker={
                                                        "color": "#dddddd",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="Income",
                                                ),
                                                go.Bar(
                                                    x=bank_spending_data['date'],
                                                    y=bank_spending_data['cashflow'],
                                                    marker={
                                                        "color": "#856879",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="Cash Flow",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                bargap=0.35,
                                                font={
                                                    "family": "Raleway", "size": 10},
                                                height=200,
                                                width=700,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0228945952895,
                                                    "y": -0.189563896463,
                                                    "orientation": "h",
                                                    "yanchor": "top",
                                                },
                                                margin={
                                                    "r": 50,
                                                    "t": 20,
                                                    "b": 10,
                                                    "l": 50,
                                                },
                                                showlegend=True,
                                                title="",
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [-0.5, 4.5],
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [0, 22.9789473684],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),

                    # Row 2: Portfolio Historical data
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Investment", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-3",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=portfolio_trend['date'],
                                                    y=portfolio_trend['value'],
                                                    line={"color": "#97151c"},
                                                    mode="lines",
                                                    name="Portfolio Value",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                width=700,
                                                height=200,
                                                font={"family": "Raleway", "size": 10},
                                                margin={
                                                    "r": 30,
                                                    "t": 30,
                                                    "b": 30,
                                                    "l": 30,
                                                },
                                                showlegend=True,
                                                titlefont={
                                                    "family": "Raleway",
                                                    "size": 10,
                                                },
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        "2007-12-31",
                                                        "2018-03-06",
                                                    ],
                                                    "rangeselector": {
                                                        "buttons": [
                                                            {
                                                                "count": 1,
                                                                "label": "1M",
                                                                "step": "month",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "count": 3,
                                                                "label": "3M",
                                                                "step": "month",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "count": 6,
                                                                "label": "6M",
                                                                "step": "month",
                                                            },
                                                            {
                                                                "label": "All",
                                                                "step": "all",
                                                            },
                                                        ]
                                                    },
                                                    "rangeslider":{'visible': True},
                                                    "showline": True,
                                                    "type": "date",
                                                    "zeroline": False,
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "showline": True,
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    ),
 

                    # Row 2: Investment table
                    html.Div(
                        [
                            html.Div(
                                [
                                   html.Table(
                                        make_dash_table(brokerage_data)),
                                ],
                                className=" columns",
                            ),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
