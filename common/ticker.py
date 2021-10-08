import requests


def _parse_yahoo_data(quote_data):
    yahoo_data = quote_data.get('quoteResponse', {}).get('result', [{}])
    try:
        symbol, prevClose = yahoo_data['symbol'], yahoo_data['regularMarketPreviousClose']
        return symbol, prevClose
    except:
        return None, None


def get_ticker_price(ticker):
    url = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com"
    r = requests.get(
        url,
        params={'symbols': ticker},
        headers={
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36"
        }
    )
    return _parse_yahoo_data(r.json())
