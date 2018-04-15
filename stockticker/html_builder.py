"""HTML/JavaScript creation for Stock Ticker App"""

def _div_id(ticker):
    """Return the div ID for the given ticker"""
    return "result_{0}".format(ticker)

def _get_js_for_ticker(ticker, ticker_handler_url):
    """Create the JavaScript to get the results for a single ticker.
    The JavaScript calls out to /_handle_ticker and places the results in
    the appropriate result div. Lervaging jQuery, the script doesn't
    run until the page loads"""

    js_builder = []
    js_builder.append("$(function() {")
    js_builder.append("$.getJSON('" + ticker_handler_url + "', ")
    js_builder.append("{ ticker: '" + ticker + "' }, ")
    js_builder.append("function(data) {")
    js_builder.append("$('#" + _div_id(ticker) + "').html(data.div);")
    js_builder.append("$('head').append(data.script);})});")
    return ''.join(js_builder)

def _get_js_for_ticker_list(tickers, ticker_handler_url):
    """Create the JavaScript that fetches results for all
    of the passed in tickers"""

    js_builder = ["<script type=text/javascript>"]
    for ticker in tickers:
        js_builder.append(_get_js_for_ticker(ticker, ticker_handler_url))
    js_builder.append('</script>')

    return ' '.join(js_builder)

def _get_result_divs(tickers):
    """Create the divs that hold the Bokeh plots"""
    div_builder = ["<div id=results>"]
    for ticker in tickers:
        div_builder.append("<span><h3>{0}</h3></span>".format(ticker))
        div_builder.append("<div id={0}>{1}</div>".format(_div_id(ticker),
                                                          "Downloading..."))
    div_builder.append("</div>")

    return ''.join(div_builder)


def get_html(tickers, ticker_handler_url):
    """Create the HTML and jQuery script to add to the application"""

    return (_get_js_for_ticker_list(tickers, ticker_handler_url),
            _get_result_divs(tickers))
