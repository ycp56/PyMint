from dash import dcc
from dash import html
import plotly.graph_objs as go

from utils import Header, make_dash_table

import pandas as pd
import pathlib


def create_layout(data, app):
    # Page layouts
    bank_data = data['bank_data']['summary']
    brokerage_data = data['brokerage_data']['summary']
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 4: Bank Trend
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Trend",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=bank_data['date'],
                                                    y=(-1.0) * \
                                                    bank_data['spending'],
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
                                                    x=bank_data['date'],
                                                    y=bank_data['income'],
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
                                                    x=bank_data['date'],
                                                    y=bank_data['cashflow'],
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
                                                    "r": 0,
                                                    "t": 20,
                                                    "b": 10,
                                                    "l": 10,
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
                    # Row 5: Investment
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Investment Price & Performance",
                                        className="subtitle padded",
                                    ),
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
