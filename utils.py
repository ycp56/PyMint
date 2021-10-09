from dash import dcc
from dash import html


def Header(app):
    return html.Div([get_header(app), html.Br([])])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Button("Source Code", id="learn-more-button"),
                        href="https://github.com/ycp56/PyMint",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Overview")],
                        className="seven columns main-title",
                    ),
               ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/dash-financial-report/overview",
                className="tab first",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    table.append(html.Tr([html.Td(col) for col in df.columns]))
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
