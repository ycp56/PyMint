# -*- coding: utf-8 -*-
import dash
import webbrowser

from threading import Timer
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from pages import (
    overview,
    creditcard
)


from common.utils import (
    get_brokerage_account, 
    get_bank_account, 
    get_card_account, 
    bank_summary,
    brokerage_summary,
    card_summary,
    portfolio_trend
)

from config import bank_config, brokerage_config, card_config
data = {
    'bank_data':{
        'summary': bank_summary(get_bank_account(bank_config)),
        'daily_summary': bank_summary(get_bank_account(bank_config), freq='D'),
        },
    'brokerage_data': {
        'summary': brokerage_summary(get_brokerage_account(brokerage_config)),
        'trend': portfolio_trend(get_brokerage_account(brokerage_config))
    },
    'card_data':{
        'summary': card_summary(get_card_account(card_config))
        },

    }

# -----------------------------------------------------------------------------
#                Main server
# -----------------------------------------------------------------------------
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Financial Report"
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/financial-report/credit-card":
        return creditcard.create_layout(data, app) 
    else:
        return overview.create_layout(data, app)

def open_browser(port=1234):
	webbrowser.open_new("http://localhost:{}".format(port))

if __name__ == "__main__":
    Timer(1, open_browser).start();
    app.run_server(debug=False, port=1234)
