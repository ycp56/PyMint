import requests


def _parse_yahoo_data(yahoo_json, type='last'):
    if type == 'last':
        try:
            yahoo_data = yahoo_json.get('quoteResponse', {}).get('result', [{}])[0]
            symbol, prevClose = yahoo_data['symbol'], yahoo_data['regularMarketPreviousClose']
            return symbol, None, prevClose
        except:
            return None, None, None
    elif type == 'history':
        try:
            yahoo_data = yahoo_json.get('chart', {}).get('result', [{}])[0]
            symbol = yahoo_data['meta']['symbol']
            timestamp = yahoo_data['timestamp']
            adjclose = yahoo_data['indicators']['adjclose'][0]['adjclose']
            return symbol, timestamp, adjclose
        except:
            return None, None, None
    else:
        raise ValueError('Unknown type!')


def get_prev_close(ticker):
    url = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com"
    r = requests.get(
        url,
        params={'symbols': ticker},
        headers={
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36"
        }
    )
    return _parse_yahoo_data(r.json(), type='last')


def get_price_history(ticker, interval='1d', range='6mo'):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    r = requests.get(
        url,
        params={
            'interval': interval,
            'range': range,
            'events': "div,splits"
            },
        headers={
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36"
        }
        )
    return _parse_yahoo_data(r.json(), type='history')
