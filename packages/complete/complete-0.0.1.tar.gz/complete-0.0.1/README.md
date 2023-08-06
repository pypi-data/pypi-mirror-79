# Complete

Complete is a Python library to autocomplete questions using search engines

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install complete.

```bash
pip install complete
```

## Usage

```python
from complete import AutoComplete as AC

results=AC.google_complete("how to")
#returns ['how to lose weight', 'how to increase height',..]
```

For asynchronous usage
```python
from complete import AioAutoComplete as AC
async def main():
    results=await AC.google_complete("how to")
    #returns ['how to lose weight', 'how to increase height',..]
```

## Supported Engines


The library currently supports:
 - Google [google_complete]
 - YouTube [youtube_complete]
 - DuckDuckGo [duckduckgo_complete]
 - Bing [bing_complete]

## License
[MIT](https://pastebin.com/4KS5ERWr)