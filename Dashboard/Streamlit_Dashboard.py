#Section 9: Streamlit Dashboard 
#Upload Libraries 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
from scipy import stats
from pathlib import Path

#Page Setup
st.set_page_config(
    page_title = "Search Trends vs. Stock Prices",
    layout = "wide"
)

#Data Loading 
@st.cache_data
def load_data():
    try:
        base_dir = Path(__file__).parent
        df = pd.read_csv(base_dir / "data_aligned.csv",
                         index_col='week_end_date',
                         parse_dates=True)
        findings = pd.read_csv(base_dir / "findings.csv")
        return df, findings
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        st.stop()

df_aligned, findings_df = load_data()

#Sidebar Controls 
st.sidebar.title("Controls")
st.sidebar.markdown("---")

selected_stock = st.sidebar.selectbox(
    "Select Stock",
    options=['TSLA', 'NVDA', 'META', 'JPM'],
    index=0,
    help="Select a stock to analyse."
)

min_date = df_aligned.index.min().date()
max_date = df_aligned.index.max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value = (min_date, max_date),
    min_value = min_date,
    max_value = max_date
)

selected_proxy = st.sidebar.selectbox(
    "Attention Proxy",
    options = ['Google Trends', 'Wikipedia', 'Both'],
    index = 2,
    help = "Select which attention proxy to display."
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
About this dashboard: 

Signal screening analysis for advisory use case.
Output: go, investigate, no-go per stock per proxy.

Data: Jan '22 to Dec '24. Pre-exported CSVs. 
No live API calls. This is not investment advice.
""")

#Data Filter by data range
if len(date_range) == 2:
    start_filter = pd.Timestamp(date_range[0])
    end_filter = pd.Timestamp(date_range[1])
    df_filtered = df_aligned[start_filter:end_filter]
else:
    df_filtered = df_aligned

#Page Header
st.title("Search Trends vs. Stock Prices")
st.subheader("Does Online Interest Correlate with Market Movements?")
st.markdown("""
Preliminary signal screening analysis. Output: go, investigate, no-go per stock.
*Illustrative business context only. Not investment advice.*
""")

#Top Metrics Row 
col1, col2, col3, col4 = st.columns(4)

stock_findings_trends = findings_df[
    (findings_df['ticker'] == selected_stock) &
    (findings_df['proxy'] == 'Google Trends') 
]
stock_findings_wiki = findings_df[
    (findings_df['ticker'] == selected_stock) &
    (findings_df['proxy'] == 'Wikipedia')
]

with col1:
    st.metric(label="Selected Stock", value=selected_stock)

with col2:
    if not stock_findings_trends.empty:
        r_val = stock_findings_trends['primary_r'].values[0]
        rec = stock_findings_trends['rec'].values[0]
        st.metric(
            label="Trends Lag 1 r",
            value=f"{r_val:+.3f}",
            delta=rec.upper()
        )

with col3:
    if not stock_findings_wiki.empty:
        r_val = stock_findings_wiki['primary_r'].values[0]
        rec = stock_findings_wiki['rec'].values[0]
        st.metric(
            label="Wikipedia Lag 1 r",
            value=f"{r_val:+.3f}",
            delta=rec.upper()
        )

with col4:
    n_obs = len(df_filtered)
    st.metric(label="Weekly Observations", value=n_obs)

#Chart 1: Dual Axis Time Series 
st.subheader(f"Does {selected_stock} Search Volume Lead Weekly Returns?")

trends_col = f"{selected_stock}_trends_lag0" 
return_col = f"{selected_stock}_return"
wiki_col = f"{selected_stock}_wiki_views"

fig_ts = make_subplots(specs=[[{"secondary_y": True}]])

if return_col in df_filtered.columns:
    fig_ts.add_trace(
        go.Scatter(
            x = df_filtered.index,
            y = df_filtered[return_col],
            name = 'Weekly Return (%)',
            line = dict(color = 'rgba(255,140,0,0.7)', width = 1.5),
            hovertemplate = '%{x|%Y-%m-%d}<br>Return: %{y:.2f}%<extra></extra>'
        ),
        secondary_y = True
    )

if selected_proxy in ['Google Trends', 'Both']:
    if trends_col in df_filtered.columns:
        fig_ts.add_trace(
            go.Scatter(
                x=df_filtered.index,
                y=df_filtered[trends_col],
                name='Google Trends Volume',
                line=dict(color='steelblue', width=2),
                hovertemplate='%{x|%Y-%m-%d}<br>Trends: %{y:.0f}<extra></extra>'
            ),
            secondary_y=False
        )

if selected_proxy in ['Wikipedia', 'Both']:
    if wiki_col in df_filtered.columns:
        wiki_series = df_filtered[wiki_col]
        wiki_normalised = (wiki_series - wiki_series.min()) / \
                          (wiki_series.max() - wiki_series.min()) * 100
        fig_ts.add_trace(
            go.Scatter(
                x=df_filtered.index,
                y=wiki_normalised,
                name='Wikipedia Views (normalised)',
                line=dict(color='mediumseagreen', width=2, dash='dot'),
                hovertemplate='%{x|%Y-%m-%d}<br>Wiki (norm): %{y:.1f}<extra></extra>'
            ),
            secondary_y=False
        )

fig_ts.add_hline(y=0, line_dash="dash", line_color="black",
                  opacity=0.3, secondary_y=True)

fig_ts.update_yaxes(title_text="Search Volume (0-100)", secondary_y=False)
fig_ts.update_yaxes(title_text="Weekly Return (%)", secondary_y=True)
fig_ts.update_layout(
    height=400,
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
    plot_bgcolor='white',
    paper_bgcolor='white'
)
fig_ts.update_xaxes(showgrid=True, gridcolor='lightgrey')
fig_ts.update_yaxes(showgrid=True, gridcolor='lightgrey')

st.plotly_chart(fig_ts, use_container_width=True)

#Chart 2: Lag Correlation Chart 
st.markdown("---")
st.subheader("Lag Structure: Pre-registered vs. Exploratory")
st.info("""
Pre-registered finding: (Lag 1) Does search volume from last week 
correlate with returns this week? This lag was locked before analyzing the data to test 
the core hypothesis: does online attention lead price movement?

Exploratory context below: The chart shows correlations across lags 0–4 for 
transparency. These exploratory results help identify any temporal structure in the data, 
but they are not the headline finding. Scanning multiple lags and reporting whichever 
looks strongest would amount to data dredging. The pre-registered lag 1 test is the actual test of the hypothesis.
""")

st.subheader(f"At Which Lag Does Search Volume Most Correlate With {selected_stock} Returns?")

##Calculate Lag Correlation for Display

lag_range_display = range(0,5)
lag_r_trends = []
lag_r_wiki = []

##Trends
for lag in lag_range_display:
    trends_lag_col = f"{selected_stock}_trends_lag{lag}"
    wiki_lag_col = f"{selected_stock}_wiki_lag{lag}"

    if trends_lag_col in df_filtered.columns and return_col in df_filtered.columns:
        pair = df_filtered[[trends_lag_col, return_col]].dropna()
        if len(pair) >= 10:
            r,_ = stats.pearsonr(pair[trends_lag_col], pair[return_col])
            lag_r_trends.append(r)
        else:
            lag_r_trends.append(None)
    else:
        lag_r_trends.append(None)

##Wiki
    if wiki_lag_col in df_filtered.columns and return_col in df_filtered.columns:
        pair = df_filtered[[wiki_lag_col,return_col]].dropna()
        if len(pair) >= 10:
            r, _ = stats.pearsonr(pair[wiki_lag_col], pair[return_col])
            lag_r_wiki.append(r)
        else:
            lag_r_wiki.append(None)
    else: 
        lag_r_wiki.append(None)

fig_lag = go.Figure()

lags_list = list(lag_range_display)

if selected_proxy in ['Google Trends', 'Both']:
    fig_lag.add_trace(go.Scatter(
        x = lags_list, y = lag_r_trends,
        mode = 'lines+markers',
        name = 'Google Trends',
        line = dict(color='steelblue', width =2),
        marker=dict(size=8)
    ))

if selected_proxy in ['Wikipedia', 'Both']:
    fig_lag.add_trace(go.Scatter(
        x=lags_list, y=lag_r_wiki,
        mode='lines+markers',
        name='Wikipedia',
        line=dict(color='mediumseagreen', width=2,dash='dot'),
        marker=dict(size=8,symbol='square')
    ))

##Threshold Reference Line
fig_lag.add_hline(y=0.20,line_dash="dot",line_color="green",
    annotation_text="investigate threshold (r=0.20)", opacity=0.6)
fig_lag.add_hline(y=0.40, line_dash="dot",line_color="darkgreen",
    annotation_text="go threshold (r=0.40)", opacity=0.6)
fig_lag.add_hline(y=0, line_color="black", opacity=0.4)

fig_lag.update_layout(
    xaxis_title = "Lag (weeks): Positive = Search leads price",
    yaxis_title = "Pearson r",
    height = 350,
    plot_bgcolor = "white",
    paper_bgcolor = "white"
)
fig_lag.update_xaxes(tickvals=lags_list, showgrid=True, gridcolor="lightgrey")
fig_lag.update_yaxes(showgrid=True, gridcolor="lightgrey", range=[-0.6, 0.6])
st.plotly_chart(fig_lag, use_container_width = True)

#Summary Table 
st.subheader("Correlation Summary (All Stocks)")
##Build Display Table from Findings
summary_display = findings_df.copy()
summary_display['r²'] = (summary_display['primary_r'] ** 2).round(4)
summary_display['primary_r'] = summary_display['primary_r'].round(4)
summary_display = summary_display.rename(columns={
    'ticker': 'Stock',
    'proxy': 'Proxy',
    'primary_r': 'Primary r (lag 1)',
    'r²': 'r²',
    'primary_lag': 'Primary Lag (weeks)',
    'best_explor_lag': 'Best Exploratory Lag',
    'rec': 'Recommendation'
})

##Colour Code Recommendation Column
def colour_recommendation(val):
    if val == 'go':
        return 'background-color: #c8e6c9'
    elif val == 'investigate':
        return 'background-color: #fff9c4'
    else:
        return 'background-color: #ffcdd2'

styled_table = summary_display.style.map(
    colour_recommendation, subset=['Recommendation']
)

st.dataframe(styled_table, use_container_width=True)

#Text Output (per selected stock)
st.subheader(f"Analytical Conclusion: {selected_stock}")

conclusions = {}
for ticker in ['TSLA', 'NVDA', 'META', 'JPM']:
    t_row = findings_df[(findings_df['ticker'] == ticker) & (findings_df['proxy'] == 'Google Trends')]
    w_row = findings_df[(findings_df['ticker'] == ticker) & (findings_df['proxy'] == 'Wikipedia')]
    t_rec = t_row['rec'].values[0] if not t_row.empty else 'no-go'
    t_r = t_row['primary_r'].values[0] if not t_row.empty else 0
    t_lag = t_row['primary_lag'].values[0] if not t_row.empty else 0
    w_rec = w_row['rec'].values[0] if not w_row.empty else 'no-go'

    if t_rec == 'no-go' and w_rec == 'no-go':
        conclusion =  (f"{ticker}: No meaningful correlation found in either proxy "
                      f"(Google Trends r = {t_r:+.3f}). No-go for both proxies.")
    elif t_rec in ('go', 'investigate'):
        conclusion = (f"{ticker}: {t_rec.capitalize()}."
                      f"Google Trends shows r = {t_r:+.3f} with search leading returns by "
                      f"approximately {t_lag} week(s).")
    else:
        conclusion = (f"{ticker}: Wikipedia proxy warrants investigation "
                      f"({w_rec}). Google Trends signal is weak.")

    conclusions[ticker] = conclusion 

st.info(conclusions.get(selected_stock, "No conclusion available."))

#Confound Caveat for Narrative Driven Stocks
if selected_stock == 'TSLA':
    st.warning("""
    TSLA: Search spikes can be driven by Elon Musk's personal news,
    which tend to produce same week co-movements, not a lag 1 lead relationship.
    """)
elif selected_stock == 'NVDA':
    st.warning("""
    NVDA: Some correlation may be attributed to a broader AI narrative cycle showing up in both
    search trends and price movement, not a search leading price relationship.
    """)
elif selected_stock == 'JPM':
    st.info("""
    JPM: Weak correlation is expected as larger banks tend to move more on 
    fundamentals than search interest.
    """)

st.markdown("---")
st.caption("""
This dashboard is for portfolio purposes and is not investment advice.
Analysis period is Jan 2022 to Dec 2024.
""")