# Correlation Analysis 
**Overview**
This project tests whether publicly available online attention (Google Trends search volume and Wikipedia page views) show a lead relationship with weekly stock returns for four large cap stocks (TSLA, NVDA, META, JPM) over a three year period (Jan 2022 to Dec 2024). Three independent data sources were cleaned, aligned to a weekly calendar, and tested at a pre-registered one week lag against a business action bar.

The result is a clean null. None of the eight tests (4 stocks x 2 attention sources) showed a correlation strong enough to act on. The available data did not reliably precede price movement for these stocks in this period. 

This is a correlation and lag analysis study.

**Live Interactive Dashboard:** 
[**search-trends-vs-stock-returns.streamlit.app**](https://search-trends-vs-stock-returns.streamlit.app/)

*Stock Selector | Data Filter | Live Correlation Recompute*

-------

## Business Context

The project is framed as a screening exercise for an investment advisory firm asking a practical question: before spending money building a tool around online trends/attention, is there a signal worth chasing?

The ouput is a tiered recommendation per stock per source: 
- no-go    |    r < 0.20   (Not worth pursuing. Explains under 4% of return movement.)
- investigate    |    0.20 <= r < 0.40  (Worth a closer look.)
- go    |    r >= 0.40  (Strong enough to build on.)

These thresholds are a business action bar, not a statistical convention. They are set before any results are seen. It answers how strong a correlation must be before a firm should look further into it. 

-------

## Key Findings

-------

## Stock Specific Notes
**TSLA**
**NVDA**
**JPM**
**META**

-------

## Methodology
**Three Independent Data Sources**
1. Yahoo Finance (yfinance): Daily closing price, auto-adjusted for splits and dividendss
2. Google Trends (pytrends): Invididuals actively searching. A 0-100 weekly relative interest index.
3. Wikipedia Page Views (Wiki REST API): Individual's passive attention.

Note: Two attention sources are used deliberately to gain a more complete and credible result than a single source provides.

**Alignment**

All sources were placed on one weekly Friday anchored calendar (Friday close for prices, summed weekly totals for Wiki Views, re-anchored weekly values for Trends) and combined with an inner join. One trailing partial week was dropped. Final dataset: 155 weeks (0.6% observations lost in the join).

**Returns (Not Prices)**

Stock prices were converted to weekly percent returns before any correlation. Raw prices trend upwards and two upward trending series look correlated even when unrelated, reflecting spurious correlation. Returns strip the trend and isolate genuine week to week movement.

**Pre-Registered Lag 1 Test**

A lag shifts attention backward in time to line up against a later week's return. Lag 1 was locked as the primary test before results were seen. This prevents data dredging (reporting the best one, manufactures findings from noise). Lag 0-4 are computed and shown for exploratory context.

-------

## Statistics

Pearson r is the primary metric with Spearman r as a robustness check (a gap over 0.10 between the two is flagged). r squared is reported for intuition and p-values are deliberately not the headline, with eight tests chances produce 0.4 'significant' results, so effect size drives every decision not significance. 

-------
## Charts
**Time Series (All Stocks)**
**Lag Correlation Chart**
**Proxy Comparison Chart**

| # | Title                     | Type                     | Notes                        |
|---|---------------------------|--------------------------|------------------------------|
| 1 | Time Series (All Stocks)  | Dual-axis line chart    | Search volume Vs. Weekly Return per stock. If search led price, spikes would precede return spikes.                            |
| 2 | Lag Correlation Chart     | Line chart | Correlation by lag (0-4) for both proxies. If attention led price, a line would clear the 0.20 threshold at lag 1 or beyond |
| 3 | Proxy Comparison Chart    | Bar chart           |                              |

-------
## Outputs

Pre-run outputs are in /outputs so you can review result without running the notebook:
 
| File                    | Contents                                               |
|-------------------------|--------------------------------------------------------|
| summary_stats.csv       | Top-level metrics: mean LOS, std dev, CI, burden rates |
| condition_analysis.csv  | Per-comorbidity mean LOS and prevalence                |
| facility_comparison.csv | Per-facility encounter count, mean LOS, std dev        |

-------

## How to Run
**Notebook**

**Dashboard**

-------

## Limitations

-------

## Disclaimer 

