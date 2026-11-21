
# Data Extraction Module Design

Version: 0.2
Status: Draft

## 1. Purpose

A data extraction module that takes configurable request parameters, retrieves historical financial market data with an authenticated REST API, and returns a deserialized Python dictionary

The module supports both an individual security extraction and bulk market data extraction while operating within the external API's request rate limitations

## 2. Scope

### 2.1 Inside Scope 
Retrieve API credentials	
Construct endpoint URLs	
Construct HTTP headers	
Configure query parameters	
Send HTTP requests	
Handle request timeouts	
Handle HTTP errors	
Handle rate limits	
Deserialize JSON responses	
- Support ticker-based historical data extraction
- Support date-based bulk market data extraction
- Enforce API request rate limits proactively
- Implement bounded retries for transient request failures
- Support multiple extraction endpoint types

### 2.2 Outside Scope
- Sector and industry classification
- Statistical correlation modeling
- Predictive selection of related securities
- Database availability checks
- Background request scheduling
- Data normalization and validation
- Database insertion
- Financial analysis and visualization

## 3. Module Inputs

### 3.1 Custom Bars Endpoint

- Ticker symbol
- Multiplier
- Timespan
- Start date
- End date
- Adjusted
- Sort

### 3.2 Grouped Daily Endpoint

- Trading date
- Adjusted
- Include OTC securities

### 3.3 Shared Configuration

- API credential
- Request timeout
- Maximum retry attempts
- Maximum requests per time window
- Rate limit time window

## 4. Module Outputs

A Python dictionary containing the deserialized API response,
including OHLCV records, timestamps, ticker information and
response metadata.

The response structure may vary depending on the requested
endpoint.

The extraction module shall preserve the original response
structure. Standardization shall occur in the transformation
module.

Failed requests shall produce an explicit error rather than
returning invalid financial data.


## 5. Functional Requirements

- EXT-FR-01: The module shall retrieve an API credential from the environment.
- EXT-FR-02: The module shall dynamically construct an aggregate bars endpoint URL.
- EXT-FR-03: The module shall authenticate requests using an HTTP authorization header.
- EXT-FR-04: The module shall support configurable query parameters.
- EXT-FR-05: The module shall execute HTTP GET requests to the financial data provider.
- EXT-FR-06: The module shall inspect returned HTTP status codes.
- EXT-FR-07: The module shall deserialize successful JSON responses into Python dictionaries.
- EXT-FR-08: The module shall handle rate-limited requests using a bounded retry policy.
- EXT-FR-09: The module shall report failed requests to the caller.
- EXT-FR-10: The module shall support ticker-based historical data extraction through the Custom Bars endpoint.
- EXT-FR-11: The module shall support bulk daily market data extraction through the Grouped Daily endpoint.
- EXT-FR-12: The module shall enforce a configurable maximum number of requests within a specified time window.
- EXT-FR-13: The module shall apply a shared rate limit across all supported endpoints and retry attempts.
- EXT-FR-14: The module shall support bounded retries for transient network and server failures.
- EXT-FR-15: The module shall distinguish successful responses containing no market records from failed requests.


## 6. Nonfunctional Requirements

- EXT-NFR-01: API credentials shall not be hardcoded or logged.
- EXT-NFR-02: HTTP requests shall have a configurable timeout.
- EXT-NFR-03: Core functions shall be independently testable.
- EXT-NFR-04: Function names, parameters and return values shall be documented.
- EXT-NFR-05: Functions shall not depend on mutable global request parameters.
- EXT-NFR-06: Shared request logic shall be reusable across supported endpoints.
- EXT-NFR-07: Rate limit settings shall be configurable without modifying core extraction logic.
- EXT-NFR-08: Failed requests shall be logged without exposing API credentials.
- EXT-NFR-09: Retry attempts shall be bounded to prevent indefinite execution.


## 7. Function Decomposition

- fetch_market_bars()
  - load api key() --> retrieve credentials
  - build url() --> construct endpoint
  - build headers() --> prep authentication
  - build params() --> build dict. of additional inputs
  - get request() --> send GET request
  - verify response() --> check and deserialize response
  
## 8. Control Flow and Pseudocode

## 9. Testing Strategy


## 10. Future Enhancements

### 10.1 Security Master

Maintain a database of approximately 1,000 securities,
classified by ticker symbol, sector and industry.

### 10.2 Statistical Relationship Modeling

Calculate statistical relationships between industries
using historical daily returns and Pearson correlation
coefficients.

Support a configurable correlation threshold for identifying
related industries.

Initial experimental threshold: 0.45

### 10.3 Correlation-Based Data Prefetching

Given a requested ticker symbol:

1. Identify its associated industry
2. Identify statistically related industries
3. Retrieve ticker symbols belonging to those industries
4. Determine which financial records are missing locally
5. Select an efficient extraction strategy
6. Schedule additional requests within API rate limits

### 10.4 Intelligent Request Planning

- Prioritize explicit user requests
- Assign lower priority to background prefetching
- Avoid redundant requests for locally available data
- Select between ticker-based and date-based extraction
- Support incremental data retrieval
- Minimize unnecessary network communication

### 10.5 Performance Evaluation

Measure the effectiveness of the data acquisition strategy
using:

- API requests consumed
- Financial records retrieved per request
- Extraction latency
- Local database coverage
- Cache hit rate
- Prefetch hit rate