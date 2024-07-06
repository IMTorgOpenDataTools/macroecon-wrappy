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
from macroecon_wrappy.auth import Auth
from fredapi import Fred

filepath = Path('tests/data/test-SECRETS.yaml')
auth = Auth(filepath)
fred = Fred(api_key=auth.data['API_KEY_FED'])
```

Using the `FredApi` Adapter enables seemless integration with the rest of the module, in particular, incorporating data series into Measures.

```python
from macroecon_wrappy.adapters import FredApi
from macroecon_wrappy.measure import Measure

FredApi.set_wrapper(fred)
data_metric = FredApi.get_data('GDP')
output_measure = Measure(data_metric)
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
* Measure line on a graph
  - (ie consumer inflation) contains multiple Metrics (cpi, core cpi, pce, bpp, etc.)
  - list of Metrics
  - Metric - continuous timeseries data
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
* nber (Extractor, ...)
  - recessions: https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions
* internet archive (Adapter)
  - explanation of sources: https://stackoverflow.com/questions/33811582/how-to-access-wayback-machine-programmatically
  - internet archive: https://archive.org/developers/internetarchive/quickstart.html
  - wayback machine: https://github.com/jsvine/waybackpack
* yahoo finance (Adapter)
  - MOVE index: https://finance.yahoo.com/quote/%5EMOVE/history/?period1=1672790400&period2=1701648000
* us treasury, additional frb sites
  - treasury home: https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics
  - treasury auction history: https://home.treasury.gov/data/investor-class-auction-allotments
  - 
  - Survey of Consumer Finances (SCF): https://www.federalreserve.gov/econres/scfindex.htm
* macromicro / trading economics
  - jpm global pmi: https://en.macromicro.me/series/20151/jp-morgan-global-manufacturing-pmi
  - jpm global pmi: https://tradingeconomics.com/world/manufacturing-pmi


Wrapper adapters and source extractors

* plot digitizers
  - https://github.com/echemdb/svgdigitizer
  - https://github.com/peterstangl/svg2data
  - https://github.com/dilawar/PlotDigitizer