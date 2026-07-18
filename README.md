# Eight Tests, Eight No-Gos: Screening Online Attention as a Stock Signal

**Recommendation: don't proceed with signal development.** Google Trends and Wikipedia page views show no lead relationship with weekly returns strong enough to act on, for any of four stocks, on either data source, at the pre-registered lag.

***Stack: Python · pandas · scipy · Plotly · Streamlit***

**Live Interactive Dashboard:** 
[**search-trends-vs-stock-returns.streamlit.app**](https://search-trends-vs-stock-returns.streamlit.app/)

*Stock Selector | Data Filter | Live Correlation Recompute*

The screening logic runs live. Narrows the date range and every correlation recomputes on the filtered window, with go/investigate/no-go recommendations updating per stock and per proxy.

-------

## Research Question

An investment advisory firm is considering building a tool around online attention data. Before committing budget, they want one thing answered: **is there a signal here worth chasing?**

## Conclusion

Eight tests. Four stocks (TSLA, NVDA, META, JPM) × two independent attention sources, tested over three years of weekly data (Jan 2022 – Dec 2024).

**All eight came back no-go.**

| Stock | Google Trends (lag 1) | Wikipedia (lag 1) |
|--------|----------------------|-------------------|
| TSLA | +0.0153 | −0.1343 |
| NVDA | −0.0015 | +0.0480 |
| META | +0.0913 | −0.1599 |
| JPM | −0.0375 | +0.0131 |

The largest observed relationship explained approximately 2.6% of weekly return variation, while the smallest explained approximately 0.0002%.

**Recommendation:** do not invest in developing an attention-based signal for these stocks. The results provide no evidence that such a signal would be reliable.

-------

## Pre-Registered Analysis Criteria

Before any data was pulled, a business action bar was fixed:

| Tier | Threshold | Meaning |
|------|-----------|---------|
| **no-go** | \|r\| < 0.20 | Explains under 4% of movement, which is not worth pursuing. |
| **investigate** | 0.20 ≤ \|r\| < 0.40 | Worth a closer look. |
| **go** | \|r\| ≥ 0.40 | Strong enough to build on. |

**A one-week lag was locked as the primary test before any results were seen.**

This  matters as scanning all lags and reporting the best is data dredging. Noise in enough lags will eventually clear any bar. Committing to lag 1 in advance means the reported result is the one that was asked for, not the one that happened to look good.

These thresholds are a *business* action bar, not a statistical convention. They answer a practical question: how strong must a correlation be before a firm should spend money on it?

## Assessing Whether the Sample Size Was Sufficient

The standard objection to any null result falls in the lack of findings due to insufficient sample size. The numbers prove otherwise.

- At n = 154 lag-1 pairs, the smallest correlation reaching statistical significance is **r ≈ 0.158** while the pre-registered threshold is **r = 0.20**.

**Any correlation strong enough to act on would have been detected.** The null reflects an absent signal, not an insufficient sample.

## Two Independent Sources, Same Answer

Two attention proxies were used deliberately, measuring different behaviours:

- **Google Trends** — active search intent. Someone typed the ticker.
- **Wikipedia page views** — passive consumption. Someone read about the company.

Both land inside the no-go band for all four stocks. **The null is robust across two independent measures of attention** — a single-source null could be a quirk of that source. This one isn't.

-------

## Stock Specific Notes

**TSLA:** Common Elon Musk news driven spikes tend to produce same week co-movement rather than a one week lead. The confound is timing not the source of searches. 

**NVDA:** Search volume and returns have been driven in part by the AI narrative, in cases this is a shared external drvier producing same week co-movements rather than a lead.

**JPM:** The weak result is expected form an institutionally traded company and confirms the projects hypothesis.

**META:** No single external noise source on the scale of its peers, so adding a comparable caveat would be unwarranted.

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

| # | Title                     | Type                 | Notes                                     |
|---|---------------------------|----------------------|-------------------------------------------|
| 1 | Time Series (All Stocks)  | Dual-axis line chart | Search volume Vs. Weekly Return per stock. If search led price, spikes would precede return spikes.                                           |
| 2 | Lag Correlation Chart     | Line chart           | Correlation by lag (0-4) for both proxies. If attention led price, a line would clear the 0.20 threshold at lag 1 or beyond                   |
| 3 | Proxy Comparison Chart    | Bar chart            | The two attention sources at lag 0. Wiki is 'stronger' than Trends for three of four stocks, but stronger means less week and neither source clear the threshold        




![Correlation by lag](Charts/lag_correlation_chart.png)


![Time series](Charts/time_series_all_stocks.png)


![Proxy comparison](Charts/proxy_comparison_chart.png)

-------
## Outputs

Pre-run outputs are in /outputs so you can review result without running the notebook:
 
| File                    | Contents                                               |
|-------------------------|--------------------------------------------------------|
| data_aligned.csv        | 155 week aligned dataset (Jan 2022–Dec 2024) per stock, weekly return, Google Trends volume, Wikipedia views, and lagged attention columns.               |
| findings.csv            | 8 rows (4 stocks × 2 proxies) pre-registered lag-1 correlation, lags, and the go/investigate/no-go recommendation per test.                              |

-------

## How to Run
**Notebook**

Open notebook.ipynb in Google Colab or Jupyter and run top to bottom. The data-collection cells call live APIs (Google Trends, Yahoo Finance, Wikimedia), these can be rate-limited, so the raw pulls are saved to CSV and treated as canonical. Use the dataset provided in this project to ensure consistency and reproducibility, as Google Trends normalized index values which can very slightly between API calls.

**Dashboard**

Runs locally with no live API calls (it reads the pre-exported CSVs):
- pip install -r requirements.txt
- streamlit run dashboard.py

Place data_aligned.csv and findings.csv in the same folder as dashboard.py. The dashboard recomputes correlations based on the selected date range, so narrowing the range may change the displayed values.

-------

## Limitations

- Weekly Granularity: A daily analysis might reveal a faster structure that a weekly view averages away. 
- One Three Year Window: A different time period could have behaved differently.
- No Macro Controls: Overall market moves, sector rotation, and volatility regime are not controlled for.
- Lag 2: Needs a pre-specified holdout period before it could be treated as real.
- Public Data Priced In: Any genuine signal in freeling available attention data is plausibly reflected in the price already, a reason to expect a null. 
-------

## Disclaimer 
*This project is for educational and portfolio purposes only. The business context is illustrative and should not be interpreted as investment advice.* 
