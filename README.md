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

Using the `FredApi` Adapter enables seemless integration with the rest of the module, in particular, incorporating them into Measures.

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


## Provisioned API-Wrappers

These API-wrappers are supported by this module with Adapters:

* [fredapi](https://github.com/mortada/fredapi)