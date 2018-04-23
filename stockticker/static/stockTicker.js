// stockTicker.js:
// Holds methods and fields used for processing ticker data
// for the stockTicker app

var stockTicker = {

    // incremental counter, used to uniquely identify a set of ticker requests
    _overallCounter: 0,
    tickerQueryUrl: null,

    _divIdForTicker: function(ticker) {
        // Returns the div identifier used to hold results for a single ticker
        return 'result-' + ticker + '-' + this._overallCounter;
    },
    tickerQueryCallback: function(data) {
        // Callback to handle the data returned form a server for a single
        // ticker
        if (data.counter !== stockTicker._overallCounter) { return; }
        $('#' + stockTicker._divIdForTicker(data.ticker)).html(data.div);
        $('head').append(data.script);
    },
    processTickers: function(tickers) {
        // Main entry point. Takes the list of tickers, and makes some
        // HTTP requests for the data
        if (!tickers) {
            return;
        }

        this._overallCounter += 1;

        var innerHtml = "";

        var i;
        for (i = 0; i < tickers.length; i++) {
            ticker = tickers[i].ticker;
            innerHtml += '<h3>' + ticker + '</h3>';
            innerHtml += '<div id="' + this._divIdForTicker(ticker) +
                '">Loading...</div>';
            $.getJSON(this.tickerQueryUrl,
                      { ticker: ticker, counter: this._overallCounter },
                      this.tickerQueryCallback);
        }

        $('#results').html(innerHtml);
    },
    onSubmitClick: function() {
        //Handle the click of the submit button
        var tickerString = $('input#tickers').val();
        if (!tickerString) { return; }

        var tickerArray = tickerString.split(",");
        var tickers = [];

        var i;
        for (i = 0 ; i < tickerArray.length; i++) {
            tickers.push({"ticker": tickerArray[i].trim()});
        }

        stockTicker.processTickers(tickers);
    }
};

$(function() {
    $('input#search').bind('click', stockTicker.onSubmitClick);
});
