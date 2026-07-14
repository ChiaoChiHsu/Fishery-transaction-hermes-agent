---
name: get-fishery-data
description: Fetches and filters fishery transaction data from Taiwan Ministry of Agriculture Open Data API.
---

**Introduction**: This skill queries the Taiwan MOA (Ministry of Agriculture) Open Data API for fishery product transaction records, using the Python script [`demo_get.py`](./scripts/demo_get.py) to call the API, paginate through results, and filter them. It accepts date ranges, optional product name/code, and market name to retrieve historical price and quantity data. Records marked as 休市 (market closed) are automatically filtered out.

**Goal**: Return a filtered list of fishery transaction records as a JSON array for downstream processing (e.g., visualization or analysis).

### Parameters

| Parameter      | Type  | Required | Description |
|----------------|-------|----------|-------------|
| `start_date`   | `str` | Yes      | Query start date in ROC calendar format `YYYMMDD` (e.g., Jan 1, 2020 = 1090101) |
| `end_date`     | `str` | Yes      | Query end date in ROC calendar format `YYYMMDD` |
| `product_code` | `str` | Optional | Numeric product code (e.g., `1071`) |
| `product_name` | `str` | Optional | Chinese product name (e.g., `金目鱸`). See `product_name.txt` for valid values. |
| `market_name`  | `str` | Optional | Market name (e.g., `三重`). If omitted, all markets are queried. |
| `api_key`      | `str` | Optional | MOA Open Data API key.  |

- `product_code` and `product_name` must describe same species. Providing only one of them is acceptable.
- For unprovided `product_code` and `product_name`, all species are applied.
- For unprovided `market_name`, all markets are applied.

See [`product_name.txt`](./references/product_name.txt) for the full list of supported fishery product names.  
Parameter `product_name` should match the user's mention to a product name in `api_params.txt`.  
See [`procduct_code_name.json`](./references/proudct_code_name.json) to clearify correct product names and product codes.  



### Get Fishery Data from Provided Python Tool
Tool python file: [`demo_get.py`](./scripts/demo_get.py)  
`FisheryQueryParams()` verify the parameters.  
`get_fishery_data()` get the json data by using verified parameters.  

```python
from demo_get import get_fishery_data, FisheryQueryParams

params = FisheryQueryParams(
    start_date="1090101",
    end_date="1091231",
    product_name="金目鱸",
    market_name="三重",
    api_key="YOUR_API_KEY"
)
data = get_fishery_data(params)
```


### Pagination Logic (`Next` field and `while` loop)

The MOA API returns results one page at a time. Each JSON response contains two relevant keys:
- `Data`: the list of records for the current page.
- `Next`: a truthy value (e.g. next page number) if more pages remain, or a falsy value (`None`/empty) if the current page is the last one.

`get_fishery_data()` walks all pages with this flow:
1. **First request** (no `page` param): fetch page 1, read `Data` into `raw_data` and read `Next` into `_next`. Filter out `休市` records and seed `all_filtered_data`.
2. **`while _next:` loop**: as long as `_next` is truthy, the loop body runs:
   - Increment `page` and set `api_params["page"] = str(page)` so the next request asks for the next page.
   - Request that page, then overwrite `_next` with the new response's `Next` value.
   - Filter `休市` records out of the page's `Data` and `extend` them onto `all_filtered_data`.
3. **Loop exit**: once a response's `Next` comes back falsy, `_next` becomes falsy, the `while` condition fails, and the loop ends — `all_filtered_data` now holds every filtered record across all pages.

In short: `Next` acts as the "is there more?" signal from the API, and the `while _next:` loop keeps requesting incrementing `page` values until the API reports no more pages.

### Output Fields

Each record in the returned JSON array contains:

| Field             | Description                        |
|-------------------|------------------------------------|
| `TransDate`       | Transaction date (`YYYMMDD` format) |
| `SeafoodProdName` | Product name (Chinese)             |
| `SeafoodProdCode` | Product code                       |
| `MarketName`      | Market name                        |
| `Avg_Price`       | Average price (TWD/kg)             |
| `Upper_Price`     | Upper price (TWD/kg)               |
| `Middle_Price`    | Middle price (TWD/kg)              |
| `Lower_Price`     | Lower price (TWD/kg)               |
| `Trans_Quantity`  | Transaction quantity (kg)          |

### Requirements in `demo_get.py`
- Ensure the `requests` library is installed (`pip install requests` or use system package).
- Network connectivity to `data.moa.gov.tw` is required. If DNS resolution fails, check your internet connection or configure a proxy.
- The API key must be valid.
- API Endpoint: `GET https://data.moa.gov.tw/api/v1/FisheryProductsTransType/`  
- json_path: file path of saving gotten fishery data. You have to ask user to save at the right path.

**Pitfalls & Workarounds**
- The MOA Open Data API may present an invalid SSL certificate, causing `requests` to raise `SSLError`. To bypass verification, pass `verify=False` to `requests.get`, or alternatively use `curl -k` (insecure TLS) when manually fetching data. This is safe in this trusted environment but should be avoided for untrusted hosts.
- If you encounter empty results, verify that the date range uses ROC calendar (YYYMMDD) and that the product/market names are correct as listed in the `references/product_name.txt`.
- The API may enforce rate limits; if you receive HTTP 429, add a short sleep (e.g., `time.sleep(1)`) between page requests.

- Ensure the `requests` library is installed (`pip install requests` or use system package).
- Network connectivity to `data.moa.gov.tw` is required. If DNS resolution fails, check your internet connection or configure a proxy.
- The API key must be valid.
- API Endpoint: `GET https://data.moa.gov.tw/api/v1/FisheryProductsTransType/`  
- json_path: file path of saving gotten fishery data. You have to ask user to save at the right path.  
### Reference Implementation

See [`scripts/demo_get.py`](./scripts/demo_get.py) for a complete working example including saving results to a local JSON file.
