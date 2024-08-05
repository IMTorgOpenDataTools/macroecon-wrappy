# MacroEcon-WrapPy

Economics Wrapper for data across multiple domains and sources (FRED, BEA, BLS, IPUMS, etc.).  The structures allow for smooth workflows for data ingest, transformations, graphing, and modeling.  

This module is used independently of any particular API-wrapper.  However, some wrappers are suggested and used in the examples.  An API-wrapper `Adapter` interface is available for improved integration with this module's primary classes.  Where no API-wrapper functionality exists, such as directly downloading files or site scraping, this module makes direct connections to a site by implementing the `Extractor` interface.


## Install and Configure

Create a file (`SECRETS.yaml`) with all appropriate keys and values.

```bash
pip install macroecon_wrappy
```

## Usage

Select a source and associated wrapper.  For this example, we will use the [fredapi wrapper](https://github.com/mortada/fredapi) with the FRED data source.  The Adapter is provided for this wrapper, but you can create your own if you use a different API-wrapper.

Set the authentication key for the wrapper.

Add external libraries using the `--dev` argument, such as:

```bash
pipenv install --dev waybackpack
```


```python
<TODO: add from notebooks/test.ipynb>
```

Using the `FredApi` Adapter enables seemless integration with the rest of the module, in particular, incorporating data series into Measures.

```python
<TODO: add from notebooks/test.ipynb>
```

Work directly with the Measure for various tasks and transformations.



## Test

```bash
pipenv run pytest --collect-only
```


## Develop

Its often best to work with the notebook while quickly developing.

```bash
pipenv install -e .
```

Then simply import into the notebook

```python
import macroecon_wrappy as me
```

But ensure to remove it when done:

```bash
pipenv uninstall macroecon_wrappy
```



## Provisioned API-Wrappers

These API-wrappers are supported by this module with Adapters:

* [fredapi](https://github.com/mortada/fredapi)



## API Structures

* Relation
  - multiple Measures, Epochs, Events related using a mathematical expression
* ~~Measure line on a graph~~
  - (ie consumer inflation) contains multiple Metrics (cpi, core cpi, pce, bpp, etc.)
  - list of Metrics
  - ~~Metric - continuous timeseries data~~
    - pd.Series with metadata
* Epoch polygon on a graph
  - (ie recessions) contain multiple Epochs (expansion, contraction, etc.)
  - pd.DataFrame of Epochs with metadata
  - Span - window of time
    - single row of pd.DataFrame with metadata
* Event dot on a graph
  - (ie fall of enron) contains multiple Points (news articles, blog posts, anecdotes, etc.)
  - pd.DataFrame of Points with metadata
  - Point in time (ie news article)
    - single row of pd.DataFrame with metadata
* Geom abstract structure with metadata

Adapter - interacts with api wrapper to get data
Extractor - interacts with site to get files and extract data


## Roadmap

* ~~Span of duration_days == 0 is Event~~
* Adapters and Extractors should enforce output of 
  - ~~?list of dicts,~~ 
  - ~~with opinionated methods for how to use with data structures (Span, Metric, etc.)~~
  - ~~return raw structure (dict, pd.DataFrame)~~
  - ~~return macroecon structure (Measure, Epoch, Event, Geom)~~
  - ~~enable caching of data using module, top-level config, and work with api-wrappers' own caching~~
* what is load.py doing?  dependencies: RM_sources
* [awesome quant](https://github.com/wilsonfreitas/awesome-quant?tab=readme-ov-file#python)


### Data sources: Adapter, Extractor

* [various APIs](https://github.com/bdecon/econ_data/tree/master/APIs)
  - useful sources: Energy Information Administration (EIA), treasury 
  - additional: IMF, census, UN Comm(odity)Trade,
* [datareader](https://github.com/pydata/pandas-datareader/tree/main/pandas_datareader)
  - list of [sources](https://pydata.github.io/pandas-datareader/stable/remote_data.html#remote-data-tiingo)
  - free api: [enigma](https://www.enigma.com/), [econdb](https://www.econdb.com/)
  - useful sources: tsp, worldbank, oecd, eurostat, fama/french, ...
* ~~internet archive (Adapter)~~
  - need better text integration with plots
* hindenburg
  - headline: https://hindenburgresearch.com/
* treasury, additional frb sites
  - example: https://github.com/bdecon/econ_data/blob/master/APIs/Treasury.ipynb
  - treasury home: https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics
* macromicro / trading economics
  - jpm global pmi: https://en.macromicro.me/series/20151/jp-morgan-global-manufacturing-pmi
  - jpm global pmi: https://tradingeconomics.com/world/manufacturing-pmi
* quandl / nasdaq data link
  - some is free
  - api wrapper: https://github.com/Nasdaq/data-link-python
  - data: https://data.nasdaq.com/search?filters=%5B%22Free%22%5D


### Functionality: graphs, digitizers, transformations, cache / storage, etc.

* [finplot](https://github.com/highfestiva/finplot)
* fixed income
  - [rates](https://github.com/attack68/rateslib)
  - [financepy](https://github.com/domokane/FinancePy)
  - [book code](https://github.com/PacktPublishing/Mastering-Python-for-Finance-Second-Edition/tree/master)
* equities
  - [ta-lib](https://github.com/TA-Lib/ta-lib-python)
* economics
  - [econ](https://github.com/weijie-chen/Econometrics-With-Python/tree/main)
  - [online econ](https://python-programming.quantecon.org/intro.html)
* altair graphs
  - repo: https://github.com/vega/altair
  - [candlestick](https://altair-viz.github.io/gallery/candlestick_chart.html)
  - [update after creation](https://stackoverflow.com/questions/72380726/configure-x-axis-limits-after-chart-creation)
  - ~~shaded regions and recession bars: ~~
    + ~~[vertical](https://stackoverflow.com/questions/43482055/how-to-shade-a-region-with-altair)~~
    + [horizonal](https://stackoverflow.com/questions/66820208/altair-python-solid-horizontal-bars-in-the-backgound)
    + [bars](https://github.com/vega/altair/issues/2214)
    + [discussion](https://stackoverflow.com/questions/53093402/how-to-plot-y-axis-bands-in-altair-charts)
* metric file storage, PyStore
  - update with pyarrow
  - original: https://aroussi.com/post/fast-datastore-for-pandas-time-series-data
* Wrapper adapters and source extractors
* plot digitizers
  - https://github.com/echemdb/svgdigitizer
  - https://github.com/peterstangl/svg2data
  - https://github.com/dilawar/PlotDigitizer
