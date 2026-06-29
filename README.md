# Correlation Analysis 
**Overview**
This project tests whether publicly available online attention (Google Trends search volume and Wikipedia page views) show a lead relationship with weekly stock returns for four large cap stocks (TSLA, NVDA, META, JPM) over a three year period (Jan 2022 to Dec 2024). Three independent data sources were cleaned, aligned to a weekly calendar, and tested at a pre-registered one week lag against a business action bar.

The result is a clean null. None of the eight tests (4 stocks x 2 attention sources) showed a correlation strong enough to act on. The available data did not reliably precede price movement for these stocks in this period. 

This is a correlation and lag analysis study.

Live Dashboard: **search-trends-vs-stock-returns.streamlit.app**

-------

## Business Context

-------

## Methodology
**Three Independent Data Sources**
**Alignment**
**Returns (Not Prices)**
**Pre-Registered Lag 1 Test**

-------

## Key Findings

-------

## Statistics

| # | Title        | Type                     | Notes                        |
|---|--------------|--------------------------|------------------------------|
| 1 | Pearson r    | Histogram + box plot     |                              |
| 2 | Spearman r   | Bar + std dev error bars |                              |

-------

## Stock Specific Notes
**TSLA**
**NVDA**
**JPM**
**META**

-------

## Charts
**Time Series (All Stocks)**
**Lag Correlation Chart**
**Proxy Comparison Chart**

| # | Title                     | Type                     | Notes                        |
|---|---------------------------|--------------------------|------------------------------|
| 1 | Time Series (All Stocks)  | Histogram + box plot     |                              |
| 2 | Lag Correlation Chart     | Bar + std dev error bars |                              |
| 3 | Proxy Comparison Chart    | Two-panel bar            |                              |

-------

## How to Run
**Notebook**

**Dashboard**

-------

## Outputs

Pre-run outputs are in /outputs so you can review result without running the notebook:
 
| File                    | Contents                                               |
|-------------------------|--------------------------------------------------------|
| summary_stats.csv       | Top-level metrics: mean LOS, std dev, CI, burden rates |
| condition_analysis.csv  | Per-comorbidity mean LOS and prevalence                |
| facility_comparison.csv | Per-facility encounter count, mean LOS, std dev        |

-------

## Limitations

-------

## Disclaimer 

