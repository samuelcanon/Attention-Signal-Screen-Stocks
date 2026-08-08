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
    page_title = "Attention vs. Stock Returns",
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
    "Attention Source",
    options = ['Google Trends', 'Wikipedia', 'Both'],
    index = 2,
    help = "Choose which online attention source to show: Google search interest, Wikipedia reading, or both."
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
About this dashboard: 

Each stock gets a simple call: go, worth a look, or no-go.

Data covers January 2022 to December 2024, loaded from a fixed and saved dataset.
Not a live feed.
""")

#Data Filter by data range
if len(date_range) == 2:
    start_filter = pd.Timestamp(date_range[0])
    end_filter = pd.Timestamp(date_range[1])
    df_filtered = df_aligned[start_filter:end_filter]
else:
    df_filtered = df_aligned

#Page Header
st.title("Attention vs. Stock Returns")
st.subheader("Eight tests, four stocks, two attention sources")
st.markdown("""
A first look at whether online attention predicts next week's stock return, tested against a bar set in advance.
Narrowing the date range in the sidebar updates the chart below live. The top numbers and table reflect the full three-year study.
*Illustrative business context only.*
\n*Use the sidebar on the left to switch between stocks and views.*
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
        rec = stock_findings_trends['recommendation'].values[0]
        st.metric(
            label="Search Interest Match (r)",
            value=f"{r_val:+.3f}",
            delta=rec.upper(),
            delta_color="off"
        )

with col3:
    if not stock_findings_wiki.empty:
        r_val = stock_findings_wiki['primary_r'].values[0]
        rec = stock_findings_wiki['recommendation'].values[0]
        st.metric(
            label="Wikipedia Reading Match (r)",
            value=f"{r_val:+.3f}",
            delta=rec.upper(),
            delta_color="off"
        )

with col4:
    n_obs = len(df_filtered)
    st.metric(label="Weeks of Data", value=n_obs)

#Chart 1: Dual Axis Time Series 
st.subheader(f"Does {selected_stock} Search Interest Predict Next Week's Return?")

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

fig_ts.update_yaxes(title_text="Search Interest (0-100)", secondary_y=False)
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

st.plotly_chart(fig_ts, use_container_width=True, theme=None)

#Chart 2: Lag Correlation Chart 
st.markdown("---")
st.subheader("How Far Back Does Search Predict Price?")
st.info("""
The main test asks whether last week's attention predicts this week's return. Lags 0 and 2 to 4 are shown for context only as picking the best of the results after the 
fact would make the results untrustworthy, the pre-registration at lag 1 exists to prevent this.
""")


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
    annotation_text="worth a closer look (0.20)", opacity=0.6)
fig_lag.add_hline(y=0.40, line_dash="dot",line_color="darkgreen",
    annotation_text="strong enough to act on (0.40)", opacity=0.6)
fig_lag.add_hline(y=0, line_color="black", opacity=0.4)

fig_lag.update_layout(
    xaxis_title = "Weeks between search activity and return (0 = same week)",
    yaxis_title = "Correlation strength (r)",
    height = 350,
    plot_bgcolor = "white",
    paper_bgcolor = "white"
)
fig_lag.update_xaxes(tickvals=lags_list, showgrid=True, gridcolor="lightgrey")
fig_lag.update_yaxes(showgrid=True, gridcolor="lightgrey", range=[-0.6, 0.6])
st.plotly_chart(fig_lag, use_container_width = True, theme=None)

#Summary Table 
st.subheader("How Every Stock Compares")
##Build Display Table from Findings
summary_display = findings_df.copy()
summary_display['r²'] = (summary_display['primary_r'] ** 2 * 100).round(2)
summary_display['primary_r'] = summary_display['primary_r'].round(4)
summary_display = summary_display.rename(columns={
    'ticker': 'Stock',
    'proxy': 'Attention Source',
    'primary_r': 'Correlation (r)',
    'r²': '% of Movement Explained',
    'primary_lag_weeks': 'Delay Tested (weeks)',
    'best_exploratory_lag': 'Strongest Delay Observed (weeks)',
    'best_exploratory_r': 'Strongest r Observed',
    'recommendation': 'Recommendation'
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
st.subheader(f"What This Means for {selected_stock}")

conclusions = {}
for ticker in ['TSLA', 'NVDA', 'META', 'JPM']:
    t_row = findings_df[(findings_df['ticker'] == ticker) & (findings_df['proxy'] == 'Google Trends')]
    w_row = findings_df[(findings_df['ticker'] == ticker) & (findings_df['proxy'] == 'Wikipedia')]
    t_rec = t_row['recommendation'].values[0] if not t_row.empty else 'no-go'
    t_r = t_row['primary_r'].values[0] if not t_row.empty else 0
    t_lag = t_row['primary_lag_weeks'].values[0] if not t_row.empty else 0
    w_rec = w_row['recommendation'].values[0] if not w_row.empty else 'no-go'

    if t_rec == 'no-go' and w_rec == 'no-go':
        conclusion =  (f"{ticker}: Neither search interest nor Wikipedia reading predicts next week's "
                      f"return (search match: {t_r:+.3f}). Recommendation: do not build a signal here.")
    elif t_rec in ('go', 'investigate'):
        conclusion = (f"{ticker}: {t_rec.capitalize()}. "
                      f"Search interest tracks returns {t_lag} week(s) ahead, at a match strength of {t_r:+.3f}.")
    else:
        conclusion = (f"{ticker}: Wikipedia reading is worth a closer look "
                      f"({w_rec}). Search interest alone is too weak to act on.")

    conclusions[ticker] = conclusion 

st.info(conclusions.get(selected_stock, "No conclusion available."))

#Confound Caveat for Narrative Driven Stocks
if selected_stock == 'TSLA':
    st.info("""
    TSLA: Elon Musk's personal news often moves search and price in the same week. That is a
    same week echo not search predicting price a week ahead.
    """)
elif selected_stock == 'NVDA':
    st.info("""
    NVDA: Search and price both move with the broader AI news cycle. They are not predicting the other but rather reacting to the
    same events together.
    """)
elif selected_stock == 'JPM':
    st.info("""
    JPM: A weak result here is expected. Large, established banks tend to move on earnings and
    rates.
    """)

st.markdown("---")
st.caption("""
This dashboard is for portfolio purposes and is not investment advice.
Analysis period is Jan 2022 to Dec 2024.
""")
