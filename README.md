# MacroEcon-WrapPy

Economics Wrapper for data across multiple domains and sources (FRED, BEA, BLS, IPUMS, etc.).  The structures allow for smooth workflows for data ingest, transformations, graphing, and modeling.  

This module is used independently of any API-wrapper.  However, some wrappers are suggested and used in the examples.  An API-wrapper Adapter interface is available for improved integration with this module's primary classes.  Where API-wrapper functionality falls short, this module makes direct connections to the site. 


## Install and Configure

Create a file (`SECRETS.yaml`) with all appropriate keys and values.

```bash
pip install macroecon_wrappy
```

## Usage

Select a source and associated wrapper.  For this example, we will use the [fredapi wrapper](https://github.com/mortada/fredapi) with the FRED data source.  The Adapter is provided for this wrapper, but you can create your own if you use a different API-wrapper.

Set the authentication key for the wrapper.

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

Data sources

* internet archive (Adapter)
  - explanation of sources: https://stackoverflow.com/questions/33811582/how-to-access-wayback-machine-programmatically
  - internet archive: https://archive.org/developers/internetarchive/quickstart.html
  - wayback machine: https://github.com/jsvine/waybackpack
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


Functionality

* APIs: https://github.com/bdecon/econ_data/tree/master/APIs
* good formulas
    - FixedIncome: https://github.com/PacktPublishing/Mastering-Python-for-Finance-Second-Edition/tree/master
    - econ: https://github.com/weijie-chen/Econometrics-With-Python/tree/main
    - online econ: https://python-programming.quantecon.org/intro.html
* altair graphs
  - repo: https://github.com/vega/altair
  - recession bars: 
    + https://stackoverflow.com/questions/43482055/how-to-shade-a-region-with-altair
    + https://stackoverflow.com/questions/66820208/altair-python-solid-horizontal-bars-in-the-backgound
    + https://github.com/vega/altair/issues/2214
    + https://stackoverflow.com/questions/53093402/how-to-plot-y-axis-bands-in-altair-charts
    + 
* metric file storage, PyStore
  - update with pyarrow
  - original: https://aroussi.com/post/fast-datastore-for-pandas-time-series-data
* Wrapper adapters and source extractors
* plot digitizers
  - https://github.com/echemdb/svgdigitizer
  - https://github.com/peterstangl/svg2data
  - https://github.com/dilawar/PlotDigitizer


  Investigate

  * us bank reserves(TOTRESNS), MOVE index, china?
  * does financial repression lead to higher p/e ratios?
  * ideas: https://www.bancreek.com/p/us-employment-data-treemap