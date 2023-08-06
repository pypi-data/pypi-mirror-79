

-------------



# finpie - a simple library to download some financial data

<p><b>For recreational and educational purposes. Creating easier access to some financial and economic data.</b></p>

<p>This library is an ongoing project designed to facilitate access to financial and economic data. It tries to cover potentially useful or interesting data points but unfortunately some functions will only return single point data which however could be aggregated over time to construct a limited time series. On the other hand, some functions that retrieve large amounts of data or depending on the data source will take some time to run. See the <a href="#A3">function index </a> for more information on issues of data availability and relative run time.</p> 

<p>The company fundamentals module includes functions to retrive data from <code>Yahoo Finance</code>, <code>MarketWatch</code>, <code>Finviz</code> and <code>Macrotrends</code>. The price data module retrieves data from <code>Yahoo Finance</code> and also includes a wrapper for price data APIs including <code>Alpha-Vantage</code>, <code>IEX Cloud</code> and <code>Tiingo</code> which require a (free) api-key from the respective provider. The economic data is solely pulled from the <code>OECD database</code> at this point and the news module enables historical news headline collection from the <code>FT</code>, <code>NYT</code>, <code>WSJ</code>, <code>Barrons</code>, <code>Seeking Alpha</code>, <code>Bloomberg</code> and <code>Reuters</code> based on keyword searches. The library also provides a function to get all Nasdaq-listed stock tickers as well as worldwide stock symbols (these need some cleaning still once retrieved).</p>


<p>If there are any issues, ideas or recommendations please feel free to reach out.</p>

<p>
<i>To do list:</i>
<ul>
<li> Create test file </li>
<li> Add an earnings transcript section </li>
<li> Add EIA and USDA data, CFTC COT and potentially add weather data sources (e.g. heating degree days, cooling degree days in NE US) </li>
<li> Add social media data (Twitter, Stocktwits, Weibo, Reddit WSB?) </li>
<li> Add async requests, multiple/batch download options, proxies.. </li>
</ul>
</p>

<br>

## <div id="0">Documentation</div>

<ol>
<li>
<a href="#A2">Installation</a>
</li>
<li><a href="#A3">Function index</a></li>
<li>
<a href="#A4">Company fundamental data</a><ul>
	<li><a href="#A41">Valuation metrics and financial ratios</a></li>
	<li><a href="#A42">Financial statements</a></li>
	<li><a href="#A43">Earnings and revenue estimates</a></li>
	<li><a href = "#A44">Insider transactions and analyst ratings</a></li>
	<li><a href = "#A46">ESG scores</a></li>
	<li><a href = "#A47">Company profile</a></li>
	</ul>
</li>
<li>
<a href="#A5">Price data</a><ul>
	<li><a href="#A51">Stock prices</a></li>
	<li><a href="#A52">Option prices</a></li>
	<li><a href="#A53">Futures prices</a></li>
	</ul>

</li>
<li><a href="#A6">Economic data</a></li>
<ul>
<li><a href = "#A61">OECD composite leading indicators</a></li>
<li><a href = "#A62">OECD business tendency survey</a></li>
<li><a href = "#A63">OECD main economic indicators</a></li>
<li><a href = "#A64">OECD balance of payment</a></li>

</ul>
<li><a href="#A7">News data</a></li>
<li><a href="#A8">Other data</a></li>
<li><a href="#A9">Sources</a></li>
<li><a href="#A10">License</a></li>
</ol>

## <div id="A2">Installation</div>

Python3 is required. Google Chrome version <code>84.\*.\*\*\*\*.\*\*\*</code> or higher is required for some functions involving Selenium (can be found <a href="https://chromereleases.googleblog.com/">here</a>). 

```python
$ pip install finpie
```
### Requirements

```
alpha_vantage>=2.1.0
beautifulsoup4>=4.9.1
iexfinance>=0.4.3
dask>=2.11.0
numpy>=1.18.2
pandas>=1.0.1
requests>=2.22.0
requests_html>=0.10.0
selenium>=3.141.0
tqdm>=4.32.1
```

<div align="right"><a href="#0">Back to top</a> </div>



## <div id="A3"> Index </div>

|Output|Data Output|Runtime|
|:-----|:-----|:-----:|
|<b>Company Fundamentals</b>|||
|<u>Valuation metrics and financial ratios</u>|||
|<li> <a id='i1' href='#f1'>yahoo.valuation\_metrics()</a> </li>|5 quarters|Fast|
|<li> <a id='i2' href='#f2'>yahoo.key_metrics()</a> </li>|Today's data|Fast|
|<li> <a id='i101' href='#f101'>finviz.key_metrics()</a> </li>|Today's data|Fast|
|<li> <a id='i102' href='#f102'>macrotrends.ratios()</a> </li>|up to 2005|Slow|
|<u>Financial statements</u>|||
|<li> <a id='i3' href='#f3'>yahoo.income\_statement()</a> </li>|4 years / quarters|Fast|
|<li> <a id='i4' href='#f4'>yahoo.balance\_sheet()</a> </li>|4 years / quarters|Fast|
|<li> <a id='i5' href='#f5'>yahoo.cashflow\_statement()</a> </li>|4 years / quarters|Fast|
|<li> <a id='i6' href='#f6'>yahoo.statements()</a> </li>|4 years / quarters|Fast|
|<li> <a id='i7' href='#f7'>mwatch.income\_statement()</a> </li>|5 years / quarters|Fast|
|<li> <a id='i8' href='#f8'>mwatch.balance\_sheet()</a> </li>|5 years / quarters|Fast|
|<li> <a id='i9' href='#f9'>mwatch.cashflow\_statement()</a> </li>|5 years / quarters|Fast|
|<li> <a id='i10' href='#f10'>mwatch.statements()</a> </li>|5 years / quarters|Fast|
|<li> <a id='i103' href='#f103'>macrotrends.income\_statement()</a> </li>|up to 2005|Slow|
|<li> <a id='i104' href='#f104'>macrotrends.balance\_sheet()</a> </li>|up to 2005|Slow|
|<li> <a id='i105' href='#f105'>macrotrends.cashflow\_statement()</a> </li>|up to 2005|Slow|
|<u>Earnings and revenue estimates</u>|||
|<li> <a id='i11' href='#f11'>yahoo.earnings\_estimates()</a> </li>|Today's data|Fast|
|<li> <a id='i12' href='#f12'>yahoo.earnings\_estimates\_trends()</a> </li>|Recent trend|Fast|
|<li> <a id='i13' href='#f13'>yahoo.earnings\_history()</a> </li>|4 quarters|Fast|
|<li> <a id='i14' href='#f14'>yahoo.revenue\_estimates()</a> </li>|Today's data|Fast|
|<li> <a id='i15' href='#f15'>yahoo.growth\_estimates()</a> </li>|Today's data|Fast|
|<u>Insider transactions and analyst ratings</u>|||
|<li> <a id='i16' href='#f16'>finviz.insider\_transactions()</a> </li>|Last year|Fast|
|<li> <a id='i17' href='#f17'>finviz.analyst\_ratings()</a> </li>|Most recent ratings|Fast|
|<u>ESG data</u>|||
|<li> <a id='i18' href='#f18'>yahoo.esg\_score()</a> </li>|Today's data|Fast|
|<li> <a id='i19' href='#f19'>yahoo.corporate\_governance\_score()</a> </li>|Today's data|Fast|
|<u>Company profile</u>|||
|<li> <a id='i20' href='#f20'>yahoo.profile()</a> </li>|Today's data|Fast|
|<li> <a id='i21' href='#f21'>yahoo.exceutives\_info()</a> </li>|Today's data|Fast|
|<b>Price data</b>|||
|<li> <a id='i22' href='#f22'>yahoo\_prices(ticker)</a> </li>|Timeseries|Fast|
|<li> <a id='i24' href='#f24'>alpha\_vantage\_prices(ticker,api\_token)</a> </li>|Timeseries|Fast|
|<li> <a id='i25' href='#f25'>iex_intraday(ticker, api\_token)</a> </li>|Timeseries|Depends on timeframe|
|<li> <a id='i26' href='#f26'>tingo\_prices(ticker, api\_token, start\_date, end\_date, freq)</a> </li>|Timeseries|Depends on timeframe|
|<li> <a id='i27' href='#f27'>yahoo\_option\_chain(ticker)</a> </li>|Today's data|Fast|
|<li> <a id='i28' href='#f28'>historical\_futures\_contracts(date\_range)</a> </li>|Timeseries|Very slow|
|<li> <a id='i29' href='#f29'>futures\_contracts(date)</a> </li>|Any date|Fast|
|<b>Economic data</b>|||
|<u>Composite leading indicators</u>|||
|<li> <a id='i30' href='#f30'>oecd.cli(subject = 'amplitude)</a> </li>|Timeseries|Not that slow|
|<li> <a id='i31' href='#f31'>oecd.cci()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i32' href='#f32'>oecd.bci()</a> </li>|Timeseries|Not that slow|
|<u>Financial indicators</u>|||
|<li> <a id='i33' href='#f33'>oecd.monetary\_aggregates\_m1()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i34' href='#f34'>oecd.monetary\_aggregates\_m3()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i35' href='#f35'>oecd.interbank\_rates()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i36' href='#f36'>oecd.short\_term\_rates()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i37' href='#f37'>oecd.long\_term\_rates()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i38' href='#f38'>oecd.all\_share\_prices( )</a> </li>|Timeseries|Not that slow|
|<li> <a id='i39' href='#f39'>oecd.share\_prices\_industrials()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i41' href='#f41'>oecd.usd\_exchange\_rates\_spot()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i42' href='#f42'>oecd.usd\_exchange\_rates\_average( )</a> </li>|Timeseries|Not that slow|
|<li> <a id='i43' href='#f43'>oecd.rer\_overall()</a> </li>|Timeseries|Not that slow|
|<u>Trade indicators</u>|||
|<li> <a id='i44' href='#f44'>oecd.exports\_value()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i45' href='#f45'>oecd.imports\_value( )</a> </li>|Timeseries|Not that slow|
|<u>Labour market indicators</u>|||
|<li> <a id='i46' href='#f46'>oecd.unemployment\_rate( )</a> </li>|Timeseries|Not that slow|
|<u>Price indices</u>|||
|<li> <a id='i47' href='#f47'>oecd.cpi\_total()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i48' href='#f48'>oecd.cpi\_city\_total( )</a> </li>|Timeseries|Not that slow|
|<li> <a id='i49' href='#f49'>oecd.cpi\_non\_food\_non\_energy()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i50' href='#f50'>oecd.cpi\_energy( )</a> </li>|Timeseries|Not that slow|
|<u>Business tendency and consumer opinion </u>|||
|<li> <a id='i51' href='#f51'>oecd.business\_tendency\_survey( sector )</a> </li>|Timeseries|Not that slow|
|<li> <a id='i52' href='#f52'>oecd.consumer\_opinion\_survey( measure = ‘national' )</a> </li>|Timeseries|Not that slow|
|<u>National accounts </u>|||
|<li> <a id='i53' href='#f53'>oecd.gdp\_deflator()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i54' href='#f54'>oecd.gdp\_total()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i55' href='#f55'>oecd.gdp\_final\_consumption()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i56' href='#f56'>oecd.gdp\_government\_consumption()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i57' href='#f57'>oecd.gdp\_fixed\_capital\_formation()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i58' href='#f58'>oecd.gdp\_exports()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i59' href='#f59'>oecd.gdp\_imports()</a> </li>|Timeseries|Not that slow|
|<u>Production and sales </u>|||
|<li> <a id='i60' href='#f60'>oecd.total\_manufacturing\_index()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i61' href='#f61'>oecd.total\_industry\_production\_ex\_construction()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i62' href='#f62'>oecd.total\_construction()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i63' href='#f63'>oecd.total\_retail\_trade()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i64' href='#f64'>oecd.passenger\_car\_registration()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i65' href='#f65'>oecd.construction\_permits\_issued()</a> </li>|Timeseries|Not that slow|
|<u>OECD Business Tendency Survey </u>|||
|<li> <a id='i66' href='#f66'>oecd.economic\_situation\_survey(sector)</a> </li>|Timeseries|Not that slow|
|<li> <a id='i67' href='#f67'>oecd.consumer\_confidence\_survey()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i68' href='#f68'>oecd.consumer\_prices\_inflation\_survey()</a> </li>|Timeseries|Not that slow|
|<u>OECD Balance of Payments </u>|||
|<i>Current Account</i>|||
|<li> <a id='i69' href='#f69'>oecd.current\_account(percent\_of\_gdp = False)</a> </li>|Timeseries|Not that slow|
|<li> <a id='i70' href='#f70'>oecd.goods\_balance( xm = ‘balance’ )</a> </li>|Timeseries|Not that slow|
|<li> <a id='i71' href='#f71'>oecd.services\_balance( xm = ‘balance’ )</a> </li>|Timeseries|Not that slow|
|<i>Financial account</i>|||
|<li> <a id='i72' href='#f72'>oecd.financial\_account(assets\_or\_liabs = None)</a> </li>|Timeseries|Not that slow|
|<li> <a id='i73' href='#f73'>oecd.direct\_investment(assets\_or\_liabs = None)</a> </li>|Timeseries|Not that slow|
|<li> <a id='i74' href='#f74'>oecd.portfolio\_investment(assets\_or\_liabs = None)</a> </li>|Timeseries|Not that slow|
|<li> <a id='i75' href='#f75'>oecd.other\_investment(assets\_or\_liabs = None)</a> </li>|Timeseries|Not that slow|
|<li> <a id='i76' href='#f76'>oecd.financial\_derivatives()</a> </li>|Timeseries|Not that slow|
|<li> <a id='i77' href='#f77'>oecd.reserve\_assets()</a> </li>|Timeseries|Not that slow|
|<b>News data</b>|||
|<li> <a id='i78' href='#f78'>news.barrons()</a> </li>|Timeseries|Slow|
|<li> <a id='i79' href='#f79'>news.bloomberg()</a> </li>|Timeseries|Very slow|
|<li> <a id='i80' href='#f80'>news.cnbc()</a> </li>|Timeseries|Very slow|
|<li> <a id='i81' href='#f81'>news.ft()</a> </li>|Timeseries|Very slow|
|<li> <a id='i82' href='#f82'>news.nyt()</a> </li>|Timeseries|Very slow|
|<li> <a id='i83' href='#f83'>news.reuters()</a> </li>|Timeseries|Very slow|
|<li> <a id='i84' href='#f84'>news.seeking\_alpha()</a> </li>|Timeseries|Slow|
|<li> <a id='i85' href='#f85'>news.wsj()</a> </li>|Timeseries|Very slow|
|<b>Other data</b>|||
|<li> <a id='i86' href='#f86'>nasdaq\_tickers()</a> </li>|List of stock tickers|Fast|
|<li> <a id='i87' href='#f87'>global\_tickers()</a> </li>|List of stock tickers|Slow|


-----

<br>

## <div id="A4"> Company Fundamental data</a>

<div align="right"><a href="#0">Back to top</a> </div>

The functions below enable you to download financial statements, valuation ratios and key financial statistics as well as analyst ratings, insider transactions, ESG scores and company profiles.

The data is pulled from <code>Yahoo Finance</code>, <code>Marketwatch.com</code> , <code>Finviz.com</code> and <code>Macrotrends.com</code>. The macrotrends scrape runs on Selenium and the website might sometimes fail to load. The function may just need to be re-run to work (assuming the ticker is available on the website). As a remedy it might sometimes help to set <code>macrotrends().head = True</code> which will then open a browser window while scraping the data.


```python
import finpie # or import finpie.fundamental_data

# Yahoo financial statements, key statistics, earnings estimates, ESG scores, company profiles
finpie.YahooData(ticker)

# Marketwatch financial statements
finpie.MwatchData(ticker)

# Finviz insider transactions, analyst ratings, key statistics
finpie.FinvizData(ticker)

# Macrotrends (long-term) financial statements and ratios
finpie.MacrotrendsData(ticker)
```

<br>

###	 <div id="A41"> <li>Valuation metrics and financial ratios <hr style="border:0.5px solid gray"> </hr> </li> </div>




#### <div id="f1"><i>YahooData(ticker).valuation\_metrics()</i></div>

<ul>
<li>Returns a dataframe with valuation metrics for the last five quarters and for the current date including trailing P/E, PEG ratio, P/S, etc.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.valuation_metrics()
```

<i> Output </i>

<center><small><small>

|    | date                  |   market\_cap\_(intraday) |   forward\_pe |   peg\_ratio\_(5\_yr\_expected) |   pricesales\_(ttm) |   pricebook\_(mrq) |   ... |
|---:|:----------------------|------------------------:|-------------:|----------------------------:|-------------------:|------------------:|--------------:|
|  1 | As of Date: 8/23/2020 |              2.02e+12   |        30.12 |                        2.4  |               7.66 |             27.98 |         ... |
|  2 | 6/30/2020             |              1.56e+12   |        24.33 |                        2.02 |               6.12 |             19.93 |         ... |
|  3 | 3/31/2020             |              1.1e+12    |        19.65 |                        1.58 |               4.34 |             12.28 |         ... |
|  4 | 12/31/2019            |              1.29e+12   |        22.17 |                        2.03 |               5.25 |             14.23 |         ...  |
|  5 | 9/30/2019             |              9.9515e+11 |        17.27 |                        2.04 |               4.09 |             10.32 |         ... |
|  6 | 6/30/2019             |              9.1064e+11 |        15.97 |                        1.45 |               3.68 |              8.47 |         ... |



</small></small></center>

<div align="right"> <a href="#i1">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id="f2"><i>YahooData(ticker).key\_metrics()</i></div>

<ul>
<li>Returns a dataframe with current key statistics and financial ratios.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.key_metrics()
```

<i> Output </i>

<center><small><small>

|    |   payout\_ratio |   profit\_margin |   operating\_margin\_(ttm) |   return\_on\_assets\_(ttm) |   return\_on\_equity\_(ttm) |   ...|
|---:|---------------:|----------------:|-------------------------:|-------------------------:|-------------------------:|----------------:|
|  0 |         0.2373 |          0.2133 |                   0.2452 |                   0.1312 |                   0.6925 |      ... |

</small></small></center>

<div align="right"> <a href="#i2">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id="f101"><i>FinvizData(ticker).key\_metrics()</i></div>

<ul>
<li>Returns a dataframe with today's key financial metrics.</li>
</ul>

<i> Example </i>

```python
finviz = FinvizData('AAPL')
finviz.key_metrics()
```

<i> Output </i>

<center><small><small>

|    | index       |   market_cap |    income |      sales |   book\_to\_sh | .. |
|---:|:------------|-------------:|----------:|-----------:|-------------:| ---: |
|  0 | DJIA S&P500 |  1.94097e+12 | 5.842e+10 | 2.7386e+11 |         4.19 | ... |


</small></small></center>

<div align="right"> <a href="#i101">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id="f102"><i>MacrotrendsData(ticker).ratios(freq = 'A')</i></div>

<ul>
<li>Returns a dataframe with annual or quarterly financial ratios up to 2005.</li>
</ul>

<i> Example </i>

```python
mt = MacrotrendsData('AAPL')
mt.ratios()
```

<i> Output </i>

<center><small><small>

|                     |   current\_ratio |   longterm\_debt\_to\_capital |   debt\_to\_equity\_ratio |   gross\_margin |   operating\_margin | ... |
|:--------------------|----------------:|---------------------------:|-----------------------:|---------------:|-------------------:| ---: |
| 2005-09-30 |          2.9538 |                        nan |                    nan |        29.0144 |            11.7938 | ... |
| 2006-09-30 |          2.2519 |                        nan |                    nan |        28.9827 |            12.7    | ... |
| 2007-09-30 |          2.3659 |                        nan |                    nan |        33.1679 |            17.9307 | ... |
| 2008-09-30 |          2.6411 |                        nan |                    nan |        35.2005 |            22.2107 | ... |
| 2009-09-30 |          2.7425 |                        nan |                    nan |        40.1399 |            27.3628 | ... |
| ... |          ... |                        ... |                    ... |        ... |            ... | ... |


</small></small></center>

<div align="right"> <a href="#i102">To index</a> </div>


<br>


###	 <div id="A42"> <li> Financial statements <hr style="border:0.5px solid gray"> </hr> </li> </div>

<div align="right"><a href="#0">Back to top</a> </div>


#### <div id="f7"><i>MwatchData(ticker).income\_statement( freq = 'annual' )</i></div>

<i>Arguments:</i>
	<code>freq = 'annual'/'a' or 'quarterly'/'q' </code>

<ul>
<li><code>freq = 'annual'</code>: Returns annual income statement for the past 5 years.</li>
<li><code>freq = 'quarterly'</code>: Returns quarterly income statement for the past 5 quarters.</li>
</ul>

<i> Example </i>

```python
mwatch = MwatchData('AAPL')
mwatch.income_statement('q')
```
<i> Output </i>
<center><small><small>

| date        |   sales\_revenue |   sales\_growth |   cost\_of\_goods\_sold\_(cogs)\_incl_danda |   cogs\_excluding\_danda |   depreciation\_and\_amortization\_expense |   ... |
|:------------|----------------:|---------------:|---------------------------------------:|-----------------------:|----------------------------------------:|---------------:|
| 30-Jun-2019 |       5.374e+10 |       nan      |                              3.357e+10 |              3.064e+10 |                                2.93e+09 |       ... |
| 30-Sep-2019 |       6.394e+10 |         0.1897 |                              3.977e+10 |              3.784e+10 |                                1.93e+09 |       ... |
| 31-Dec-2019 |       9.172e+10 |         0.4346 |                              5.677e+10 |              5.396e+10 |                                2.82e+09 |       ... |
| 31-Mar-2020 |       5.835e+10 |        -0.3639 |                              3.593e+10 |              3.315e+10 |                                2.79e+09 |      ... |
| 30-Jun-2020 |       5.942e+10 |         0.0183 |                              3.737e+10 |              3.462e+10 |                                2.75e+09 |      ... |


</small></small></center>

<div align="right"> <a href="#i7">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id="f8"><i>MwatchData(ticker).balance\_sheet( freq = 'annual' )</i></div>

<i>Arguments:</i>
	<code>freq = 'annual'/'a' or 'quarterly'/'q' </code> 
<ul><li><code>freq = 'annual'</code>: Returns annual balance sheet for the past 5 years.</li><li><code>freq = 'quarterly'</code>: Returns quarterly balance sheet for the past 5 quarters.</li>
</ul>

<i> Example </i>

```python
mwatch = MwatchData('AAPL')
mwatch.balance_sheet('q')
```
<i> Output </i>
<center><small><small>

| date        |   cash\_and\_short\_term\_investments |   cash\_only |   short-term\_investments |   cash\_and\_short\_term\_investments\_growth |   ... |
|:------------|----------------------------------:|------------:|-------------------------:|-----------------------------------------:|-----------------------------------------:|
| 30-Jun-2019 |                        9.488e+10  |   2.29e+10  |                      nan |                                 nan      |                                   ... |
| 30-Sep-2019 |                        1.0058e+11 |   2.812e+10 |                      nan |                                   0.0601 |                                   ... |
| 31-Dec-2019 |                        1.0723e+11 |   2.299e+10 |                      nan |                                   0.0661 |                                   ... |
| 31-Mar-2020 |                        9.513e+10  |   2.996e+10 |                      nan |                                  -0.1129 |                                   ... |
| 30-Jun-2020 |                        9.305e+10  |   2.73e+10  |                      nan |                                  -0.0218 |                                   ... |




</small></small></center>

<div align="right"> <a href="#i8">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id="f9"><i>MwatchData(ticker).cashflow\_statement( freq = 'annual' )</i></div>

<i>Arguments:</i>
	<code>freq = 'annual'/'a' or 'quarterly'/'q' </code> 
	
<ul>
<li><code>freq = 'annual'</code>: Returns annual cashflow statement for the past 5 years.</li>
<li><code>freq = 'quarterly'</code>: Returns quarterly cashflow statement for the past 5 quarters.</li>
</ul>


<i> Example: </i>

```python
mwatch = MwatchData('AAPL')
mwatch.cashflow_statement('q')
```

<i> Output: </i>
<center><small><small>

| date        |   net\_income\_before\_extraordinaries |   net\_income\_growth |   depreciation\_depletion\_and\_amortization |   depreciation\_and\_depletion |   ... |
|:------------|------------------------------------:|--------------------:|-------------------------------------------:|-----------------------------:|------------------------------------:|
| 30-Jun-2019 |                           1.004e+10 |            nan      |                                   2.93e+09 |                     2.93e+09 |                                 ... |
| 30-Sep-2019 |                           1.369e+10 |              0.3626 |                                   3.18e+09 |                     3.18e+09 |                                 ... |
| 31-Dec-2019 |                           2.224e+10 |              0.6247 |                                   2.82e+09 |                     2.82e+09 |                                 ... |
| 31-Mar-2020 |                           1.125e+10 |             -0.4941 |                                   2.79e+09 |                     2.79e+09 |                                 ... |
| 30-Jun-2020 |                           1.125e+10 |              0.0004 |                                   2.75e+09 |                     2.75e+09 |                                 ... |


</small></small></center>

<div align="right"> <a href="#i9">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id="f10"><i>MwatchData(ticker).statements( freq = 'annual' )</i></div>

<ul>
<li>Returns <code>MwatchData(ticker).income_statement(freq = 'annual')</code>, <code>MwatchData(ticker).balance_sheet(freq = 'annual')</code> and <code>MwatchData(ticker).cashflow_statement(freq = 'annual')</code> for the given company.</li>
</ul> 

<div align="right"> <a href="#i10">To index</a> </div>


-------

#### <div id = "f3" ><i>YahooData( ticker ).income\_statement()</i></div>

<ul>
<li>Returns annual income statement for the past 4 years.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.income_statement()
```

<i> Output </i>

<center><small><small>

|    | breakdown   |   total\_revenue |   cost\_of\_revenue |   gross\_profit |   operating\_expense |   operating\_income |   ... |
|---:|:------------|----------------:|------------------:|---------------:|--------------------:|-------------------:|--------------------------------------------:|
|  0 | ttm         |       273857000 |         169277000 |      104580000 |            37442000 |           67138000 |                                     ... |
|  1 | 9/30/2019   |       260174000 |         161782000 |       98392000 |            34462000 |           63930000 |                                     ... |
|  2 | 9/30/2018   |       265595000 |         163756000 |      101839000 |            30941000 |           70898000 |                                     ... |
|  3 | 9/30/2017   |       229234000 |         141048000 |       88186000 |            26842000 |           61344000 |                                     ... |
|  4 | 9/30/2016   |       215639000 |         131376000 |       84263000 |            24239000 |           60024000 |                                     ... |

</small></small></center>

<div align="right"> <a href="#i3">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f4" ><i>YahooData( ticker ).balance\_sheet()</i></div>

<ul>
<li>Returns annual balance sheet for the past 4 years.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.balance_sheet()
```

<i> Output </i>

<center><small><small>

|    | breakdown   |   total\_assets |   total\_liabilities\_net\_minority\_interest |   total\_equity\_gross\_minority\_interest |   total\_capitalization |   ... |
|---:|:------------|---------------:|------------------------------------------:|---------------------------------------:|-----------------------:|----------------------:|
|  0 | 9/30/2019   |      338516000 |                                 248028000 |                               90488000 |              182295000 |              ... |
|  1 | 9/30/2018   |      365725000 |                                 258578000 |                              107147000 |              200882000 |             ... |
|  2 | 9/30/2017   |      375319000 |                                 241272000 |                              134047000 |              231254000 |             ... |
|  3 | 9/30/2016   |      321686000 |                                 193437000 |                              128249000 |              203676000 |             ... |


</small></small></center>

<div align="right"> <a href="#i4">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f5" ><i>YahooData( ticker ).cashflow\_statement()</i></div>

<ul>
<li>Returns annual cashflow statement for the past 4 years.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.cashflow_statement()
```

<i> Output </i>

<center><small><small>

|    | breakdown   |   operating\_cash\_flow |   investing\_cash\_flow |   financing\_cash\_flow |   end\_cash\_position |   ... |
|---:|:------------|----------------------:|----------------------:|----------------------:|--------------------:|------------------------------------:|
|  0 | ttm         |              80008000 |             -10618000 |             -86502000 |            35039000 |                            ... |
|  1 | 9/30/2019   |              69391000 |              45896000 |             -90976000 |            50224000 |                            ... |
|  2 | 9/30/2018   |              77434000 |              16066000 |             -87876000 |            25913000 |                            ... |
|  3 | 9/30/2017   |              63598000 |             -46446000 |             -17347000 |            20289000 |                            ... |
|  4 | 9/30/2016   |              65824000 |             -45977000 |             -20483000 |            20484000 |                            ... |

</small></small></center>

<div align="right"> <a href="#i5">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f6" ><i>YahooData( ticker ).statements()</i></div>

<ul>
<li>Returns <code>YahooData(ticker).income_statement()</code>, <code>YahooData(ticker).balance_sheet()</code> and <code>YahooData(ticker).cashflow_statement()</code> for the given company.</li>
</ul> 

<div align="right"> <a href="#i6">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id="f103"><i>MacrotrendsData(ticker).income\_statement(freq = 'A')</i></div>

<ul>
<li>Returns a dataframe with annual or quarterly income statements up to 2005.</li>
</ul>

<i> Example </i>

```python
mt = MacrotrendsData('AAPL')
mt.income_statement()
```

<i> Output </i>

<center><small><small>

|                     |   revenue |   cost\_of\_goods\_sold |   gross_profit |   research\_and\_development\_expenses |   sganda\_expenses | ... |
|:--------------------|----------:|---------------------:|---------------:|------------------------------------:|------------------:| ---: |
| 2005-09-30 |     13931 |                 9889 |           4042 |                                 535 |              1864 | ... |
| 2006-09-30 |     19315 |                13717 |           5598 |                                 712 |              2433 | ... |
| 2007-09-30  |     24578 |                16426 |           8152 |                                 782 |              2963 | ... |
| 2008-09-30  |     37491 |                24294 |          13197 |                                1109 |              3761 | ... |
| 2009-09-30  |     42905 |                25683 |          17222 |                                1333 |              4149 | ... |
| ... |     ... |                ... |          ... |                                1333 |              4149 | ... |




</small></small></center>

<div align="right"> <a href="#i103">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id="f104"><i>MacrotrendsData(ticker).balance_sheet(freq = 'A')</i></div>

<ul>
<li>Returns a dataframe with annual or quarterly balance sheets up to 2005.</li>
</ul>

<i> Example </i>

```python
mt = MacrotrendsData('AAPL')
mt.balance_sheet()
```

<i> Output </i>

<center><small><small>

|                     |   cash\_on\_hand |   receivables |   inventory |   prepaid\_expenses |   other\_current\_assets | ... |
|:--------------------|---------------:|--------------:|------------:|-------------------:|-----------------------:| --- |
| 2005-09-30 00:00:00 |           8261 |           895 |         165 |                nan |                    648 | ... |
| 2006-09-30 00:00:00 |          10110 |          1252 |         270 |                nan |                   2270 | ... |
| 2007-09-30 00:00:00 |          15386 |          1637 |         346 |                nan |                   3805 | ... |
| 2008-09-30 00:00:00 |          22111 |          2422 |         509 |                nan |                   3920 | ... |
| 2009-09-30 00:00:00 |          23464 |          5057 |         455 |                nan |                   1444 | ... |
| ... |                 ... |                                             ... |                  ... |                  ... |   ... | ... |


</small></small></center>

<div align="right"> <a href="#i104">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id="f105"><i>MacrotrendsData(ticker).cashflow_statement(freq = 'A')</i></div>

<ul>
<li>Returns a dataframe with annual or quarterly cashflow statements up to 2005.</li>
</ul>

<i> Example </i>

```python
mt = MacrotrendsData('AAPL')
mt.cashflow_statement()
```

<i> Output </i>

<center><small><small>

|                     |   net\_income\_to\_loss |   total\_depreciation\_and\_amortization\_cash\_flow |   other\_noncash\_items |   total\_noncash\_items |   change\_in\_accounts\_receivable | ... |
|:--------------------|---------------------:|-------------------------------------------------:|----------------------:|----------------------:|--------------------------------:| ----: |
| 2005-09-30 |                 1328 |                                              179 |                   536 |                   715 |                             121 | ... |
| 2006-09-30 |                 1989 |                                             225 |                   231 |                   456 |                             357 | ... |
| 2007-09-30 |                 3495 |                                            327 |                   327 |                   654 |                             385 | ... |
| 2008-09-30 |                 6119 |                                           496 |                   936 |                  1432 |                             785 | ... |
| 2009-09-30 |                 8235 |                                             734 |                  1750 |                  2484 |                             939 | ... |
| ... |                 ... |                                             ... |                  ... |                  ... |                             ... | ... |


</small></small></center>

<div align="right"> <a href="#i105">To index</a> </div>



<br>




###	 <div id="A43"> <li>Earnings and revenue estimates<hr style="border:0.5px solid gray"> </hr> </li> </div>


<div align="right"><a href="#0">Back to top</a> </div>

#### <div id = "f11" ><i>YahooData( ticker ).earnings\_estimates()</i></div>

<ul>
<li>Returns current earnings estimates for the current quarter, next quarter, current year and the next year.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.earnings_estimates('AAPL')
```

<i> Output </i>
<center><small><small>

|    | date                    |   no\_of\_analysts |   avg\_estimate |   low\_estimate |   high\_estimate |   year\_ago\_eps |
|---:|:------------------------|------------------:|----------------:|---------------:|----------------:|---------------:|
|  1 | Current Qtr. (Sep 2020) |                28 |            2.8  |           2.18 |            3.19 |           3.03 |
|  2 | Next Qtr. (Dec 2020)    |                24 |            5.45 |           4.76 |            6.82 |           4.99 |
|  3 | Current Year (2020)     |                35 |           12.97 |          12.36 |           13.52 |          11.89 |
|  4 | Next Year (2021)        |                35 |           15.52 |          12.67 |           18    |          12.97 |

</small></small></center>

<div align="right"> <a href="#i11">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f12" ><i> YahooData( ticker ).earnings\_estimate\_trends()</i></div>

<ul>
<li>Returns earnings estimates for the current quarter, next quarter, current year and the next year for the current date, 7 days ago, 30 days ago, 60 days ago and 90 days ago.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.earnings_estimate_trends()
```

<i> Output </i>

<center><small><small>

|    | date                    |   current\_estimate |   7\_days\_ago |   30\_days\_ago |   60\_days\_ago |   90\_days\_ago |
|---:|:------------------------|-------------------:|-------------:|--------------:|--------------:|--------------:|
|  1 | Current Qtr. (Sep 2020) |               2.8  |         2.84 |          2.79 |          2.82 |          2.8  |
|  2 | Next Qtr. (Dec 2020)    |               5.45 |         5.44 |          5.22 |          5.21 |          5.22 |
|  3 | Current Year (2020)     |              12.97 |        13    |         12.41 |         12.39 |         12.32 |
|  4 | Next Year (2021)        |              15.52 |        15.54 |         14.94 |         14.86 |         14.73 |

</small></small></center>

<div align="right"> <a href="#i12">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f13" ><i> YahooData( ticker ).earnings\_history()</i></div>

<ul>
<li>Returns earnings estimates and actual earnings for the past 4 quarters.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.earnings_history()
```

<i> Output </i>

<center><small><small>

|    | date       |   eps\_est |   eps\_actual |   difference |   surprise\_% |
|---:|:-----------|-----------:|-------------:|-------------:|-------------:|
|  1 | 9/29/2019  |       2.84 |         3.03 |         0.19 |        0.067 |
|  2 | 12/30/2019 |       4.55 |         4.99 |         0.44 |        0.097 |
|  3 | 3/30/2020  |       2.26 |         2.55 |         0.29 |        0.128 |
|  4 | 6/29/2020  |       2.04 |         2.58 |         0.54 |        0.265 |

</small></small></center>

<div align="right"> <a href="#i13">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f14" ><i> YahooData(ticker)._revenue\_estimates()</i></div>

<ul>
<li>Returns revenue estimates for the current quarter, next quarter, current year and the next year.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.revenue_estimates()
```

<i> Output </i>

<center><small><small>

|    | date                    |   no\_of\_analysts |   avg\_estimate |   low\_estimate |   high\_estimate |   year\_ago\_sales |   sales\_growth\_(yearest) |
|---:|:------------------------|------------------:|----------------:|---------------:|----------------:|-----------------:|-------------------------:|
|  1 | Current Qtr. (Sep 2020) |                26 |      6.351e+10  |     5.255e+10  |      6.85e+10   |       6.404e+10  |                   -0.008 |
|  2 | Next Qtr. (Dec 2020)    |                24 |      1.0036e+11 |     8.992e+10  |      1.157e+11  |       8.85e+10   |                    0.134 |
|  3 | Current Year (2020)     |                33 |      2.7338e+11 |     2.6236e+11 |      2.8089e+11 |       2.6017e+11 |                    0.051 |
|  4 | Next Year (2021)        |                33 |      3.0734e+11 |     2.7268e+11 |      3.3153e+11 |       2.7338e+11 |                    0.124 |

</small></small></center>

<div align="right"> <a href="#i14">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f15" ><i> YahooData( ticker ).growth\_estimates()</i></div>

<ul>
<li>Returns earnings estimates and actual earnings for the past 4 quarters.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.growth_estimates()
```

<i> Output </i>

<center><small><small>

|                          |    aapl |   industry |   sector(s) |   sandp_500 |
|:-------------------------|--------:|-----------:|------------:|------------:|
| Current\_Qtr.             | -0.079  |        nan |         nan |         nan |
| Next\_Qtr.                |  0.088  |        nan |         nan |         nan |
| Current_Year             |  0.088  |        nan |         nan |         nan |
| Next_Year                |  0.195  |        nan |         nan |         nan |
| Next\_5\_Years\_(per\_annum) |  0.1246 |        nan |         nan |         nan |
| Past\_5\_Years\_(per\_annum) |  0.0842 |        nan |         nan |         nan |


</small></small></center>

<div align="right"> <a href="#i15">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

<br>

###	 <div id="A44"> <li>Insider transactions and analyst ratings <hr style="border:0.5px solid gray"> </hr> </li> </div>

<div align="right"><a href="#0">Back to top</a> </div>


#### <div id = "f16" ><i> FinvizData( ticker ).insider\_transactions()</i></div>

<ul>
<li>Returns company insider transactions for the past year.</li>
</ul>

<i> Example </i>

```python
finviz = FinvizData('AAPL')
finviz.insider_transactions()
```

<i> Output </i>

<center><small><small>

|    | insider_trading   | relationship                 | date   | transaction     |   cost |   #shares |   value\_($) |   #shares\_total | sec\_form\_4      |
|---:|:------------------|:-----------------------------|:-------|:----------------|-------:|----------:|------------:|----------------:|:----------------|
|  0 | COOK TIMOTHY D    | Chief Executive Officer      | Aug 25 | Sale            | 496.91 |    265160 |   131761779 |          837374 | Aug 25 06:45 PM |
|  1 | KONDO CHRIS       | Principal Accounting Officer | May 08 | Sale            | 305.62 |      4491 |     1372539 |            7370 | May 12 06:30 PM |
|  2 | JUNG ANDREA       | Director                     | Apr 28 | Option Exercise |  48.95 |      9590 |      469389 |           33548 | Apr 30 09:30 PM |
|  3 | O'BRIEN DEIRDRE   | Senior Vice President        | Apr 16 | Sale            | 285.12 |      9137 |     2605141 |           33972 | Apr 17 06:31 PM |
|  4 | Maestri Luca      | Senior Vice President, CFO   | Apr 07 | Sale            | 264.44 |     41062 |    10858445 |           27568 | Apr 09 06:30 PM |
|  ... |...     | ...  | ...| ...            | ... |     ... |    ... |           ... | ... |

</small></small></center>

<div align="right"> <a href="#i16">To index</a> </div>

-----

#### <div id = "f17" ><i> FinvizData( ticker ).analyst\_ratings()</i></div>

<ul>
<li>Returns recent history of analyst ratings.</li>
</ul>

<i> Example </i>

```python
finviz = FinvizData('AAPL')
finviz.analyst_ratings()
```

<i> Output </i>

<center><small><small>

| date                | action     | rating_institution     | rating     | price_target   |
|:--------------------|:-----------|:-----------------------|:-----------|:---------------|
| 2020-09-01 00:00:00 | Reiterated | JP Morgan              | Overweight | $115 → $150    |
| 2020-09-01 00:00:00 | Reiterated | Cowen                  | Outperform | $530 → $133    |
| 2020-08-31 00:00:00 | Reiterated | Monness Crespi & Hardt | Buy        | $117.50 → $144 |
| 2020-08-26 00:00:00 | Reiterated | Wedbush                | Outperform | $515 → $600    |
| 2020-08-25 00:00:00 | Reiterated | Cowen                  | Outperform | $470 → $530    |
| ...| ... | ...                  | ... | ...    |


</small></small></center>

<div align="right"> <a href="#i17">To index</a> </div>

-----


<br>

###	 <div id="A46"> <li> Yahoo ESG scores<hr style="border:0.5px solid gray"> </hr> </li> </div>

<div align="right"><a href="#0">Back to top</a> </div>



#### <div id = "f18" ><i>YahooData( ticker ).esg\_score()</i></div>

<ul>
<li>Returns current ESG scores from XXXX published on Yahoo Finance.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.esg_score()
```

<i> Output </i>

<center><small><small>

|    | date       |   total\_esg\_risk_score | risk\_category   | risk\_percentile   |   environment\_risk_score |   social\_risk\_score |   ... |
|---:|:-----------|-----------------------:|:----------------|:------------------|-------------------------:|--------------------:|------------------------:|
|  0 | 2020-08-25 |                     24 | Medium          | 33rd              |                      0.5 |                  13 |                    ... | 

</small></small></center>

<div align="right"> <a href="#i18">To index</a> </div>

----

#### <div id = "f19" ><i>YahooData( ticker ).corporate\_governance\_score()</i></div>

<ul>
<li>Returns current corporate governance scores from XXXX published on Yahoo Finance.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.corporate_governance_score()
```

<i> Output </i>

<center><small><small>

|    |   audit |   board |   shareholder\_rights |   compensation |   quality\_score | ticker   | date       |
|---:|--------:|--------:|---------------------:|---------------:|----------------:|:---------|:-----------|
|  0 |       1 |       1 |                    1 |              3 |               1 | AAPL     | 2020-08-25 |

</small></small></center>

<div align="right"> <a href="#i19">To index</a> </div>

----

<br>


###	 <div id="A47"> <li>Company info<hr style="border:0.5px solid gray"> </hr> </li> </div>


<div align="right"><a href="#0">Back to top</a> </div>


#### <div id = "f20" ><i>YahooData( ticker ).profile()</i></div>

<ul>
<li>Returns company sector, industry, current number of employees and a company description.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.profile()
```

<i> Output </i>

<center><small><small>

|    | company\_name   | sector     | industry             |   number\_of\_employees | description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | ticker   |
|---:|:---------------|:-----------|:---------------------|----------------------:|:----------|:---------|
|  0 | Apple Inc.     | Technology | Consumer Electronics |                137000 | Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide...  | AAPL     |

</small></small></center>

<div align="right"> <a href="#i20">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f21" ><i>YahooData( ticker ).executives_info()</i></div>

<ul>
<li>Returns current company executives with name, title, salary, age and their gender.</li>
</ul>

<i> Example </i>

```python
yahoo = YahooData('AAPL')
yahoo.executives_info()
```

<i> Output </i>


<center><small><small>

|    | name                    | title                       |       pay |   exercised |   year\_born | gender   |   age\_at\_end\_of\_year |
|---:|:------------------------|:----------------------------|----------:|------------:|------------:|:---------|---------------------:|
|  0 | Mr. Timothy D. Cook     | CEO & Director              | 1.156e+07 |         nan |        1961 | male     |                   59 |
|  1 | Mr. Luca Maestri        | CFO & Sr. VP                | 3.58e+06  |         nan |        1964 | male     |                   56 |
|  2 | Mr. Jeffrey E. Williams | Chief Operating Officer     | 3.57e+06  |         nan |        1964 | male     |                   56 |
|  3 | Ms. Katherine L. Adams  | Sr. VP, Gen. Counsel & Sec. | 3.6e+06   |         nan |        1964 | female   |                   56 |
|  4 | Ms. Deirdre O'Brien     | Sr. VP of People & Retail   | 2.69e+06  |         nan |        1967 | female   |                   53 |

</small></small></center>

<div align = "right">  <a href="#i21">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

<br>

## <div id="A5"> Price data </div>

<div align="right"><a href="#0">Back to top</a> </div>

The functions below help to retrieve daily historical price data from <code>Yahoo Finance</code> and <code>AlphaVantage</code> as well as intraday historical data from the <code>IEX Cloud</code> and <code>Tiingo</code>. Tiingo also gets their data from the IEX Cloud but their timeseries are sometimes longer although they only give OHLC data while the download from the IEX Cloud includes volume, number of trades etc..

For <a href="https://www.alphavantage.co/support/#api-key">AlphaVantage</a> and <a href="https://www.tiingo.com/">Tiingo</a> and <a href="https://iexcloud.io/cloud-login?r=https%3A%2F%2Fiexcloud.io%2Fconsole%2F#/register">IEX Cloud</a> free API keys are available. Note that IEX has a monthly free download limit unfortunately.

The <code>yahoo\_option\_chain</code> function only retrives the option chain from the last available date from Yahoo Finance.

The <code>historical\_futures\_contracts</code> function enables a bulk download of historical monthly futures contracts up to the year 2000 for currencies, indices, interest rates and commodities including energy, metals and agricultural contracts. The data is downloaded from <a href = "www.mrci.com">www.mrci.com</a> but the data is not completely cleaned (yet).

```python
import finpie.price_data

# Price data from Yahoo Finance, AlphaVantage, IEX Cloud or Tiingo 
from finpie.price_data import price_data

# Futures prices bulk-download..
from finpie.price_data import futures_prices
```

###	 <div id="A51"> <li> Stock and ETF prices <hr style="border:0.5px solid gray"> </hr> </li> </div>


#### <div id="f22"><i>yahoo\_prices( ticker )</i></div>

<ul>
<li>Returns dataframe with daily historical prices from Yahoo Finance.</li>

</ul>

<i> Example </i>

```python
yahoo_prices('AAPL')
```

<i> Output </i>

<center><small><small>

|    | Date       |    Open |    High |     Low |   Close |   Adj Close |   Volume |
|---:|:-----------|--------:|--------:|--------:|--------:|------------:|---------:|
|  0 | 1993-01-29 | 43.9688 | 43.9688 | 43.75   | 43.9375 |     26.1841 |  1003200 |
|  1 | 1993-02-01 | 43.9688 | 44.25   | 43.9688 | 44.25   |     26.3703 |   480500 |
|  2 | 1993-02-02 | 44.2188 | 44.375  | 44.125  | 44.3438 |     26.4262 |   201300 |
|  3 | 1993-02-03 | 44.4062 | 44.8438 | 44.375  | 44.8125 |     26.7055 |   529400 |
|  4 | 1993-02-04 | 44.9688 | 45.0938 | 44.4688 | 45      |     26.8172 |   531500 |
|  ... | ... | ... | ... | ... | ...      |     ... |   ... |

</small></small></center>

<div align="right"> <a href="#i22">To index</a> </div>

--------


#### <div id="f24"><i>alpha\_vantage\_prices( ticker, api\_key, start_date = None )</i></div>

<ul>
<li>Returns dataframe with daily historical prices using the AlphaVantage API.</li>
</ul>

<i> Example </i>

```python
alpha_vantage_prices('AAPL', <api_key>)
```

<i> Output </i>

<center><small><small>

| date                |   open |   high |   low |   close |   adjusted_close |     volume |   dividend_amount |   split_coefficient |
|:--------------------|-------:|-------:|------:|--------:|-----------------:|-----------:|------------------:|--------------------:|
| 1999-11-01 00:00:00 |  80    |  80.69 | 77.37 |   77.62 |           0.5988 | 2.4873e+06 |                 0 |                   1 |
| 1999-11-02 00:00:00 |  78    |  81.69 | 77.31 |   80.25 |           0.6191 | 3.5646e+06 |                 0 |                   1 |
| 1999-11-03 00:00:00 |  81.62 |  83.25 | 81    |   81.5  |           0.6287 | 2.9327e+06 |                 0 |                   1 |
| 1999-11-04 00:00:00 |  82.06 |  85.37 | 80.62 |   83.62 |           0.6451 | 3.3847e+06 |                 0 |                   1 |
| 1999-11-05 00:00:00 |  84.62 |  88.37 | 84    |   88.31 |           0.6813 | 3.7215e+06 |                 0 |                   1 |
| ... |  ... |  ... | ...    |   ... |           ... | ... |                 ... |                   ... |

</small></small></center>


<div align="right"> <a href="#i24">To index</a> </div>

------

#### <div id="f25"><i>iex\_intraday( ticker, api\_key, start\_date = None, end\_date = None )</i></div>

<ul>
<li>Returns dataframe with historical intraday price data from the IEX Cloud using the IEX Cloud API.</li>
</ul>


<i> Example </i>

```python
iex_intraday('AAPL', <api_key>)
```

<i> Output </i>

<center><small><small>

|                     | date       | label    |   high |    low |   average |   volume |         notional |   numberOfTrades |   marketHigh |   marketLow |   marketAverage |   marketVolume |   marketNotional |   marketNumberOfTrades |    open |   close |   marketOpen |   marketClose |   changeOverTime |   marketChangeOverTime |
|:--------------------|:-----------|:---------|-------:|-------:|----------:|---------:|-----------------:|-----------------:|-------------:|------------:|----------------:|---------------:|-----------------:|-----------------------:|--------:|--------:|-------------:|--------------:|-----------------:|-----------------------:|
| 2019-04-02 11:34:00 | 2019-04-02 | 11:34 AM | 285.66 | 285.59 |   285.643 |     1303 | 372193           |               15 |       285.67 |     285.59  |         285.646 |          78564 |      2.24415e+07 |                    375 | 285.655 |  285.59 |      285.65  |        285.6  |     -0.00118888  |           -0.00129363  |
| 2019-04-02 11:35:00 | 2019-04-02 | 11:35 AM | 285.62 | 285.56 |   285.599 |      755 | 215627           |                9 |       285.63 |     285.55  |         285.583 |          76670 |      2.18956e+07 |                    466 | 285.62  |  285.56 |      285.6   |        285.55 |     -0.00134274  |           -0.0015139   |
| 2019-04-02 11:36:00 | 2019-04-02 | 11:36 AM | 285.53 | 285.49 |   285.512 |      784 | 223841           |               12 |       285.56 |     285.48  |         285.506 |          80973 |      2.31183e+07 |                    412 | 285.525 |  285.52 |      285.555 |        285.52 |     -0.00164695  |           -0.00178312  |
| ... | ... | ... | ... | ... |   ... |      ... | ...           |               ... |       ... |    ...  |         ... |          ... |      ... |                    ... | ... | ... |      ... |        ... |     ...  |           ...  |

</small></small></center>

<div align="right"> <a href="#i25">To index</a> </div>



-----


#### <div id="f26"><i>tingo\_prices( ticker, api\_token, start\_date = None, end\_date = None, freq = '1min' )</i></div>

<ul>
<li>Returns dataframe with historical intraday prices using the Tiingo API. Concatenates API calls for given date range. If no date range is given all available data for the given ticker is returned.</li>
</ul>

<i> Example </i>

```python
tingo_prices('AAPL', <api_key>)
```

<i> Output </i>

<center><small><small>

| date                      |   close |    high |     low |    open |
|:--------------------------|--------:|--------:|--------:|--------:|
| 2017-01-03 14:30:00+00:00 | 115.885 | 115.9   | 115.58  | 115.8   |
| 2017-01-03 14:31:00+00:00 | 116.24  | 116.24  | 115.9   | 115.9   |
| 2017-01-03 14:32:00+00:00 | 116.3   | 116.3   | 116.26  | 116.26  |
| 2017-01-03 14:33:00+00:00 | 116.06  | 116.165 | 116.05  | 116.16  |
| 2017-01-03 14:34:00+00:00 | 116.14  | 116.18  | 116.115 | 116.115 |
| ... | ...  | ...  | ... | ... |

</small></small></center>

<div align="right"> <a href="#i26">To index</a> </div>

----

<br>

###	 <div id="A52"> <li> Option prices <hr style="border:0.5px solid gray"> </hr> </li> </div>
<div align="right"><a href="#0">Back to top</a> </div>


#### <div id="f27"><i>yahoo\_option_chain( ticker )</i></div>

<ul>
<li>Returns two dataframes for current put and call options from Yahoo Finance.</li>
</ul>

<i> Example </i>

```python
calls, puts = yahoo_option_chain('AAPL')
```

<i> Output </i>


<i>Call options chain</i>
<center><small><small>

|    | Contract_Name       | Last\_Trade\_Date        |   Strike |   Last\_Price |   ... |
|---:|:--------------------|:-----------------------|---------:|-------------:|------:|
|  0 | AAPL200828C00190000 | 2020-08-25 3:40PM EDT  |      190 |       310.29 |     ... |
|  1 | AAPL200828C00195000 | 2020-08-25 12:36PM EDT |      195 |       300.7  |     ... |
|  2 | AAPL200828C00200000 | 2020-08-25 12:13PM EDT |      200 |       294.8  |     ... |
|  3 | AAPL200828C00205000 | 2020-08-06 3:07PM EDT  |      205 |       249.54 |     ... |
|  ... | ... | ...  |      ... |       ... |     ... |

</small></small></center>

<i>Put options chain</i>
<center><small><small>

|    | Contract_Name       | Last_Trade_Date        |   Strike |   Last_Price |   Bid |
|---:|:--------------------|:-----------------------|---------:|-------------:|------:|
|  0 | AAPL200828P00190000 | 2020-08-24 2:05PM EDT  |      190 |         0.01 |     ... |
|  1 | AAPL200828P00195000 | 2020-08-10 10:38AM EDT |      195 |         0.02 |     ... |
|  2 | AAPL200828P00200000 | 2020-08-24 1:36PM EDT  |      200 |         0.01 |     ... |
|  3 | AAPL200828P00205000 | 2020-08-24 10:08AM EDT |      205 |         0.02 |     ... |
|  ... | ... | ... |      ... |         ... |     ... |

</small></small></center>



<div align="right"> <a href="#i27">To index</a> </div>




###	 <div id="A53"> <li> Futures prices <hr style="border:0.5px solid gray"> </hr> </li> </div>
<div align="right"><a href="#0">Back to top</a> </div>


#### <div id="f28"><i>historical\_futures\_contracts( pandas.date_range )</i></div>

<ul>
<li>
Returns daily price data for a number of monthly future contracts including open interest of each contract for the given date range.
</li>
</ul>

<i> Example </i>

```python
historical_futures_contracts( pd.date_range('2020-01-01', '2020-09-01') )
```

<i> Output </i>


<center><small><small>

|                     | month   |   date |   open |   high |   low |   close |   change |   volume |   open_interest | change_in_oi   | future             |
|:--------------------|:--------|-------:|-------:|-------:|------:|--------:|---------:|---------:|----------------:|:---------------|:-------------------|
| 2020-01-06 | Jan20   | 200106 |  296.2 |  299.4 | 296.2 |   297.7 |      1.6 |     4103 |            2459 | -811           | Soybean Meal(CBOT) |
| 2020-01-06 | Mar20   | 200106 |  301.5 |  304.5 | 300.6 |   302.9 |      1.7 |    58930 |          222007 | 3,678          | Soybean Meal(CBOT) |
| 2020-01-06 | May20   | 200106 |  305.3 |  308.3 | 304.6 |   306.9 |      1.7 |    23500 |           92983 | 2,616          | Soybean Meal(CBOT) |
| ... | ...   | ... |  ... |  ... | ... |   ... |      ... |    ... |           ... | ...         | ... |


</small></small></center>



<div align="right"> <a href="#i28">To index</a> </div>

----


#### <div id="f29"><i>futures\_contracts( date )</i></div>

<ul>
<li>Returns daily price data for a number of monthly future contracts including open interest of each contract for the given date.
</li>
</ul>

<i> Example </i>

```python
futures_prices('2020-01-06')
```

<i> Output </i>



<center><small><small>

|                     | month   |   date |   open |   high |   low |   close |   change |   volume |   open_interest | change_in_oi   | future             |
|:--------------------|:--------|-------:|-------:|-------:|------:|--------:|---------:|---------:|----------------:|:---------------|:-------------------|
| 2020-01-06 | Jan20   | 200106 |  296.2 |  299.4 | 296.2 |   297.7 |      1.6 |     4103 |            2459 | -811           | Soybean Meal(CBOT) |
| 2020-01-06 | Mar20   | 200106 |  301.5 |  304.5 | 300.6 |   302.9 |      1.7 |    58930 |          222007 | 3,678          | Soybean Meal(CBOT) |
| 2020-01-06 | May20   | 200106 |  305.3 |  308.3 | 304.6 |   306.9 |      1.7 |    23500 |           92983 | 2,616          | Soybean Meal(CBOT) |
| ... | ...   | ... |  ... |  ... | ... |   ... |      ... |    ... |           ... | ...         | ... |

</small></small></center>



<div align="right"> <a href="#i29">To index</a> </div>

------

## <div id="A6">Economic data</div>

<div align="right"><a href="#0">Back to top</a> </div>

The functions below retrieve economic data from the OECD database. The available economic timeseries so far include the OECD composite leading indicators, OECD business surveys, OECD main economic indicators and OECD balance of payments. 

The data can be accessed by country or for list of countries and for timeseries specific keyword arguments. Not all timeseries are available for all countries at all frequencies.

For available country codes see <a href="https://www.oecd-ilibrary.org/economics/oecd-style-guide/country-names-codes-and-currencies_9789264243439-8-en">here</a>.

```python
from finpie.economic_data import oecd_data # or import finpie

# Example for instantiating class for Australia and the USA at monthly frequency with national currencies
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'M', currency_code = 'NXCU')
# or oecd = finpie.OecdData(...) 

# Example for instantiating class for all available countries at quarterly frequency with dollar converted currencies
oecd = oecd_data.OecdData( country_code = 'all', freq = 'Q', currency_code = 'CXCU')
# or oecd = finpie.OecdData(...) 

```


<br>


### <div id="A61"><li> OECD Composite Leading Indicators </li></div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

<div align="right"><a href="#0">Back to top</a> </div>


#### <div id = "f30"><i>OecdData( country\_code, **args ).cli( subject = 'amplitude' )</i>

<ul>
<li>Returns the OECD composite leading indicator with a given measure. Only monthly data available.</li>
<li><i>Subject options:</i></li>
	<ul>
		<li>(default) amplitude adjusted</li>
		<li>LOLITONO - normalised</li>
		<li>LOLITOTR_STSA - trend restored </li>
		<li>LOLITOTR_GYSA - 12-month rate of change of the trend restored </li>
		<li>BSCICP03 - OECD standardised BCI, amplitude adjusted </li>
		<li>CSCICP03 - OECD standardised CCI, amplitude adjusted </li>
		<li>LORSGPRT - ratio to trend (gdp) </li>
		<li>LORSGPNO - normalised ( gdp ) </li>
		<li>LORSGPTD - trend ( gdp ) </li>
		<li>LORSGPOR_IXOBSA - original seasonally adjusted (gdp) </li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'M' )
oecd.cli(subject = 'amplitude')
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                  | Country       | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------------|:--------------|:------------|:--------|:------------|-----------------:|--------:|
| 1955-01-01 00:00:00 | LOLITOAA  | Amplitude adjusted (CLI) | United States | M           | 1955-01 | IDX         |                0 | 101.484 |
| 1955-02-01 00:00:00 | LOLITOAA  | Amplitude adjusted (CLI) | United States | M           | 1955-02 | IDX         |                0 | 101.838 |
| 1955-03-01 00:00:00 | LOLITOAA  | Amplitude adjusted (CLI) | United States | M           | 1955-03 | IDX         |                0 | 102.131 |
| ... | ...  | ... | ... | ...           | ... | ...         |                ... | ...  |


</small></small></center>

<div align = "right">  <a href="#i30">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f31"><i>OecdData( country\_code, **args ).cci()</i>

<ul>
<li>Returns the OECD consumer confidence indicator. Only monthly data available.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'M' )
oecd.cci()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                               | Country       | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:----------------------------------------------------------------------|:--------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | CSCICP03  | OECD Standardised CCI, Amplitude adjusted (Long term average=100), sa | United States | M           | 1960-01 | IDX         |                0 | 101.498 |
| 1960-02-01 00:00:00 | CSCICP03  | OECD Standardised CCI, Amplitude adjusted (Long term average=100), sa | United States | M           | 1960-02 | IDX         |                0 | 101.243 |
| 1960-03-01 00:00:00 | CSCICP03  | OECD Standardised CCI, Amplitude adjusted (Long term average=100), sa | United States | M           | 1960-03 | IDX         |                0 | 101.023 |
| ... | ...  | ... | ... | ...           | ... | ...         |                ... | ...  |


</small></small></center>

<div align = "right">  <a href="#i31">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f32"><i>OecdData( country\_code, **args ).bci()</i>

<ul>
<li>Returns the OECD business confidence indicator. Only monthly data available.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'M' )
oecd.bci()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                               | Country       | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:----------------------------------------------------------------------|:--------------|:------------|:--------|:------------|-----------------:|--------:|
| 1950-01-01 00:00:00 | BSCICP03  | OECD Standardised BCI, Amplitude adjusted (Long term average=100), sa | United States | M           | 1950-01 | IDX         |                0 | 101.071 |
| 1950-02-01 00:00:00 | BSCICP03  | OECD Standardised BCI, Amplitude adjusted (Long term average=100), sa | United States | M           | 1950-02 | IDX         |                0 | 101.59  |
| 1950-03-01 00:00:00 | BSCICP03  | OECD Standardised BCI, Amplitude adjusted (Long term average=100), sa | United States | M           | 1950-03 | IDX         |                0 | 102.282 |
| ... | ...  | ... | ... | ...           | ... | ...         |                ... | ...  |


</small></small></center>

<div align = "right">  <a href="#i32">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

<br>

### <div id="A62"><li> OECD Main Economic Indicators </li></div>

--------


<div align="right"><a href="#0">Back to top</a> </div>


<br>

### 

###	 <div id="A621"> <li> <i> Financial indicators </i> <hr style="border:0.5px solid gray"> </hr> </li> </div>
<div align="right"><a href="#0">Back to top</a> </div>


<br>

#### <div id = "f33"><i>OecdData( country\_code, **args ).monetary\_aggregates\_m1( index = True, seasonally\_adjusted = True )</i>

<ul>
<li>Returns the M1 monetary aggregate. Not available for all countries.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>index = True</code> returns an index, <code>index = False</code> returns level values</li>
	<li><code>seasonally_adjusted = True</code> returns seasonally adjusted index</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.monetary_aggregates_m1(index = True, seasonally_adjusted = True)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                         | Country        | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:------------------------------------------------------------------------------------------------|:---------------|:------------|:--------|:------------|-----------------:|--------:|
| 1992-01-01 00:00:00 | MANMM101  | Monetary aggregates and their components > Narrow money and components > M1 and components > M1 | Czech Republic | M           | 1992-01 | IDX         |                0 | 10.4902 |
| 1992-02-01 00:00:00 | MANMM101  | Monetary aggregates and their components > Narrow money and components > M1 and components > M1 | Czech Republic | M           | 1992-02 | IDX         |                0 | 10.4718 |
| 1992-03-01 00:00:00 | MANMM101  | Monetary aggregates and their components > Narrow money and components > M1 and components > M1 | Czech Republic | M           | 1992-03 | IDX         |                0 | 10.7145 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i33">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f34"><i>OecdData( country\_code, **args ).monetary\_aggregates\_m3(index = True, seasonally\_adjuted = True)</i>

<ul>
<li>Returns the M3 monetary aggregate. Not available for all countries.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>index = True</code> returns an index, <code>index = False</code> returns level values</li>
	<li><code>seasonally_adjusted = True</code> returns seasonally adjusted index</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.monetary_aggregates_m3( index = True, seasonally_adjuted = True )
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                         | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |    Value |
|:--------------------|:----------|:--------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|---------:|
| 1980-02-01 00:00:00 | MABMM301  | Monetary aggregates and their components > Broad money and components > M3 > M3 | Korea     | M           | 1980-02 | IDX         |                0 | 0.461489 |
| 1980-03-01 00:00:00 | MABMM301  | Monetary aggregates and their components > Broad money and components > M3 > M3 | Korea     | M           | 1980-03 | IDX         |                0 | 0.47687  |
| 1980-04-01 00:00:00 | MABMM301  | Monetary aggregates and their components > Broad money and components > M3 > M3 | Korea     | M           | 1980-04 | IDX         |                0 | 0.488449 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i34">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f35"><i>OecdData( country\_code, **args ).interbank\_rates()</i>

<ul>
<li>Returns interbank interest rates. Not available for all countries.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.interbank_rates()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                         | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:--------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1990-08-01 00:00:00 | IRSTCI01  | Interest Rates > Immediate rates (< 24 hrs) > Call money/interbank rate > Total | Australia | M           | 1990-08 | PC          |                0 |   14    |
| 1990-09-01 00:00:00 | IRSTCI01  | Interest Rates > Immediate rates (< 24 hrs) > Call money/interbank rate > Total | Australia | M           | 1990-09 | PC          |                0 |   14    |
| 1990-10-01 00:00:00 | IRSTCI01  | Interest Rates > Immediate rates (< 24 hrs) > Call money/interbank rate > Total | Australia | M           | 1990-10 | PC          |                0 |   13.43 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i35">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f36"><i>OecdData( country\_code, **args ).short\_term\_rates()</i>

<ul>
<li>Returns short-term interest rates. Not avaialable for all countries.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.short_term_rates()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                  | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1968-01-01 00:00:00 | IR3TBB01  | Interest Rates > 3-month or 90-day rates and yields > Bank bills > Total | Australia | M           | 1968-01 | PC          |                0 |    5.1  |
| 1968-02-01 00:00:00 | IR3TBB01  | Interest Rates > 3-month or 90-day rates and yields > Bank bills > Total | Australia | M           | 1968-02 | PC          |                0 |    5.15 |
| 1968-03-01 00:00:00 | IR3TBB01  | Interest Rates > 3-month or 90-day rates and yields > Bank bills > Total | Australia | M           | 1968-03 | PC          |                0 |    5.15 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i36">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f37"><i>OecdData( country\_code, **args ).long\_term\_rates()</i>

<ul>
<li>Returns long-term interest rates. Not available for all countries.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.long_term_rates()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                  | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1969-07-01 00:00:00 | IRLTLT01  | Interest Rates > Long-term government bond yields > 10-year > Main (including benchmark) | Australia | M           | 1969-07 | PC          |                0 |    5.8  |
| 1969-08-01 00:00:00 | IRLTLT01  | Interest Rates > Long-term government bond yields > 10-year > Main (including benchmark) | Australia | M           | 1969-08 | PC          |                0 |    5.79 |
| 1969-09-01 00:00:00 | IRLTLT01  | Interest Rates > Long-term government bond yields > 10-year > Main 
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i37">To index</a> </div>


_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f38"><i>OecdData( country\_code, **args ).all\_share\_prices()</i>

<ul>
<li>Returns aggregate share prices of a given country. Not available for all countries.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.all_share_prices()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                         | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1958-01-01 00:00:00 | SPASTT01  | Share Prices > All shares/broad > Total > Total | Australia | M           | 1958-01 | IDX         |                0 | 2.46886 |
| 1958-02-01 00:00:00 | SPASTT01  | Share Prices > All shares/broad > Total > Total | Australia | M           | 1958-02 | IDX         |                0 | 2.55808 |
| 1958-03-01 00:00:00 | SPASTT01  | Share Prices > All shares/broad > Total > Total | Australia | M           
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i38">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f39"><i>OecdData( country\_code, **args ).share\_prices\_industrials()</i>

<ul>
<li>Returns aggregate share prices of industrial companies from a given country. Not available for all countries.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.share_prices_industrials()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                    | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1955-01-01 00:00:00 | SPINTT01  | Share Prices > Industrials > Total > Total | Norway    | M           | 1955-01 | IDX         |                0 | 2.38957 |
| 1955-02-01 00:00:00 | SPINTT01  | Share Prices > Industrials > Total > Total | Norway    | M           | 1955-02 | IDX         |                0 | 2.29226 |
| 1955-03-01 00:00:00 | SPINTT01  | Share Prices > Industrials > Total > Total | Norway    | M           | 1955-03 | IDX         |                0 | 2.34632 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i39">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f41"><i>OecdData( country\_code, **args ).usd\_exchange\_rates\_spot()</i>

<ul>
<li>Returns USD spot exchange rates at end of month/quarter.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
usd_exchange_rates_spot()
```

<i> Output </i>


<center><small><small>


| TIME                | SUBJECT   | Subject                                                  | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:---------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1983-10-01 00:00:00 | LCEATT02  | Labour Compensation > Earnings > All activities > Weekly | Australia | Q           | 1983-Q4 | AUD         |                0 | 311.822 |
| 1984-01-01 00:00:00 | LCEATT02  | Labour Compensation > Earnings > All activities > Weekly | Australia | Q           | 1984-Q1 | AUD         |                0 | 321.838 |
| 1984-04-01 00:00:00 | LCEATT02  | Labour Compensation > Earnings > All activities > Weekly | Australia | Q           | 1984-Q2 | AUD         |                0 | 333.959 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i41">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f42"><i>OecdData( country\_code, **args ).usd\_exchange\_rates\_average()</i>

<ul>
<li>Returns monthly/quarterly average USD exchange rates.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.usd_exchange_rates_average()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                   | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |    Value |
|:--------------------|:----------|:------------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|---------:|
| 1957-01-01 00:00:00 | CCUSMA02  | Currency Conversions > US$ exchange rate > Average of daily rates > National currency:USD | Australia | M           | 1957-01 | AUD         |                0 | 0.598516 |
| 1957-02-01 00:00:00 | CCUSMA02  | Currency Conversions > US$ exchange rate > Average of daily rates > National currency:USD | Australia | M           | 1957-02 | AUD         |                0 | 0.598015 |
| 1957-03-01 00:00:00 | CCUSMA02  | Currency Conversions > US$ exchange rate > Average of daily rates > National currency:USD | Australia | M           | 1957-03 | AUD         |                0 | 0.599125 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i42">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f43"><i>OecdData( country\_code, **args ).rer\_overall()</i>

<ul>
<li>Returns overall real exchange rates.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.rer_overall()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                      | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1972-01-01 00:00:00 | CCRETT01  | Currency Conversions > Real effective exchange rates > Overall Economy > CPI | Australia | M           | 1972-01 | IDX         |                0 | 110.762 |
| 1972-02-01 00:00:00 | CCRETT01  | Currency Conversions > Real effective exchange rates > Overall Economy > CPI | Australia | M           | 1972-02 | IDX         |                0 | 109.613 |
| 1972-03-01 00:00:00 | CCRETT01  | Currency Conversions > Real effective exchange rates > Overall Economy > CPI | Australia | M           | 1972-03 | IDX         |                0 | 108.894 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i43">To index</a> </div>



<br>

### <div id="A622"> <li> <i>Trade indicators </i><hr style="border:0.5px solid gray"> </hr> </li> </div>

<div align="right"><a href="#0">Back to top</a> </div>


#### <div id = "f44"><i>OecdData( country\_code, **args ).exports\_value(growth = False, seasonally\_adjusted = True)</i>

<ul>
<li>Returns value of exports in national currency or dollar converted, etc..</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns seasonally adjusted growth</li>
	<li><code>growth = False</code> returns monthly level values in specified currency conversion (national or dollar converted)</li>
	<li><code>seasonally_adjusted = True</code> returns seasonally adjusted monthly level values in specified currency conversion (national or dollar converted)</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', currency_code = 'CXCU', freq = 'M' )
oecd.exports_value(growth = False, seasonally_adjusted = True)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                               | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |    Value |
|:--------------------|:----------|:------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|---------:|
| 1958-01-01 00:00:00 | XTEXVA01  | International Trade > Exports > Value (goods) > Total | Australia | M           | 1958-01 | USD         |                9 | 0.149812 |
| 1958-02-01 00:00:00 | XTEXVA01  | International Trade > Exports > Value (goods) > Total | Australia | M           | 1958-02 | USD         |                9 | 0.133962 |
| 1958-03-01 00:00:00 | XTEXVA01  | International Trade > Exports > Value (goods) > Total | Australia | M           | 1958-03 | USD         |                9 | 0.131655 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i44">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f45"><i>OecdData( country\_code, **args ).imports\_value(growth = False, seasonally\_adjusted = True)</i>

<ul>
<li>Returns value of imports in national currency or dollar converted, etc..</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns seasonally adjusted growth</li>
	<li><code>growth = False</code> returns monthly level values in specified currency conversion (national or dollar converted)</li>
	<li><code>seasonally_adjusted = True</code> returns seasonally adjusted monthly level values in specified currency conversion (national or dollar converted)</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', currency_code = 'CXCU', freq = 'M' )
oecd.imports_value(growth = False, seasonally_adjusted = True)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                               | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |    Value |
|:--------------------|:----------|:------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|---------:|
| 1958-01-01 00:00:00 | XTIMVA01  | International Trade > Imports > Value (goods) > Total | Australia | M           | 1958-01 | USD         |                9 | 0.155267 |
| 1958-02-01 00:00:00 | XTIMVA01  | International Trade > Imports > Value (goods) > Total | Australia | M           | 1958-02 | USD         |                9 | 0.150965 |
| 1958-03-01 00:00:00 | XTIMVA01  | International Trade > Imports > Value (goods) > Total | Australia | M           | 1958-03 | USD         |                9 | 0.138973 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i45">To index</a> </div>


_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


<br>

###	 <div id="A623"> <li> <i>Labour market indicators </i><hr style="border:0.5px solid gray"> </hr> </li> </div>

<div align="right"><a href="#0">Back to top</a> </div>


#### <div id = "f46"><i>OecdData( country\_code, **args ).unemployment\_rate()</i>

<ul>
<li>Returns unemployment rates.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.unemployment_rate()
```

<i> Output </i>

<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                               | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:------------------------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1978-02-01 00:00:00 | LRHUTTTT  | Labour Force Survey - quarterly rates > Harmonised unemployment - monthly rates > Total > All persons | Australia | M           | 1978-02 | PC          |                0 | 6.64535 |
| 1978-03-01 00:00:00 | LRHUTTTT  | Labour Force Survey - quarterly rates > Harmonised unemployment - monthly rates > Total > All persons | Australia | M           | 1978-03 | PC          |                0 | 6.30344 |
| 1978-04-01 00:00:00 | LRHUTTTT  | Labour Force Survey - quarterly rates > Harmonised unemployment - monthly rates > Total > All persons | Australia | M           | 1978-04 | PC          |                0 | 6.26811 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i46">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


<br>

###	 <div id="A624"> <li> <i>Price indices</i> <hr style="border:0.5px solid gray"> </hr> </li> </div>

<div align="right"><a href="#0">Back to top</a> </div>

#### <div id = "f47"><i>OecdData( country\_code, **args ).cpi\_total(growth = False, seasonally\_adjusted = True)</i>

<ul>
<li>Returns the consumer price index.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns yoy growth</li>
	<li><code>growth = False</code> returns index </li>
	<li><code>growth = False</code> and <code>seasonally_adjusted = True</code> returns seasonally adjusted index</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.cpi_total(growth = False, seasonally_adjusted = True)
```

<i> Output </i>

<center><small><small>

| TIME                | SUBJECT   | Subject                                          | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1985-01-01 00:00:00 | CPALTT01  | Consumer Price Index > All items > Total > Total | Japan     | M           | 1985-01 | IDX         |                0 | 85.7678 |
| 1985-02-01 00:00:00 | CPALTT01  | Consumer Price Index > All items > Total > Total | Japan     | M           | 1985-02 | IDX         |                0 | 85.6816 |
| 1985-03-01 00:00:00 | CPALTT01  | Consumer Price Index > All items > Total > Total | Japan     | M           | 1985-03 | IDX         |                0 | 85.6816 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i47">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f48"><i>OecdData( country\_code, **args ).cpi\_city\_total()</i>

<ul>
<li>Returns the consumer price index for cities.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.cpi_city_total()
```

<i> Output </i>

<center><small><small>

| TIME                | SUBJECT   | Subject                                                    | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1961-01-01 00:00:00 | CPALCY01  | Consumer Price Index > All items > All items: City > Total | Canada    | M           | 1961-01 | IDX         |                0 | 13.4288 |
| 1961-02-01 00:00:00 | CPALCY01  | Consumer Price Index > All items > All items: City > Total | Canada    | M           | 1961-02 | IDX         |                0 | 13.4288 |
| 1961-03-01 00:00:00 | CPALCY01  | Consumer Price Index > All items > All items: City > Total | Canada    | M           | 1961-03 | IDX         |                0 | 13.3779 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i48">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f49"><i>OecdData( country\_code, **args ).cpi\_non\_food\_non_energy(growth = False, seasonally\_adjusted = True)</i>

<ul>
<li>Returns non-food and non-energy consumer price index .</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns yoy growth</li>
	<li><code>growth = False</code> returns index </li>
	<li><code>growth = False</code> and <code>seasonally_adjusted = True</code> returns seasonally adjusted index</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.cpi_non_food_non_energy(growth = False, seasonally_adjusted = True)
```

<i> Output </i>

<center><small><small>

| TIME                | SUBJECT   | Subject                                                                    | Country       | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:---------------------------------------------------------------------------|:--------------|:------------|:--------|:------------|-----------------:|--------:|
| 1957-01-01 00:00:00 | CPGRLE01  | Consumer Price Index > OECD Groups > All items non-food non-energy > Total | United States | M           | 1957-01 | IDX         |                0 | 11.7649 |
| 1957-02-01 00:00:00 | CPGRLE01  | Consumer Price Index > OECD Groups > All items non-food non-energy > Total | United States | M           | 1957-02 | IDX         |                0 | 11.8062 |
| 1957-03-01 00:00:00 | CPGRLE01  | Consumer Price Index > OECD Groups > All items non-food non-energy > Total | United States | M           | 1957-03 | IDX         |                0 | 11.8474 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i49">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f50"><i>OecdData( country\_code, **args ).cpi\_energy(growth = False, seasonally\_adjusted = True)</i>

<ul>
<li>Returns consumer price index for energy (fuel, electricity, etc.).</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns yoy growth</li>
	<li><code>growth = False</code> returns index </li>
	<li><code>growth = False</code> and <code>seasonally_adjusted = True</code> returns seasonally adjusted index</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.cpi_energy(growth = False, seasonally_adjusted = True)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                            | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1991-01-01 00:00:00 | CPGREN01  | Consumer Price Index > OECD Groups > Energy (Fuel, electricity & gasoline) > Total | Germany   | M           | 1991-01 | IDX         |                0 | 46.028  |
| 1991-02-01 00:00:00 | CPGREN01  | Consumer Price Index > OECD Groups > Energy (Fuel, electricity & gasoline) > Total | Germany   | M           | 1991-02 | IDX         |                0 | 45.7485 |
| 1991-03-01 00:00:00 | CPGREN01  | Consumer Price Index > OECD Groups > Energy (Fuel, electricity & gasoline) > Total | Germany   | M           | 1991-03 | IDX         |                0 | 44.0713 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i50">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


<br>

###	 <div id="A625"> <li> <i>Business tendency and consumer opinion </i><hr style="border:0.5px solid gray"> </hr> </li> </div>
 
<div align="right"><a href="#0">Back to top</a> </div>


#### <div id = "f51"><i>OecdData( country\_code, **args ).business\_tendency\_survey( sector )</i>

<ul>
<li>Returns national business tendency survey for given sector.</li>
<li><i>Sector arguments:</i></li>
<ul>
	<li> (default) retail</li>
	<li> construction </li>
	<li> services </li>
	<li> manufacturing </li>
</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.business_tendency_survey('retail')
```

<i> Output </i>

<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                                      | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------------------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1996-01-01 00:00:00 | BRCICP02  | Business tendency surveys (retail trade) > Confidence indicators > Composite indicators > National indicator | Austria   | M           | 1996-01 | PC          |                0 |   -19.4 |
| 1996-02-01 00:00:00 | BRCICP02  | Business tendency surveys (retail trade) > Confidence indicators > Composite indicators > National indicator | Austria   | M           | 1996-02 | PC          |                0 |   -15.1 |
| 1996-03-01 00:00:00 | BRCICP02  | Business tendency surveys (retail trade) > Confidence indicators > Composite indicators > National indicator | Austria   | M           | 1996-03 | PC          |                0 |   -13.4 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |


</small></small></center>

<div align = "right">  <a href="#i51">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f52"><i>OecdData( country\_code, **args ).consumer\_opinion\_survey( measure = 'national' )</i>

<ul>
<li>Returns national consumer opinion survey.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.consumer_opinion_survey()
```

<i> Output </i>

<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                      | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:---------------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1974-09-01 00:00:00 | CSCICP02  | Consumer opinion surveys > Confidence indicators > Composite indicators > National indicator | Australia | M           | 1974-09 | PC          |                0 |      -9 |
| 1974-10-01 00:00:00 | CSCICP02  | Consumer opinion surveys > Confidence indicators > Composite indicators > National indicator | Australia | M           | 1974-10 | PC          |                0 |      -9 |
| 1974-11-01 00:00:00 | CSCICP02  | Consumer opinion surveys > Confidence indicators > Composite indicators > National indicator | Australia | M           | 1974-11 | PC          |                0 |      -8 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |


</small></small></center>

<div align = "right">  <a href="#i52">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
 
<br>

###	 <div id="A626"> <li> <i>National accounts</i><hr style="border:0.5px solid gray"> </hr> </li> </div>

<div align="right"><a href="#0">Back to top</a> </div>


#### <div id = "f53"><i>OecdData( country\_code, **args ).gdp\_deflator()</i>

<ul>
<li>Returns the quarterly GDP deflator. Not available for all countries.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'Q' )
oecd.gdp_deflator()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                 | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:----------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | NAGIGP01  | National Accounts > National Accounts Deflators > Gross Domestic Product > GDP Deflator | Australia | Q           | 1960-Q1 | IDX         |                0 | 6.78408 |
| 1960-04-01 00:00:00 | NAGIGP01  | National Accounts > National Accounts Deflators > Gross Domestic Product > GDP Deflator | Australia | Q           | 1960-Q2 | IDX         |                0 | 6.93289 |
| 1960-07-01 00:00:00 | NAGIGP01  | National Accounts > National Accounts Deflators > Gross Domestic Product > GDP Deflator | Australia | Q           | 1960-Q3 | IDX         |                0 | 6.9521  
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i53">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f54"><i>OecdData( country\_code, **args ).gdp\_total( growth = False, index = False )</i>

<ul>
<li>Returns total GDP at constant prices.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns seasonally adjusted yoy growth</li>
	<li><code>growth = False</code> and <code>index = True</code> returns seasonally adjusted index </li>
	<li><code>growth = False</code> and <code>index = False</code> returns seasonally adjusted level values</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'Q' )
oecd.gdp_total(growth = False, index = False)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                   | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:------------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1959-07-01 00:00:00 | NAEXKP01  | National Accounts > GDP by Expenditure > Constant Prices > Gross Domestic Product - Total | Australia | Q           | 1959-Q3 | AUD         |                9 |  62.496 |
| 1959-10-01 00:00:00 | NAEXKP01  | National Accounts > GDP by Expenditure > Constant Prices > Gross Domestic Product - Total | Australia | Q           | 1959-Q4 | AUD         |                9 |  63.043 |
| 1960-01-01 00:00:00 | NAEXKP01  | National Accounts > GDP by Expenditure > Constant Prices > Gross Domestic Product - Total | Australia | Q           | 1960-Q1 | AUD         |                9 |  64.683 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i54">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _



#### <div id = "f55"><i>OecdData( country\_code, **args ).gdp\_final\_consumption()</i>

<ul>
<li>Returns GDP final consumption at constant prices.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns seasonally adjusted yoy growth</li>
	<li><code>growth = False</code> and <code>index = True</code> returns seasonally adjusted index </li>
	<li><code>growth = False</code> and <code>index = False</code> returns seasonally adjusted level values</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'Q' )
oecd.gdp_final_consumption(growth = False, index = False)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                          | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1959-07-01 00:00:00 | NAEXKP02  | National Accounts > GDP by Expenditure > Constant Prices > Private Final Consumption Expenditure | Australia | Q           | 1959-Q3 | AUD         |                9 |  33.383 |
| 1959-10-01 00:00:00 | NAEXKP02  | National Accounts > GDP by Expenditure > Constant Prices > Private Final Consumption Expenditure | Australia | Q           | 1959-Q4 | AUD         |                9 |  34.303 |
| 1960-01-01 00:00:00 | NAEXKP02  | National Accounts > GDP by Expenditure > Constant Prices > Private Final Consumption Expenditure | Australia | Q           | 1960-Q1 | AUD         |                9 |  35.111 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i55">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _



#### <div id = "f56"><i>OecdData( country\_code, **args ).gdp\_government\_consumption()</i>

<ul>
<li>Returns government consumption at constant prices.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns seasonally adjusted yoy growth</li>
	<li><code>growth = False</code> and <code>index = True</code> returns seasonally adjusted index </li>
	<li><code>growth = False</code> and <code>index = False</code> returns seasonally adjusted level values</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'Q' )
oecd.gdp_government_consumption(growth = False, index = False)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                             | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:----------------------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1959-07-01 00:00:00 | NAEXKP03  | National Accounts > GDP by Expenditure > Constant Prices > Government Final Consumption Expenditure | Australia | Q           | 1959-Q3 | AUD         |                9 |   9.626 |
| 1959-10-01 00:00:00 | NAEXKP03  | National Accounts > GDP by Expenditure > Constant Prices > Government Final Consumption Expenditure | Australia | Q           | 1959-Q4 | AUD         |                9 |   9.56  |
| 1960-01-01 00:00:00 | NAEXKP03  | National Accounts > GDP by Expenditure > Constant Prices > Government Final Consumption Expenditure | Australia | Q           | 1960-Q1 | AUD         |                9 |  10.004 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i56">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _



#### <div id = "f57"><i>OecdData( country\_code, **args ).gdp\_fixed\_capital\_formation(growth = False, index = False)</i>

<ul>
<li>Returns fixed capital formation at constant prices.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns seasonally adjusted yoy growth</li>
	<li><code>growth = False</code> and <code>index = True</code> returns seasonally adjusted index </li>
	<li><code>growth = False</code> and <code>index = False</code> returns seasonally adjusted level values</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'Q' )
oecd.gdp_fixed_capital_formation(growth = False, index = False)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                  | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1959-07-01 00:00:00 | NAEXKP04  | National Accounts > GDP by Expenditure > Constant Prices > Gross Fixed Capital Formation | Australia | Q           | 1959-Q3 | AUD         |                9 |  10.278 |
| 1959-10-01 00:00:00 | NAEXKP04  | National Accounts > GDP by Expenditure > Constant Prices > Gross Fixed Capital Formation | Australia | Q           | 1959-Q4 | AUD         |                9 |   9.984 |
| 1960-01-01 00:00:00 | NAEXKP04  | National Accounts > GDP by Expenditure > Constant Prices > Gross Fixed Capital Formation | Australia | Q           | 1960-Q1 | AUD         |                9 |  10.25  |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i57">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _



#### <div id = "f58"><i>OecdData( country\_code, **args ).gdp\_exports(growth = False, index = False)</i>

<ul>
<li>Returns export value for GDP calculation.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns seasonally adjusted yoy growth</li>
	<li><code>growth = False</code> and <code>index = True</code> returns seasonally adjusted index </li>
	<li><code>growth = False</code> and <code>index = False</code> returns seasonally adjusted level values</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'Q' )
oecd.gdp_exports(growth = False, index = False)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                  | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1959-07-01 00:00:00 | NAEXKP06  | National Accounts > GDP by Expenditure > Constant Prices > Exports of Goods and Services | Australia | Q           | 1959-Q3 | AUD         |                9 |   3.991 |
| 1959-10-01 00:00:00 | NAEXKP06  | National Accounts > GDP by Expenditure > Constant Prices > Exports of Goods and Services | Australia | Q           | 1959-Q4 | AUD         |                9 |   5.172 |
| 1960-01-01 00:00:00 | NAEXKP06  | National Accounts > GDP by Expenditure > Constant Prices > Exports of Goods and Services | Australia | Q           | 1960-Q1 | AUD         |                9 |   4.603 |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i58">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _



#### <div id = "f59"><i>OecdData( country\_code, **args ).gdp\_imports(growth = False, index = False)</i>

<ul>
<li>Returns import value for GDP calculation.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>growth = True</code> returns seasonally adjusted yoy growth</li>
	<li><code>growth = False</code> and <code>index = True</code> returns seasonally adjusted index </li>
	<li><code>growth = False</code> and <code>index = False</code> returns seasonally adjusted level values</li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'Q' )
oecd.gdp_imports(growth = False, index = False)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                                        | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1959-07-01 00:00:00 | NAEXKP07  | National Accounts > GDP by Expenditure > Constant Prices > Less: Imports of Goods and Services | Australia | Q           | 1959-Q3 | AUD         |                9 |   3.226 |
| 1959-10-01 00:00:00 | NAEXKP07  | National Accounts > GDP by Expenditure > Constant Prices > Less: Imports of Goods and Services | Australia | Q           | 1959-Q4 | AUD         |                9 |   3.422 |
| 1960-01-01 00:00:00 | NAEXKP07  | National Accounts > GDP by Expenditure > Constant Prices > Less: Imports of Goods and Services | Australia | Q           | 1960-Q1 | AUD         |                9 |   3.58  |
| ... | ...  | ... | ... | ...           | ...| ...         |                ... |   ... |

</small></small></center>

<div align = "right">  <a href="#i59">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _




<br>

###	 <div id="A627"> <li> <i>Production and sales</i> <hr style="border:0.5px solid gray"> </hr> </li> </div>

<div align="right"><a href="#0">Back to top</a> </div>


#### <div id = "f60"><i>OecdData( country\_code, **args ).total\_manufacturing\_index( index = True, seasonally\_adjusted = True )</i>

<ul>
<li>Returns total manufacturing index.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>index = True</code> returns index <code>index = False</code> returns monthly or quarterly levels depending on frequency</li>
	<li><code>seasonally\_adjusted = True</code> returns seasonally adjusted values </li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.total_manufacturing_index(index = True, seasonally_adjusted = True)
```

<i> Output </i>

<center><small><small>

| TIME                | SUBJECT   | Subject                                                                | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1956-01-01 00:00:00 | PRMNTO01  | Production > Manufacturing > Total manufacturing > Total manufacturing | Austria   | M           | 1956-01 | IDX         |                0 | 11.2315 |
| 1956-02-01 00:00:00 | PRMNTO01  | Production > Manufacturing > Total manufacturing > Total manufacturing | Austria   | M           | 1956-02 | IDX         |                0 | 11.0611 |
| 1956-03-01 00:00:00 | PRMNTO01  | Production > Manufacturing > Total manufacturing > Total manufacturing | Austria   | M           | 1956-03 | IDX         |                0 | 11.2976 |
| ... | ...    | ... | ... | ...           | ... | ...          |                ... |      ... |

</small></small></center>

<div align = "right">  <a href="#i60">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f61"><i>OecdData( country\_code, **args ).total\_industry\_production\_ex\_construction(index = True, seasonally\_adjusted = True)</i>

<ul>
<li>Returns total industry production excluding construction.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>index = True</code> returns index <code>index = False</code> returns monthly or quarterly levels depending on frequency</li>
	<li><code>seasonally\_adjusted = True</code> returns seasonally adjusted values </li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.total_industrial_production_ex_construction(index = True, seasonally_adjusted = True)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                                        | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1955-01-01 00:00:00 | PRINTO01  | Production > Industry > Total industry > Total industry excluding construction | Austria   | M           | 1955-01 | IDX         |                0 | 10.7655 |
| 1955-02-01 00:00:00 | PRINTO01  | Production > Industry > Total industry > Total industry excluding construction | Austria   | M           | 1955-02 | IDX         |                0 | 10.7772 |
| 1955-03-01 00:00:00 | PRINTO01  | Production > Industry > Total industry > Total industry excluding construction | Austria   | M           | 1955-03 | IDX         |                0 | 10.7544 |
| ... | ...    | ... | ... | ...           | ... | ...          |                ... |      ... |


</small></small></center>

<div align = "right">  <a href="#i61">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f62"><i>OecdData( country\_code, **args ).total\_construction(index = True, seasonally\_adjusted = True)</i>

<ul>
<li>Returns total construction index.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>index = True</code> returns index <code>index = False</code> returns monthly or quarterly levels depending on frequency</li>
	<li><code>seasonally\_adjusted = True</code> returns seasonally adjusted values </li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.total_construction(index = True, seasonally_adjusted = True)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1996-01-01 00:00:00 | PRCNTO01  | Production > Construction > Total construction > Total | Austria   | M           | 1996-01 | IDX         |                0 |    56.1 |
| 1996-02-01 00:00:00 | PRCNTO01  | Production > Construction > Total construction > Total | Austria   | M           | 1996-02 | IDX         |                0 |    57.8 |
| 1996-03-01 00:00:00 | PRCNTO01  | Production > Construction > Total construction > Total | Austria   | M           | 1996-03 | IDX         |                0 |    57   |
| ... | ...    | ... | ... | ...           | ... | ...          |                ... |      ... |

</small></small></center>

<div align = "right">  <a href="#i62">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f63"><i>OecdData( country\_code, **args ).total\_retail\_trade(index = True, seasonally\_adjusted = True)</i>

<ul>
<li>Returns total retail trade index.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>index = True</code> returns index <code>index = False</code> returns monthly or quarterly levels depending on frequency</li>
	<li><code>seasonally\_adjusted = True</code> returns seasonally adjusted values </li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.total_retail_trade(index = True, seasonally_adjusted = True)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                           | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:--------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1955-01-01 00:00:00 | SLRTTO02  | Sales > Retail trade > Total retail trade > Value | Austria   | M           | 1955-01 | IDX         |                0 | 5.65006 |
| 1955-02-01 00:00:00 | SLRTTO02  | Sales > Retail trade > Total retail trade > Value | Austria   | M           | 1955-02 | IDX         |                0 | 5.72288 |
| 1955-03-01 00:00:00 | SLRTTO02  | Sales > Retail trade > Total retail trade > Value | Austria   | M           | 1955-03 | IDX         |                0 | 5.63975 |
| ... | ...    | ... | ... | ...           | ... | ...          |                ... |      ... |

</small></small></center>

<div align = "right">  <a href="#i63">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f64"><i>OecdData( country\_code, **args ).passenger\_car\_registrations(index = True, seasonally\_adjusted = True)</i>

<ul>
<li>Returns index for passenger car registrations.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>index = True</code> returns index <code>index = False</code> returns monthly or quarterly levels depending on frequency</li>
	<li><code>seasonally\_adjusted = True</code> returns seasonally adjusted values </li>
	</ul>
<li> </li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.passenger_car_registrations(index = True, seasonally_adjusted = True)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                                  | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:---------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1994-01-01 00:00:00 | SLRTCR03  | Sales > Retail trade > Car registration > Passenger cars | Australia | M           | 1994-01 | IDX         |                0 | 83.9795 |
| 1994-02-01 00:00:00 | SLRTCR03  | Sales > Retail trade > Car registration > Passenger cars | Australia | M           | 1994-02 | IDX         |                0 | 86.7998 |
| 1994-03-01 00:00:00 | SLRTCR03  | Sales > Retail trade > Car registration > Passenger cars | Australia | M           | 1994-03 | IDX         |                0 | 85.8574 |
| ... | ...    | ... | ... | ...           | ... | ...          |                ... |      ... |

</small></small></center>

<div align = "right">  <a href="#i64">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f65"><i>OecdData( country\_code, **args ).construction\_permits\_issued(index = True, seasonally\_adjusted = True)</i>

<ul>
<li>Returns index for construction permits issued.</li>
<li><i>Arguments</i>:</li>
	<ul>
	<li><code>index = True</code> returns index <code>index = False</code> returns monthly or quarterly levels depending on frequency</li>
	<li><code>seasonally\_adjusted = True</code> returns seasonally adjusted values </li>
	</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'all', freq = 'M' )
oecd.construction_permits_issued(index = True, seasonally_adjusted = True)
```

<i> Output </i>

<center><small><small>

| TIME                | SUBJECT   | Subject                                                                    | Country   | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:---------------------------------------------------------------------------|:----------|:------------|:--------|:------------|-----------------:|--------:|
| 1955-01-01 00:00:00 | ODCNPI03  | Orders > Construction > Permits issued > Dwellings / Residential buildings | Australia | M           | 1955-01 | IDX         |                0 | 32.3003 |
| 1955-02-01 00:00:00 | ODCNPI03  | Orders > Construction > Permits issued > Dwellings / Residential buildings | Australia | M           | 1955-02 | IDX         |                0 | 40.88   |
| 1955-03-01 00:00:00 | ODCNPI03  | Orders > Construction > Permits issued > Dwellings / Residential buildings | Australia | M           | 1955-03 | IDX         |                0 | 35.8331 |
| ... | ...    | ... | ... | ...           | ... | ...          |                ... |      ... |

</small></small></center>

<div align = "right">  <a href="#i65">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


<br>


## <div id = "A63"><li> OECD Business Tendency Survey </li></div>

<div align="right"><a href="#0">Back to top</a> </div>



#### <div id = "f66" ><i>OecdData( country\_code, **args ).economic\_situation\_survey()</i> </div>

<ul>
<li>Returns national economic situation survey.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'M' )
oecd.economic_situation_survey()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject         | Country       | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:----------------|:--------------|:------------|:--------|:------------|-----------------:|--------:|
| 1978-01-01 00:00:00 | CSESFT    | Future tendency | United States | M           | 1978-01 | PC          |                0 |       8 |
| 1978-02-01 00:00:00 | CSESFT    | Future tendency | United States | M           | 1978-02 | PC          |                0 |      11 |
| 1978-03-01 00:00:00 | CSESFT    | Future tendency | United States | M           | 1978-03 | PC          |                0 |      -3 |
| ... | ...    | ... | ... | ...           | ... | ...          |                ... |      ... |

</small></small></center>

<div align = "right">  <a href="#i66">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f67" ><i>OecdData( country\_code, **args ).consumer\_confidence\_survey()</i> </div>

<ul>
<li>Returns national consumer confidence survey.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'M' )
oecd.consumer_confidence_survey()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject            | Country       | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------|:--------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | CSCICP02  | National indicator | United States | M           | 1960-01 | PC          |                0 | 107.594 |
| 1960-02-01 00:00:00 | CSCICP02  | National indicator | United States | M           | 1960-02 | PC          |                0 | 105.191 |
| 1960-03-01 00:00:00 | CSCICP02  | National indicator | United States | M           | 1960-03 | PC          |                0 | 102.788 |
| ... | ...  | ... | ... | ...          | ... | ...          |                ... | ... |

</small></small></center>

<div align = "right">  <a href="#i67">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f68" ><i>OecdData( country\_code, **args ).consumer\_price_inflation\_survey()</i></div>

<ul>
<li>Returns consumer price inflation survey.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'M' )
oecd.consumer_price_inflation_survey()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject         | Country       | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:----------------|:--------------|:------------|:--------|:------------|-----------------:|--------:|
| 1978-01-01 00:00:00 | CSINFT    | Future tendency | United States | M           | 1978-01 | PC          |                0 |     6.1 |
| 1978-02-01 00:00:00 | CSINFT    | Future tendency | United States | M           | 1978-02 | PC          |                0 |     8.5 |
| 1978-03-01 00:00:00 | CSINFT    | Future tendency | United States | M           | 1978-03 | PC          |                0 |     7.5 |
| ... | ...    | ... | ... | ...         | ...| ...          |                ... |     ... |

</small></small></center>

<div align = "right">  <a href="#i68">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

<br>


## <div id = "A64"><li> OECD Balance of Payments </li></div>

<div align="right"><a href="#0">Back to top</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


### <div id = "A641"><i>Current account</i></div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f69" ><i>OecdData( country\_code, **args ).current_account( percent\_of\_gdp = False )</i></div>

<ul>
<li>Returns the current account as value or as percent of GDP.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'Q' )
oecd.current_account(percent_of_gdp = True)
```

<i> Output </i>

<center><small><small>

| TIME                | SUBJECT   | Subject                             | Country       | MEASURE   | Measure                  | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |    Value |
|:--------------------|:----------|:------------------------------------|:--------------|:----------|:-------------------------|:------------|:--------|:------------|-----------------:|---------:|
| 1960-01-01 00:00:00 | B6BLTT02  | Current account balance as % of GDP | United States | STSA      | Indicators in percentage | Q           | 1960-Q1 | PC          |                0 | 0.257994 |
| 1960-04-01 00:00:00 | B6BLTT02  | Current account balance as % of GDP | United States | STSA      | Indicators in percentage | Q           | 1960-Q2 | PC          |                0 | 0.391809 |
| 1960-07-01 00:00:00 | B6BLTT02  | Current account balance as % of GDP | United States | STSA      | Indicators in percentage | Q           | 1960-Q3 | PC          |                0 | 0.612899 |
| ... | ...  | ... | ... | ...      | ... | ...           | ... | ...         |                ... |    ... |

</small></small></center>

<div align="right"> <a href="#i69">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f70" ><i>OecdData( country\_code, **args ).goods\_balance( xm = 'balance' )</i></div>

<ul>
<li>Returns the imported, exported goods or good balance of the current account.</li>
<li><i>xm arguments:</i></li>
<ul>
<li> (default) balance </li>
<li> exports </li>
<li> imports </li>
</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'Q' )
oecd.goods_balance(xm = 'exports')
```

<i> Output </i>


<center><small><small>


| TIME                | SUBJECT   | Subject                  | Country       | MEASURE   | Measure             | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-------------------------|:--------------|:----------|:--------------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | B6CRTD01  | Goods, credits (exports) | United States | CXCU      | US-Dollar converted | Q           | 1960-Q1 | USD         |                6 |    4664 |
| 1960-04-01 00:00:00 | B6CRTD01  | Goods, credits (exports) | United States | CXCU      | US-Dollar converted | Q           | 1960-Q2 | USD         |                6 |    5058 |
| 1960-07-01 00:00:00 | B6CRTD01  | Goods, credits (exports) | United States | CXCU      | US-Dollar converted | Q           | 1960-Q3 | USD         |                6 |    4736 |
| ... | ...  | ... | ... | ...      | ... | ...           | ... | ...         |                ... |    ... |


</small></small></center>

<div align = "right">  <a href="#i70">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f71" ><i>OecdData( country\_code, **args ).services\_balance( xm = 'balance' )</i></div>

<ul>
<li>Returns the imported, exported services or services balance of the current account.</li>
<li><i>xm arguments:</i></li>
<ul>
<li> (default) balance </li>
<li> exports </li>
<li> imports </li>
</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'Q' )
oecd.goods_balance(xm = 'balance')
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject           | Country       | MEASURE   | Measure             | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:------------------|:--------------|:----------|:--------------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | B6BLSE01  | Services, balance | United States | CXCU      | US-Dollar converted | Q           | 1960-Q1 | USD         |                6 |    -239 |
| 1960-04-01 00:00:00 | B6BLSE01  | Services, balance | United States | CXCU      | US-Dollar converted | Q           | 1960-Q2 | USD         |                6 |    -205 |
| 1960-07-01 00:00:00 | B6BLSE01  | Services, balance | United States | CXCU      | US-Dollar converted | Q           | 1960-Q3 | USD         |                6 |    -758 |
| ... | ...  | ... | ... | ...      | ...| ...           | ... | ...         | ... |    ... |


</small></small></center>

<div align = "right">  <a href="#i71">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


### <div id = "A642"><i>Financial account</i></div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f72" ><i>OecdData( country\_code, **args ).financial\_account( assets\_or\_liabs = None )</i></div>

<ul>
<li>Returns the assets, liabilities or net financial account in specified currency.</li>
<li><i>assets\_or\_liabs arguments:</i></li>
<ul>
<li> (default) None </li>
<li> assets </li>
<li> liabs </li>
</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'Q', currency = 'CXCU' )
oecd.financial_account(assets_or_liabs = None)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                | Country       | MEASURE   | Measure             | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------|:--------------|:----------|:--------------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | B6FATT01  | Financial account, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q1 | USD         |                6 |     358 |
| 1960-04-01 00:00:00 | B6FATT01  | Financial account, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q2 | USD         |                6 |     414 |
| 1960-07-01 00:00:00 | B6FATT01  | Financial account, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q3 | USD         |                6 |     159 |
| ... | ...  | ... | ... | ...      | ... | ...           | ... | ...         |                ... |    ... |


</small></small></center>

<div align = "right">  <a href="#i72">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f73" ><i>OecdData( country\_code, **args ).direct\_investment( assets\_or\_liabs = None )</i></div>

<ul>
<li>Returns the assets, liabilities or net direct investment of the financial account.</li>
<ul>
<li> (default) None </li>
<li> assets </li>
<li> liabs </li>
</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'Q', currency = 'CXCU' )
oecd.direct_investment(assets_or_liabs = None)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                | Country       | MEASURE   | Measure             | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:-----------------------|:--------------|:----------|:--------------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | B6FADI01  | Direct investment, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q1 | USD         |                6 |     591 |
| 1960-04-01 00:00:00 | B6FADI01  | Direct investment, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q2 | USD         |                6 |     560 |
| 1960-07-01 00:00:00 | B6FADI01  | Direct investment, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q3 | USD         |                6 |     595 |
| ... | ...  | ... | ... | ...      | ... | ...           | ... | ...         |                ... |    ... |

</small></small></center>

<div align = "right">  <a href="#i73">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f74" ><i>OecdData( country\_code, **args ).portfolio\_investment( assets\_or\_liabs = None )</i></div>

<ul>
<li>Returns the assets, liabilities or net portfolio investment of the financial account.</li>
<ul>
<li> (default) None </li>
<li> assets </li>
<li> liabs </li>
</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'Q', currency = 'CXCU' )
oecd.portfolio_investment(assets_or_liabs = None)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                   | Country       | MEASURE   | Measure             | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:--------------------------|:--------------|:----------|:--------------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | B6FAPI10  | Portfolio investment, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q1 | USD         |                6 |      69 |
| 1960-04-01 00:00:00 | B6FAPI10  | Portfolio investment, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q2 | USD         |                6 |     139 |
| 1960-07-01 00:00:00 | B6FAPI10  | Portfolio investment, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q3 | USD         |                6 |     -27 |
| ... | ...  | ... | ... | ...      | ... | ...           | ... | ...         |                ... |    ... |

</small></small></center>

<div align = "right">  <a href="#i74">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f75" ><i>OecdData( country\_code, **args ).other\_investment( assets\_or\_liabs = None )</i></div>

<ul>
<li>Returns the assets, liabilities or net other investments of the financial account.</li>
<ul>
<li> (default) None </li>
<li> assets </li>
<li> liabs </li>
</ul>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'Q', currency = 'CXCU' )
oecd.other_investment(assets_or_liabs = None)
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject               | Country       | MEASURE   | Measure             | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:----------------------|:--------------|:----------|:--------------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | B6FAOI01  | Other investment, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q1 | USD         |                6 |    -143 |
| 1960-04-01 00:00:00 | B6FAOI01  | Other investment, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q2 | USD         |                6 |    -110 |
| 1960-07-01 00:00:00 | B6FAOI01  | Other investment, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q3 | USD         |                6 |     331 |
| ... | ...  | ... | ... | ...      | ... | ...           | ... | ...         |                ... |    ... |

</small></small></center>

<div align = "right">  <a href="#i75">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f76" ><i>OecdData( country\_code, **args ).financial\_derivatives()</i></div>

<ul>
<li>Returns the net financial derivatives of the financial account.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'Q', currency = 'CXCU' )
oecd.financial_derivatives()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                    | Country       | MEASURE   | Measure             | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:---------------------------|:--------------|:----------|:--------------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | B6FAFD01  | Financial derivatives, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q1 | USD         |                6 |       0 |
| 1960-04-01 00:00:00 | B6FAFD01  | Financial derivatives, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q2 | USD         |                6 |       0 |
| 1960-07-01 00:00:00 | B6FAFD01  | Financial derivatives, net | United States | CXCU      | US-Dollar converted | Q           | 1960-Q3 | USD         |                6 |       0 |
| ... | ...  | ... | ... | ...      | ... | ...           | ... | ...         |                ... |    ... |


</small></small></center>

<div align = "right">  <a href="#i76">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f77" ><i>OecdData( country\_code, **args ).reserve\_assets()</i></div>

<ul>
<li>Returns the net reserve assets of the financial account.</li>
</ul>

<i> Example </i>

```python
oecd = oecd_data.OecdData( country_code = 'USA', freq = 'Q', currency = 'CXCU' )
oecd.reserve_assets()
```

<i> Output </i>


<center><small><small>

| TIME                | SUBJECT   | Subject                                             | Country       | MEASURE   | Measure             | FREQUENCY   | TIME    | Unit Code   |   PowerCode Code |   Value |
|:--------------------|:----------|:----------------------------------------------------|:--------------|:----------|:--------------------|:------------|:--------|:------------|-----------------:|--------:|
| 1960-01-01 00:00:00 | B6FARA01  | Reserve assets, net acquisition of financial assets | United States | CXCU      | US-Dollar converted | Q           | 1960-Q1 | USD         |                6 |    -159 |
| 1960-04-01 00:00:00 | B6FARA01  | Reserve assets, net acquisition of financial assets | United States | CXCU      | US-Dollar converted | Q           | 1960-Q2 | USD         |                6 |    -175 |
| 1960-07-01 00:00:00 | B6FARA01  | Reserve assets, net acquisition of financial assets | United States | CXCU      | US-Dollar converted | Q           | 1960-Q3 | USD         |                6 |    -740 |
| ... | ...  | ... | ... | ...      | ... | ...           | ... | ...         |                ... |    ... |

</small></small></center>

<div align = "right">  <a href="#i77">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

## <div id="A7">News data</div>

<div align="right"><a href="#0">Back to top</a> </div>

The functions below retrieve news headlines based on keyword searches from <code>Barrons</code>, <code>Bloomberg</code>, <code>CNBC</code>, the <code>Financial Times</code>, the <code>New York Times</code>, <code>Reuters</code>, <code>Seeking Alpha</code> and the <code>Wall Street Journal</code>. The keyword for Seeking Alpha is simply the relevant stock ticker.


The scrape is based on Selenium and may not be very stable if the website layouts change although I'll try to update asap if it does. 

Furthermore, some of the functions will can for a long-time so it is recommended to use a reasonable <code>datestop</code> value especially for CNBC, Reuters or Bloomberg. 


```python
# Importing the NewsData class
from finpie import NewsData # 
news = NewsData('XOM', 'exxon mobil')
news.head = False # default = false, ensures selenium headless mode
news.verbose = True # default = False, prints total number of collected articles
```


<br>

-----

#### <div id = "f78" ><i>NewsData(ticker, keywords).barrons()</i></div>

<ul>
<li>Returns the news headlines from Barrons.com for the specified keywords.</li>
</ul>

<i> Example </i>

```python
# retrieve news article for a given search term
news = NewsData('XOM', 'exxon mobil')
df = news.barrons()
# filter news headlines with a keyword list
news.filterz = [ 'exxon', 'mobil', 'oil', 'energy' ]
df = news.filter_data(df)
```

<i> Output </i>


<center><small><small>

| date       | link                                                                                                           | headline                                                                      | description                                                                                                                                                                                                   | newspaper   | author                  | date_retrieved             | ticker   |   comments |   tag | search_term   | id                                                                                                                                                                                                | source   |
|:-----------|:---------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|:------------------------|:---------------------------|:---------|-----------:|------:|:--------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
| 15/09/2020 | https://www.barrons.com/articles/options-traders-are-pricing-in-an-exxon-dividend-cut-analyst-says-51600181938 | Options Traders Are Pricing In an Exxon Dividend Cut, Analyst Says            | Whether Exxon can maintain its dividend is one of the most active debates right now among energy investors. The company has a strong incentive to keep making payments at current levels.                     | Barrons.com | Avi Salzman             | 2020-09-16 13:35:26.574289 | XOM      |        nan |   nan | exxon mobil   | Barrons.comOptions Traders Are Pricing In an Exxon Dividend Cut, Analyst Sayshttps://www.barrons.com/articles/options-traders-are-pricing-in-an-exxon-dividend-cut-analyst-says-51600181938       | barrons  |
| 13/09/2020 | https://www.wsj.com/articles/exxon-used-to-be-americas-most-valuable-company-what-happened-oil-gas-11600037243 | Exxon Used to Be America’s Most Valuable Company. What Happened?              | The oil giant doubled down on oil and gas at what now looks to be the worst possible time. Investors are fleeing and workers are grumbling about the direction of a company some see as out of touch.         | WSJ.com     | Christopher M. Matthews | 2020-09-16 13:35:26.574289 | XOM      |        nan |   nan | exxon mobil   | WSJ.comExxon Used to Be America’s Most Valuable Company. What Happened?https://www.wsj.com/articles/exxon-used-to-be-americas-most-valuable-company-what-happened-oil-gas-11600037243             | barrons  |
| 11/09/2020 | https://www.barrons.com/articles/where-to-find-bargains-in-oil-stocks-51599837910                              | Where to Find Bargains in Oil Stocks Now                                      | Goldman Sachs analyst likes certain refiners and Canadian oil companies.                                                                                                                                      | Barrons.com | Avi Salzman             | 2020-09-16 13:35:26.574289 | XOM      |        nan |   nan | exxon mobil   | Barrons.comWhere to Find Bargains in Oil Stocks Nowhttps://www.barrons.com/articles/where-to-find-bargains-in-oil-stocks-51599837910                                                              | barrons  |
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|


</small></small></center>

<div align = "right">  <a href="#i78">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f79" ><i>NewsData(ticker, keywords).bloomberg()</i></div>

<ul>
<li>Returns the news headlines from Bloomberg.com for the specified keywords.</li>
</ul>

<i> Example </i>

```python
# retrieve news article for a given search term
news = NewsData('XOM', 'exxon mobil')
df = news.bloomberg()
# filter news headlines with a keyword list
news.filterz = [ 'exxon', 'mobil', 'oil', 'energy' ]
df = news.filter_data(df)
```

<i> Output </i>


<center><small><small>

| date                | link                                                                                                            | headline                                                        | description                                                                                                     | tag     |   author | date_retrieved             | ticker   |   comments | newspaper   | search_term   | id                                                                                                                                                                                      | source    |
|:--------------------|:----------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------|:--------|---------:|:---------------------------|:---------|-----------:|:------------|:--------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------|
| 2020-09-14 00:00:00 | https://www.bloomberg.com/view/articles/2020-09-14/what-tesla-exxon-mobil-and-shale-have-in-common              | What Tesla, Exxon Mobil and Shale Have in Common                | Both share a revolutionary story, shaky profits and regular capital-raising. That didn’t end well for frackers. | opinion |      nan | 2020-09-16 14:09:38.411697 | XOM      |        nan | Bloomberg   | exxon mobil   | BloombergWhat Tesla, Exxon Mobil and Shale Have in Commonhttps://www.bloomberg.com/view/articles/2020-09-14/what-tesla-exxon-mobil-and-shale-have-in-common                             | bloomberg |
| 2020-09-15 00:00:00 | https://www.bloomberg.com/view/articles/2020-09-15/bp-s-peak-oil-era-threatens-more-venezuela-like-collapses    | BP's Peak Oil Era Threatens More Venezuela-Like Collapses       | Producers that aren’t able to diversify in time will face economic collapse.                                    | opinion |      nan | 2020-09-16 14:09:38.411697 | XOM      |        nan | Bloomberg   | exxon mobil   | BloombergBP's Peak Oil Era Threatens More Venezuela-Like Collapseshttps://www.bloomberg.com/view/articles/2020-09-15/bp-s-peak-oil-era-threatens-more-venezuela-like-collapses          | bloomberg |
| 2020-09-15 00:00:00 | https://www.bloomberg.com/news/articles/2020-09-15/peak-oil-bp-shell-eni-lead-big-oil-s-search-for-new-business | Peak Oil: BP, Shell, Eni Lead Big Oil’s Search for New Business | The supermajor business model that owned a century comes undone.                                                | green   |      nan | 2020-09-16 14:09:38.411697 | XOM      |        nan | Bloomberg   | exxon mobil   | BloombergPeak Oil: BP, Shell, Eni Lead Big Oil’s Search for New Businesshttps://www.bloomberg.com/news/articles/2020-09-15/peak-oil-bp-shell-eni-lead-big-oil-s-search-for-new-business | bloomberg |
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|


</small></small></center>

<div align = "right">  <a href="#i79">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f80" ><i>NewsData(ticker, keywords).cnbc()</i></div>

<ul>
<li>Returns the news headlines from CNBC for the specified keywords.</li>
</ul>

<i> Example </i>

```python
# retrieve news article for a given search term
news = NewsData('XOM', 'exxon mobil')
df = news.cnbc()
# filter news headlines with a keyword list
news.filterz = [ 'exxon', 'mobil', 'oil', 'energy' ]
df = news.filter_data(df)
```

<i> Output </i>


<center><small><small>

| date                | link                                                                                                                              | headline                                                            | description                                                                                                                                                               | tag             | author       | date_retrieved             | ticker   |   comments | newspaper   | search_term   | id                                                                                                                                                                                                       | source   |
|:--------------------|:----------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------|:-------------|:---------------------------|:---------|-----------:|:------------|:--------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
| 2020-09-10 00:00:00 | https://www.cnbc.com/video/2020/09/10/honeywell-ceo-darius-adamczyk-on-rejoining-the-dow.html?&qsearchterm=exxon mobil            | Honeywell CEO Darius Adamczyk on rejoining the Dow                  | S&P Dow Jones Indices said Monday that three new companies will be joining the 30-stock benchmark. Salesforce.com will replace Exxon Mobil, Amgen will replace Pfizer ... | Squawk Box U.S. | nan          | 2020-09-16 14:14:43.533664 | XOM      |        nan | CNBC        | exxon mobil   | CNBCHoneywell CEO Darius Adamczyk on rejoining the Dowhttps://www.cnbc.com/video/2020/09/10/honeywell-ceo-darius-adamczyk-on-rejoining-the-dow.html?&qsearchterm=exxon mobil                             | cnbc     |
| 2020-09-09 00:00:00 | https://www.cnbc.com/2020/09/09/options-market-predicts-exxon-mobils-dividend-could-be-in-danger.html?&qsearchterm=exxon mobil    | Options market predicts Exxon Mobil’s dividend could be in danger   | One of the most consistent dividend payers in the history of the energy trade could be in danger of having to slash its payout, according ...                             | Options Action  | Tyler Bailey | 2020-09-16 14:14:43.533664 | XOM      |        nan | CNBC        | exxon mobil   | CNBCOptions market predicts Exxon Mobil’s dividend could be in dangerhttps://www.cnbc.com/2020/09/09/options-market-predicts-exxon-mobils-dividend-could-be-in-danger.html?&qsearchterm=exxon mobil      | cnbc     |
| 2020-09-08 00:00:00 | https://www.cnbc.com/2020/09/08/exxon-downsizes-global-empire-as-wall-street-worries-about-dividend.html?&qsearchterm=exxon mobil | Exxon downsizes global empire as Wall Street worries about dividend | Ill-timed bets on rising demand have Exxon Mobil facing a shortfall of about $48 billion through 2021, according to a Reuters tally and Wall Street ...                   | Oil and Gas     | nan          | 2020-09-16 14:14:43.533664 | XOM      |        nan | CNBC        | exxon mobil   | CNBCExxon downsizes global empire as Wall Street worries about dividendhttps://www.cnbc.com/2020/09/08/exxon-downsizes-global-empire-as-wall-street-worries-about-dividend.html?&qsearchterm=exxon mobil | cnbc     |
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|


</small></small></center>

<div align = "right">  <a href="#i80">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f81" ><i>NewsData(ticker, keywords).ft()</i></div>

<ul>
<li>Returns the news headlines from the Financial Times for the specified keywords.</li>
</ul>

<i> Example </i>

```python
# retrieve news article for a given search term
news = NewsData('XOM', 'exxon mobil')
df = news.ft()
# filter news headlines with a keyword list
news.filterz = [ 'exxon', 'mobil', 'oil', 'energy' ]
df = news.filter_data(df)
```

<i> Output </i>


<center><small><small>

| date                | link                                          | headline                                                         | description                                                                                                                                                                                                                     | tag                  | date_retrieved             | ticker   |   comments |   author | newspaper   | search_term   | id                                                                                                              | source   |
|:--------------------|:----------------------------------------------|:-----------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------|:---------------------------|:---------|-----------:|---------:|:------------|:--------------|:----------------------------------------------------------------------------------------------------------------|:---------|
| 2020-07-31 00:00:00 | /content/64d7e86e-079c-4502-a9a4-5ab7439c732f | Big Oil gets smaller as Chevron and Exxon losses mount to $9.4bn | ...destruction in the second quarter was unprecedented in the history of modern oil markets,” Neil Chapman, Exxon senior vice-president, told analysts on an investor call.                  “To put it in context, absolute... | Oil & Gas industry   | 2020-09-16 14:20:31.865540 | XOM      |        nan |      nan | FT          | exxon mobil   | FTBig Oil gets smaller as Chevron and Exxon losses mount to $9.4bn/content/64d7e86e-079c-4502-a9a4-5ab7439c732f | ft       |
| 2020-05-27 00:00:00 | /content/c43ead81-5af3-44de-af1e-b108d6491354 | Exxon shareholders vote against splitting chair and CEO roles    | ...Exxon, said the appointment of a lead director had helped improve oversight.                  A separate resolution calling for increased transparency about Exxon’s lobbying activity won 37.5 per cent support, a...       | Oil & Gas industry   | 2020-09-16 14:20:31.865540 | XOM      |        nan |      nan | FT          | exxon mobil   | FTExxon shareholders vote against splitting chair and CEO roles/content/c43ead81-5af3-44de-af1e-b108d6491354    | ft       |
| 2020-05-12 00:00:00 | /content/c54ee229-f4e7-43c8-87a5-e383099542fb | Big Exxon shareholder to vote against chief                      | ...company to disclose its lobbying activities, arguing it was falling behind global peers by failing to act on climate change.                  Wednesday’s move by LGIM, whose roughly $1bn stake makes it a top-20 Exxon...  | Corporate governance | 2020-09-16 14:20:31.865540 | XOM      |        nan |      nan | FT          | exxon mobil   | FTBig Exxon shareholder to vote against chief/content/c54ee229-f4e7-43c8-87a5-e383099542fb                      | ft       |
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|


</small></small></center>

<div align = "right">  <a href="#i81">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f82" ><i>NewsData(ticker, keywords).nyt()</i></div>

<ul>
<li>Returns the news headlines from the New York Times for the specified keywords.</li>
</ul>

<i> Example </i>

```python
# retrieve news article for a given search term
news = NewsData('XOM', 'exxon mobil')
df = news.nyt()
# filter news headlines with a keyword list
news.filterz = [ 'exxon', 'mobil', 'oil', 'energy' ]
df = news.filter_data(df)
```

<i> Output </i>


<center><small><small>

| date                | link                                                                                                  | headline                                                                       | description                                                                                                                                                                                                                                                             | tag      | author               |   comments | date_retrieved             | ticker   | newspaper   | search_term   | id                                                                                                                                                                                 | source   |
|:--------------------|:------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|:---------------------|-----------:|:---------------------------|:---------|:------------|:--------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
| 2020-09-08 00:00:00 | /aponline/2020/09/08/business/ap-financial-markets-stocks.html?searchResultPosition=2                 | Exxon, Tesla Fall; Nikola, Beyond Meat Rise                                    | Stocks that moved heavily or traded substantially Tuesday:                                                                                                                                                                                                              | Business | The Associated Press |        nan | 2020-09-16 14:22:13.032245 | XOM      | NYT         | exxon mobil   | NYTExxon, Tesla Fall; Nikola, Beyond Meat Rise/aponline/2020/09/08/business/ap-financial-markets-stocks.html?searchResultPosition=2                                                | nyt      |
| 2020-09-08 00:00:00 | /reuters/2020/09/08/business/08reuters-exxon-mobil-spending-exclusive.html?searchResultPosition=3     | Exclusive: Exxon Downsizes Global Empire as Wall Street Worries About Dividend | Ill-timed bets on rising demand have Exxon Mobil Corp facing a shortfall of about $48 billion through 2021, according to a Reuters tally and Wall Street estimates, a situation that will require the top U.S. oil company to make deep cuts to its staff and projects. | Business | Reuters              |        nan | 2020-09-16 14:22:13.032245 | XOM      | NYT         | exxon mobil   | NYTExclusive: Exxon Downsizes Global Empire as Wall Street Worries About Dividend/reuters/2020/09/08/business/08reuters-exxon-mobil-spending-exclusive.html?searchResultPosition=3 | nyt      |
| 2020-09-03 00:00:00 | /reuters/2020/09/03/business/03reuters-refinery-operations-exxon-beaumont.html?searchResultPosition=4 | Exxon Beaumont, Texas, Refinery Restarts Large Crude Unit: Sources             | Exxon Mobil Corp restarted the large crude distillation unit (CDU) at its 369,024 barrel-per-day (bpd) Beaumont, Texas, refinery on Thursday, said sources familiar with plant operations.                                                                              | Business | Reuters              |        nan | 2020-09-16 14:22:13.032245 | XOM      | NYT         | exxon mobil   | NYTExxon Beaumont, Texas, Refinery Restarts Large Crude Unit: Sources/reuters/2020/09/03/business/03reuters-refinery-operations-exxon-beaumont.html?searchResultPosition=4         | nyt      |
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|


</small></small></center>

<div align = "right">  <a href="#i82">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f83" ><i>NewsData(ticker, keywords).reuters()</i></div>

<ul>
<li>Returns the news headlines from Reuters for the specified keywords.</li>
</ul>

<i> Example </i>

```python
# retrieve news article for a given search term
news = NewsData('XOM', 'exxon mobil')
df = news.reuters()
# filter news headlines with a keyword list
news.filterz = [ 'exxon', 'mobil', 'oil', 'energy' ]
df = news.filter_data(df)
df.drop_duplicates('headline', inplace = True) # Reuters returns duplicate articles if articles were updated after publication...

```

<i> Output </i>


<center><small><small>

| date                | link                   | headline                                                           | description                                                           | date_retrieved             | ticker   |   comments |   author |   tag | newspaper   | search_term   | id                                                                                              | source   |
|:--------------------|:-----------------------|:-------------------------------------------------------------------|:----------------------------------------------------------------------|:---------------------------|:---------|-----------:|---------:|------:|:------------|:--------------|:------------------------------------------------------------------------------------------------|:---------|
| 2020-09-16 00:00:00 | /article/idUSL4N2GD12G | FACTBOX-Oil refiners shut plants as demand losses may never return | Plc, Exxon Mobil Corp,Viva Energy Group and Ampol Ltd - all welcomed  | 2020-09-16 15:37:54.994138 | XOM      |        nan |      nan |   nan | Reuters     | exxon mobil   | ReutersFACTBOX-Oil refiners shut plants as demand losses may never return/article/idUSL4N2GD12G | reuters  |
| 2020-09-15 00:00:00 | /article/idUSKBN26707N | U.S. presidential candidate Biden rips Trump's record on ethanol   | Exxon Mobil Corp and billionaire investor Carl Icahn.Biden's team has | 2020-09-16 15:37:54.994138 | XOM      |        nan |      nan |   nan | Reuters     | exxon mobil   | ReutersU.S. presidential candidate Biden rips Trump's record on ethanol/article/idUSKBN26707N   | reuters  |
| 2020-09-15 00:00:00 | /article/idUSKBN2660I3 | Column: Australia still addicted to fossil fuel with oil, gas subsidies - Russell | for subsidising the four oil refineries, owned by BP Plc, Exxon Mobil | 2020-09-16 15:37:54.994138 | XOM      |        nan |      nan |   nan | Reuters     | exxon mobil   | ReutersColumn: Australia still addicted to fossil fuel with oil, gas subsidies - Russell/article/idUSKBN2660I3 | reuters  |
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|

</small></small></center>

<div align = "right">  <a href="#i83">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


#### <div id = "f84" ><i>NewsData(ticker, keywords).seeking\_alpha()</i></div>

<ul>
<li>Returns the news headlines from Seeking Alpha for the specified keywords.</li>
</ul>

<i> Example </i>

```python
# retrieve news article for a given search term
news = NewsData('XOM', 'exxon mobil')
df = news.seeking_alpha()
# filter news headlines with a keyword list
news.filterz = [ 'exxon', 'mobil', 'oil', 'energy' ]
df = news.filter_data(df)
```
<i> Output </i>


<center><small><small>

| date                | link                                                                                                                                                                                         | headline                                                    | author   | comments   | date_retrieved             | ticker   |   description |   tag | newspaper   | search_term   | id                                                                                                                                                                                                                                                               | source   |
|:--------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------|:---------|:-----------|:---------------------------|:---------|--------------:|------:|:------------|:--------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
| 2020-09-15 00:00:00 | /news/3614409-options-traders-pricing-in-exxon-dividend-cut-analyst-says?source=content_type:react\|section:News\|sectionAsset:News\|first\_level\_url:symbol\|button:Author\|lock\_status:No\|line:1 | Options traders pricing in Exxon dividend cut, analyst says | SA News  | 0 comments | 2020-09-16 15:14:23.575898 | XOM      |           nan |   nan | SA - News   | exxon mobil   | SA - NewsOptions traders pricing in Exxon dividend cut, analyst says/news/3614409-options-traders-pricing-in-exxon-dividend-cut-analyst-says?source=content_type:react\|section:News\|sectionAsset:News\|first\_level\_url:symbol\|button:Author\|lock\_status:No\|line:1 | sa       |
| 2020-09-14 00:00:00 | /news/3613801-connecticut-latest-state-to-sue-exxon-over-climate-change?source=content_type:react\|section:News\|sectionAsset:News\|first\_level\_url:symbol\|button:Author\|lock\_status:No\|line:2  | Connecticut latest state to sue Exxon over climate change   | SA News  | 0 comments | 2020-09-16 15:14:23.575898 | XOM      |           nan |   nan | SA - News   | exxon mobil   | SA - NewsConnecticut latest state to sue Exxon over climate change/news/3613801-connecticut-latest-state-to-sue-exxon-over-climate-change?source=content_type:react\|section:News\|sectionAsset:News\|first\_level\_url:symbol\|button:Author\|lock\_status:No\|line:2 | sa       |
| 2020-09-10 00:00:00 | /news/3612953-exxon-rated-new-buy-mkm-shares-slip?source=content_type:react\|section:News\|sectionAsset:News\|first\_level\_url:symbol\|button:Author\|lock\_status:No\|line:3                         | Exxon rated new Buy at MKM but shares slip                  | SA News  | 0 comments | 2020-09-16 15:14:23.575898 | XOM      |           nan |   nan | SA - News   | exxon mobil   | SA - NewsExxon rated new Buy at MKM but shares slip/news/3612953-exxon-rated-new-buy-mkm-shares-slip?source=content_type:react|section:News|sectionAsset:News|first_level_url:symbol|button:Author|lock_status:No|line:3                                         | sa       |
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|



</small></small></center>

<div align = "right">  <a href="#i84">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f85" ><i>NewsData(ticker, keywords).wsj()</i></div>

<ul>
<li>Returns the news headlines from the Wall Street Journal for the specified keywords.</li>
</ul>

<i> Example </i>

```python
# retrieve news article for a given search term
news = NewsData('XOM', 'exxon mobil')
df = news.wsj()
# filter news headlines with a keyword list
news.filterz = [ 'exxon', 'mobil', 'oil', 'energy' ]
df = news.filter_data(df)
```

<i> Output </i>


<center><small><small>


| date                | link                                                                                                                       | headline                                                         | description                                                                                                                                                                                                     | author                  | tag                 | date_retrieved             | ticker   | newspaper   | search_term   | id                                                                                                                                                                                            |   comments | source   |
|:--------------------|:---------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------|:--------------------|:---------------------------|:---------|:------------|:--------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|:---------|
| 2020-09-13 00:00:00 | /articles/exxon-used-to-be-americas-most-valuable-company-what-happened-oil-gas-11600037243?mod=searchresults&page=1&pos=1 | Exxon Used to Be America’s Most Valuable Company. What Happened? | The oil giant doubled down on oil and gas at what now looks to be the worst possible time. Investors are fleeing and workers are grumbling about the direction of a company some see as out of touch.           | Christopher M. Matthews | Business            | 2020-09-16 15:19:39.733511 | XOM      | WSJ         | exxon mobil   | WSJExxon Used to Be America’s Most Valuable Company. What Happened?/articles/exxon-used-to-be-americas-most-valuable-company-what-happened-oil-gas-11600037243?mod=searchresults&page=1&pos=1 |        nan | wsj      |
| 2020-09-10 00:00:00 | /articles/oil-major-bp-gives-a-taste-of-how-it-will-go-green-11599745648?mod=searchresults&page=1&pos=2                    | Oil Major BP Gives a Taste of How It Will Go Green               | A deal to buy into wind farms off the coast of New York and Massachusetts showcases the British company’s ambitions in the clean-energy sector—and the risks it is taking.                                      | Rochelle Toplensky      | Heard on the Street | 2020-09-16 15:19:39.733511 | XOM      | WSJ         | exxon mobil   | WSJOil Major BP Gives a Taste of How It Will Go Green/articles/oil-major-bp-gives-a-taste-of-how-it-will-go-green-11599745648?mod=searchresults&page=1&pos=2                                  |        nan | wsj      |
| 2020-09-08 00:00:00 | /articles/oil-prices-drop-on-faltering-recovery-in-demand-11599562101?mod=searchresults&page=1&pos=3                       | Oil Prices Tumble on Faltering Recovery in Demand                | Oil prices slumped to their lowest level in nearly three months, under pressure from a stalling recovery in demand and planned production expansions by OPEC that threaten to add to an existing glut of crude. | Joe Wallace             | Oil Markets         | 2020-09-16 15:19:39.733511 | XOM      | WSJ         | exxon mobil   | WSJOil Prices Tumble on Faltering Recovery in Demand/articles/oil-prices-drop-on-faltering-recovery-in-demand-11599562101?mod=searchresults&page=1&pos=3                                      |        nan | wsj      |
|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|


</small></small></center>

<div align = "right">  <a href="#i85">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _


## <div id="A8">Other data</div>


<div align="right"><a href="#0">Back to top</a> </div>


#### <div id = "f86" ><i>nasdaq\_tickers()</i></div>

<ul>
<li>Returns dataframe of tickers traded on the Nasdaq exchange.</li>
</ul>

<i> Example </i>

```python
nasdaq_tickers()
```

<i> Output </i>


<center><small><small>

|    | Symbol   | Security Name                                                                                    |
|---:|:---------|:-------------------------------------------------------------------------------------------------|
|  0 | AACG     | ATA Creativity Global - American Depositary Shares, each representing two common shares          |
|  1 | AACQ     | Artius Acquisition Inc. - Class A Common Stock                                                   |
|  2 | AACQU    | Artius Acquisition Inc. - Unit consisting of one ordinary share and one third redeemable warrant |
|  3 | AACQW    | Artius Acquisition Inc. - Warrant                                                                |
|  4 | AAL      | American Airlines Group, Inc. - Common Stock                                                     |
|  ... | ...    | ...        				                                                                           |


</small></small></center>

<div align = "right">  <a href="#i86">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

#### <div id = "f87" ><i>global\_tickers()</i></div>

<ul>
<li>Returns 100.000+ global tickers from Gurufocus.com. Note that companies are listed in different countries or exchanges with different ticker symbols. </li>
</ul>

<i> Example </i>

```python
global_tickers()
```

<i> Output </i>


<center><small><small>

|    | Symbol          | Company                      |
|---:|:----------------|:-----------------------------|
|  0 | QNCO.Israel     | (Y.Z) Queenco Ltd            |
|  1 | ONE.Canada      | 01 Communique Laboratory Inc |
|  2 | DFK.Germany     | 01 Communique Laboratory Inc |
|  3 | OCQLF           | 01 Communique Laboratory Inc |
|  4 | 01C.Poland      | 01Cyberaton SA               |
|  5 | 1PG.Australia   | 1 Page Ltd                   |
|  6 | I8Y.Germany     | 1 Page Ltd                   |
|  8 | 8458.Taiwan     | 1 Production Film Co         |
|  9 | DRI.Austria     | 1&1 Drillisch AG             |
| 10 | DRI.Switzerland | 1&1 Drillisch AG             |
|  ... | ...    | ...        				    |

</small></small></center>

<div align = "right">  <a href="#i87">To index</a> </div>

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

<br>


## <div id="A9"> Sources </div>

<li>Alpha-Vantage, www.alphavantage.co</li>
<li>Barrons, www.barrons.com</li>
<li>Bloomberg, www.bloomberg.com</li>
<li>CNBC, www.cnbc.com</li>
<li>Financial Times, www.ft.com</li>
<li>Finviz, www.finviz.com</li>
<li>Gurufocus, www.gurufocus.com</li>
<li>IEX Cloud, www.iexcloud.io</li>
<li>Investing.com, www.investing.com </li>
<li>MarketWatch, www.marketwatch.com </li>
<li>Macrotrends, www.macrotrends.net</li>
<li>Moore Research Center, www.mrci.com </li>
<li>NASDAQ, www.nasdaq.com</li>
<li>OECD, www.oecd.org</li>
<li>Reuters, www.reuters.com</li>
<li>Seeking Alpha, www.seekingalpha.com</li>
<li>Tiingo, www.tiingo.com</li>
<li>Wall Street Journal, www.wsj.com</li>
<li>Yahoo Finance, www.finance.yahoo.com </li>

<br>

<div align="right"><a href="#0">Back to top</a> </div>

----

## <div id="A10">License</div>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Copyright (c) 2020 Peter la Cour