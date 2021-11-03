from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

from utils import Header, make_dash_table


def create_layout(data, app):
    # Page layouts
    bank_data = data['bank_data']['summary']
    card_data = -1.0*data['card_data']['summary'].round(decimals=2)
    card_data_by_category = card_data.rename_axis(['date', 'category']).unstack(
        level=['category']).reset_index().fillna(0.).astype({'date': str})

    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 1: Bank Trend
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

                    # Row 2: Category
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Spending By Category",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",
                                        figure=px.pie(
                                            card_data.groupby('category').sum().reset_index(),
                                            names='category',
                                            values='spending'
                                            )
                                    ),

                                    html.Table(
                                        make_dash_table(card_data_by_category)),

                                ],
                                className="twelve columns",
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
