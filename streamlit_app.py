import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(
    page_title="Lyme Disease Climate Dashboard",
    layout="wide"
)

st.markdown(
    """
    <style>
    /* -----------------------------
       Global page styling
    ----------------------------- */

    html, body, [class*="css"] {
        font-family: Helvetica, Arial, sans-serif !important;
    }

    .stApp {
        background-color: #ffffff !important;
        color: #111111 !important;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        padding-left: 4rem;
        padding-right: 4rem;
        max-width: 1400px;
        position: relative;
        z-index: 2;
    }

    /* -----------------------------
       Red concentric arc background
    ----------------------------- */

    .stApp::before {
        content: "";
        position: fixed;
        top: -220px;
        right: -260px;
        width: 620px;
        height: 620px;
        border-radius: 50%;
        border: 72px solid rgba(217, 71, 75, 0.88);
        z-index: 0;
        pointer-events: none;
    }

    .stApp::after {
        content: "";
        position: fixed;
        bottom: -260px;
        left: -280px;
        width: 720px;
        height: 720px;
        border-radius: 50%;
        border: 80px solid rgba(217, 71, 75, 0.72);
        z-index: 0;
        pointer-events: none;
    }

    /* -----------------------------
       Typography
    ----------------------------- */

    h1 {
        font-family: Helvetica, Arial, sans-serif !important;
        font-size: 3rem !important;
        font-weight: 500 !important;
        line-height: 1.08 !important;
        letter-spacing: -0.04em !important;
        color: #111111 !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-family: Helvetica, Arial, sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.025em !important;
        color: #111111 !important;
        border: 1.5px solid #111111;
        padding: 0.65rem 1rem;
        background-color: rgba(255, 255, 255, 0.94);
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        font-family: Helvetica, Arial, sans-serif !important;
        font-size: 1.25rem !important;
        font-weight: 500 !important;
        color: #111111 !important;
    }

    p, li, label, div, span {
        font-family: Helvetica, Arial, sans-serif !important;
    }

    /* -----------------------------
       Cards / content boxes
    ----------------------------- */

    .section-card {
        border: 1.5px solid #111111;
        background-color: rgba(255, 255, 255, 0.96);
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
        color: #111111 !important;
    }

    .intro-card {
        border-left: 12px solid #d9474b;
        border-top: 1.5px solid #111111;
        border-right: 1.5px solid #111111;
        border-bottom: 1.5px solid #111111;
        background-color: rgba(255, 255, 255, 0.97);
        padding: 1.5rem 1.6rem;
        margin-top: 1.4rem;
        margin-bottom: 1.5rem;
        color: #111111 !important;
    }

    .intro-title {
        font-size: 2.35rem;
        font-weight: 600;
        line-height: 1.08;
        letter-spacing: -0.035em;
        color: #d9474b;
        margin-bottom: 0.6rem;
    }

    .intro-body {
        font-size: 1rem;
        line-height: 1.55;
        color: #111111;
        max-width: 980px;
    }

    .note-card {
        border-left: 8px solid #d9474b;
        background-color: rgba(255, 255, 255, 0.96);
        padding: 1rem 1.25rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 0 1px #111111;
        color: #111111 !important;
    }

    .metric-card {
        border: 1.5px solid #111111;
        background-color: #ffffff;
        padding: 1rem;
        min-height: 110px;
        color: #111111 !important;
    }

    /* -----------------------------
       Sidebar styling
    ----------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1.5px solid #111111 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #111111 !important;
        font-family: Helvetica, Arial, sans-serif !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #111111 !important;
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #111111 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #111111 !important;
        background-color: #ffffff !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label * {
        color: #111111 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSlider"] * {
        color: #111111 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stCheckbox"] * {
        color: #111111 !important;
    }

    /* -----------------------------
       Buttons, widgets, and charts
    ----------------------------- */

    .stButton > button {
        border: 1.5px solid #111111 !important;
        background-color: #ffffff !important;
        color: #111111 !important;
        border-radius: 0 !important;
        font-family: Helvetica, Arial, sans-serif !important;
    }

    .stButton > button:hover {
        border-color: #d9474b !important;
        color: #d9474b !important;
    }

    div[data-testid="stAltairChart"] {
        background-color: rgba(255, 255, 255, 0.96);
        border: 1.5px solid #111111;
        padding: 1rem;
        margin-bottom: 1.5rem;
    }

    hr {
        border: none;
        border-top: 1.5px solid #111111;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    /* -----------------------------
       Fix dark-mode inherited text
    ----------------------------- */

    .stMarkdown, .stText, .stCaption {
        color: #111111 !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #111111 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="middle-ring"></div>

    <style>
    .middle-ring {
        position: fixed;
        top: 70%;
        left: 42%;
        width: 520px;
        height: 520px;
        border-radius: 50%;
        border: 64px solid rgba(217, 71, 75, 0.42);
        z-index: 0;
        pointer-events: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Color palette
# -----------------------------

LYME_RED = "#d9474b"
TEMP_RED = "#c85c5c"
MOUSE_RED = "#a94442"
RAW_LINE = "#d7b3b3"
RAW_POINT = "#caa4a4"
DARK = "#111111"
LIGHT_GRAY = "#e6e6e6"

# -----------------------------
# Sidebar controls
# -----------------------------

st.sidebar.title("Dashboard Controls")

section = st.sidebar.radio(
    "Dashboard section",
    [
        "Overview",
        "National Trends",
        "State Heatmap",
        "State Explorer",
        "Comparative Scatterplots",
        "Insights"
    ]
)

year_range = st.sidebar.slider(
    "Year range",
    min_value=1992,
    max_value=2023,
    value=(1992, 2023)
)

intro_trend_type = st.sidebar.selectbox(
    "Intro Lyme trend view",
    [
        "Raw trendline",
        "Moving average",
        "Binomial filter"
    ]
)

show_raw = st.sidebar.checkbox("Show raw yearly values", value=True)
show_binomial = st.sidebar.checkbox("Show binomial filter", value=True)

# -----------------------------
# Page header
# -----------------------------

st.title("Climate Change and Lyme Disease")

st.markdown(
    """
    <div class="intro-card">
        <div class="intro-title">Everything has been on an increase in the last 3 decades.</div>
        <div class="intro-body">
            This dashboard explores the relationship between reported Lyme disease cases,
            average U.S. state temperature, and white-footed mouse GBIF occurrence records
            from 1992 to 2023. It begins with the core disease trend before moving into
            climate and reservoir-host comparisons.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    # Lyme data is an Excel (.xlsx) file -- use read_excel, not read_csv
    lyme_wide = pd.read_excel(
        "/workspaces/termproject-lyme/Files/lyme_1992_2023_state_year_cases_wide_clean.xlsx"
    )

    lyme = lyme_wide.melt(
        id_vars="State",
        var_name="year",
        value_name="lyme_cases"
    )

    lyme = lyme.rename(columns={"State": "state"})
    lyme["year"] = lyme["year"].astype(int)
    lyme["lyme_cases"] = pd.to_numeric(lyme["lyme_cases"], errors="coerce").fillna(0)

    # Temperature CSV
    temp = pd.read_csv(
        "/workspaces/termproject-lyme/Files/combined_state_average_temperature_1992_2023_all_states.csv",
        encoding="latin1"
    )
    temp["year"] = temp["year"].astype(int)
    temp["avg_temp_F"] = pd.to_numeric(temp["avg_temp_F"], errors="coerce")

    # Mouse CSV
    mouse = pd.read_csv(
        "/workspaces/termproject-lyme/Files/gbif_white_footed_mouse_state_year_1992_2023.csv",
        encoding="latin1"
    )
    mouse["year"] = mouse["year"].astype(int)
    mouse["white_footed_mouse_occurrence_records"] = pd.to_numeric(
        mouse["white_footed_mouse_occurrence_records"],
        errors="coerce"
    ).fillna(0)

    return lyme, temp, mouse

lyme, temp, mouse = load_data()

# ============================================================
# NATIONAL YEARLY SERIES
# ============================================================

national_lyme = (
    lyme.groupby("year", as_index=False)["lyme_cases"]
    .sum()
    .sort_values("year")
)

national_temp = (
    temp.groupby("year", as_index=False)["avg_temp_F"]
    .mean()
    .sort_values("year")
)

national_mouse = (
    mouse.groupby("year", as_index=False)["white_footed_mouse_occurrence_records"]
    .sum()
    .sort_values("year")
)

all_years = pd.DataFrame({"year": list(range(1992, 2024))})

national_lyme = all_years.merge(national_lyme, on="year", how="left")
national_temp = all_years.merge(national_temp, on="year", how="left")
national_mouse = all_years.merge(national_mouse, on="year", how="left")

national_lyme["lyme_cases"] = national_lyme["lyme_cases"].fillna(0)
national_mouse["white_footed_mouse_occurrence_records"] = (
    national_mouse["white_footed_mouse_occurrence_records"].fillna(0)
)

# ============================================================
# MOVING AVERAGE + BINOMIAL FILTER
# ============================================================

national_lyme["lyme_cases_ma5"] = (
    national_lyme["lyme_cases"]
    .rolling(window=5, center=True)
    .mean()
)

weights = np.array([1, 4, 6, 4, 1]) / 16

def binomial_filter(series):
    values = series.to_numpy()

    if len(values) < 5:
        return pd.Series([np.nan] * len(values), index=series.index)

    filtered = np.convolve(values, weights, mode="same")
    filtered[:2] = np.nan
    filtered[-2:] = np.nan

    return pd.Series(filtered, index=series.index)

national_lyme["lyme_cases_binomial"] = binomial_filter(national_lyme["lyme_cases"])
national_temp["avg_temp_F_binomial"] = binomial_filter(national_temp["avg_temp_F"])
national_mouse["mouse_records_binomial"] = binomial_filter(
    national_mouse["white_footed_mouse_occurrence_records"]
)

# ============================================================
# FILTER DATA BY YEAR RANGE
# ============================================================

start_year, end_year = year_range

national_lyme_f = national_lyme[
    (national_lyme["year"] >= start_year) & (national_lyme["year"] <= end_year)
].copy()

national_temp_f = national_temp[
    (national_temp["year"] >= start_year) & (national_temp["year"] <= end_year)
].copy()

national_mouse_f = national_mouse[
    (national_mouse["year"] >= start_year) & (national_mouse["year"] <= end_year)
].copy()

# ============================================================
# COMMON ALTAIR STYLE
# ============================================================

intro_zoom = alt.selection_interval(name="intro_zoom", bind="scales", encodings=["x"])
zoom = alt.selection_interval(name="national_zoom", bind="scales", encodings=["x"])

def style_chart(chart, width=520, height=320):
    return chart.properties(
        width=width,
        height=height,
        background="white"
    ).configure_axis(
        labelFont="Helvetica",
        titleFont="Helvetica",
        gridColor=LIGHT_GRAY,
        domainColor=DARK,
        tickColor=DARK,
        labelColor=DARK,
        titleColor=DARK
    ).configure_title(
        font="Helvetica",
        fontSize=16,
        color=DARK,
        anchor="middle"
    ).configure_view(
        stroke=None
    )

def empty_chart_message(label):
    st.warning(f"Turn on at least one line option to display the {label} chart.")

# ============================================================
# INTRODUCTION LYME-ONLY TREND CHART
# ============================================================

st.markdown("## Disease Trend Overview")

st.markdown(
    """
    <div class="section-card">
    Reported Lyme disease cases form the foundation of this dashboard. Before comparing
    Lyme disease with temperature and white-footed mouse occurrence records, this view
    isolates the national Lyme case trend from 1992 to 2023. Use the sidebar dropdown
    to switch between the raw yearly trend, a 5-year moving average, and a 5-point
    binomial filter.
    </div>
    """,
    unsafe_allow_html=True
)

intro_base = alt.Chart(national_lyme_f).encode(
    x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d"))
)

intro_layers = []

if intro_trend_type in ["Moving average", "Binomial filter"]:
    intro_layers.append(
        intro_base.mark_line(
            color=RAW_LINE,
            strokeWidth=2,
            opacity=0.8
        ).encode(
            y=alt.Y(
                "lyme_cases:Q",
                title="Total Reported Lyme Disease Cases"
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Raw Lyme Cases", format=",")
            ]
        )
    )

    intro_layers.append(
        intro_base.mark_circle(
            color=RAW_POINT,
            size=45,
            opacity=0.75
        ).encode(
            y="lyme_cases:Q",
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Raw Lyme Cases", format=",")
            ]
        )
    )

if intro_trend_type == "Raw trendline":
    intro_layers.append(
        intro_base.mark_line(
            color=LYME_RED,
            strokeWidth=3
        ).encode(
            y=alt.Y(
                "lyme_cases:Q",
                title="Total Reported Lyme Disease Cases"
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Reported Lyme Cases", format=",")
            ]
        )
    )

    intro_layers.append(
        intro_base.mark_circle(
            color=LYME_RED,
            size=55,
            opacity=0.85
        ).encode(
            y="lyme_cases:Q",
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Reported Lyme Cases", format=",")
            ]
        )
    )

elif intro_trend_type == "Moving average":
    intro_layers.append(
        intro_base.mark_line(
            color=LYME_RED,
            strokeWidth=3.5
        ).encode(
            y=alt.Y(
                "lyme_cases_ma5:Q",
                title="Total Reported Lyme Disease Cases"
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases_ma5:Q", title="5-Year Moving Average", format=",.0f"),
                alt.Tooltip("lyme_cases:Q", title="Raw Lyme Cases", format=",")
            ]
        )
    )

elif intro_trend_type == "Binomial filter":
    intro_layers.append(
        intro_base.mark_line(
            color=LYME_RED,
            strokeWidth=3.5
        ).encode(
            y=alt.Y(
                "lyme_cases_binomial:Q",
                title="Total Reported Lyme Disease Cases"
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases_binomial:Q", title="Binomial Filtered Cases", format=",.0f"),
                alt.Tooltip("lyme_cases:Q", title="Raw Lyme Cases", format=",")
            ]
        )
    )

intro_lyme_chart = style_chart(
    alt.layer(*intro_layers).add_params(intro_zoom).properties(
        title=f"Total Aggregated Reported Lyme Disease Cases in the U.S., 1992–2023: {intro_trend_type}"
    ),
    width=1080,
    height=430
)

st.altair_chart(intro_lyme_chart, width="stretch")

st.markdown(
    """
    <div class="note-card">
    <b>Reading this chart:</b> The raw trendline shows reported annual Lyme disease cases directly.
    The moving average and binomial filter smooth short-term fluctuations to make the broader
    multi-year increase easier to see.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# NATIONAL TREND CHARTS
# ============================================================

st.markdown("## National Trends")

# -----------------------------
# Lyme chart
# -----------------------------

lyme_base = alt.Chart(national_lyme_f).encode(
    x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d"))
)

lyme_layers = []

if show_raw:
    lyme_layers.append(
        lyme_base.mark_line(color=RAW_LINE, strokeWidth=2).encode(
            y=alt.Y("lyme_cases:Q", title="Reported Lyme Disease Cases"),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Raw Lyme Cases", format=",")
            ]
        )
    )
    lyme_layers.append(
        lyme_base.mark_circle(color=RAW_POINT, size=45, opacity=0.8).encode(
            y="lyme_cases:Q",
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Raw Lyme Cases", format=",")
            ]
        )
    )

if show_binomial:
    lyme_layers.append(
        lyme_base.mark_line(color=LYME_RED, strokeWidth=3.2).encode(
            y=alt.Y("lyme_cases_binomial:Q", title="Reported Lyme Disease Cases"),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases_binomial:Q", title="Smoothed Lyme Cases", format=",.0f")
            ]
        )
    )

if lyme_layers:
    lyme_chart = style_chart(
        alt.layer(*lyme_layers).add_params(zoom).properties(
            title="Lyme disease cases, 1992–2023"
        ),
        width=520,
        height=320
    )
else:
    lyme_chart = None

# -----------------------------
# Temperature chart
# -----------------------------

temp_base = alt.Chart(national_temp_f).encode(
    x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d"))
)

temp_layers = []

if show_raw:
    temp_layers.append(
        temp_base.mark_line(color=RAW_LINE, strokeWidth=2).encode(
            y=alt.Y(
                "avg_temp_F:Q",
                title="Average Temperature (°F)",
                scale=alt.Scale(zero=False)
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F:Q", title="Raw Avg Temp (°F)", format=".2f")
            ]
        )
    )
    temp_layers.append(
        temp_base.mark_circle(color=RAW_POINT, size=45, opacity=0.8).encode(
            y=alt.Y("avg_temp_F:Q", scale=alt.Scale(zero=False)),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F:Q", title="Raw Avg Temp (°F)", format=".2f")
            ]
        )
    )

if show_binomial:
    temp_layers.append(
        temp_base.mark_line(color=TEMP_RED, strokeWidth=3.2).encode(
            y=alt.Y(
                "avg_temp_F_binomial:Q",
                title="Average Temperature (°F)",
                scale=alt.Scale(zero=False)
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F_binomial:Q", title="Smoothed Avg Temp (°F)", format=".2f")
            ]
        )
    )

if temp_layers:
    temp_chart = style_chart(
        alt.layer(*temp_layers).add_params(zoom).properties(
            title="Average temperature, 1992–2023"
        ),
        width=520,
        height=320
    )
else:
    temp_chart = None

# -----------------------------
# Mouse chart
# -----------------------------

mouse_base = alt.Chart(national_mouse_f).encode(
    x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d"))
)

mouse_layers = []

if show_raw:
    mouse_layers.append(
        mouse_base.mark_line(color=RAW_LINE, strokeWidth=2).encode(
            y=alt.Y("white_footed_mouse_occurrence_records:Q", title="Total Occurrence Records"),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip(
                    "white_footed_mouse_occurrence_records:Q",
                    title="Raw Mouse Records",
                    format=","
                )
            ]
        )
    )
    mouse_layers.append(
        mouse_base.mark_circle(color=RAW_POINT, size=45, opacity=0.8).encode(
            y="white_footed_mouse_occurrence_records:Q",
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip(
                    "white_footed_mouse_occurrence_records:Q",
                    title="Raw Mouse Records",
                    format=","
                )
            ]
        )
    )

if show_binomial:
    mouse_layers.append(
        mouse_base.mark_line(color=MOUSE_RED, strokeWidth=3.2).encode(
            y=alt.Y("mouse_records_binomial:Q", title="Total Occurrence Records"),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip(
                    "mouse_records_binomial:Q",
                    title="Smoothed Mouse Records",
                    format=",.0f"
                )
            ]
        )
    )

if mouse_layers:
    mouse_chart = style_chart(
        alt.layer(*mouse_layers).add_params(zoom).properties(
            title="White-footed mouse occurrence records, 1992–2023"
        ),
        width=1080,
        height=340
    )
else:
    mouse_chart = None

# ============================================================
# DISPLAY CHARTS IN 2 + 1 LAYOUT
# ============================================================

col1, col2 = st.columns(2)

with col1:
    if lyme_chart is not None:
        st.altair_chart(lyme_chart, width="stretch")
    else:
        empty_chart_message("Lyme")

with col2:
    if temp_chart is not None:
        st.altair_chart(temp_chart, width="stretch")
    else:
        empty_chart_message("temperature")

if mouse_chart is not None:
    st.altair_chart(mouse_chart, width="stretch")
else:
    empty_chart_message("mouse occurrence")

st.markdown(
    """
    <div class="section-card">
    <b>How to interact:</b> Use the sidebar to filter the year range.
    You can also zoom and pan horizontally on the charts to inspect shorter time windows.
    The pale red line and points show raw annual values, while the darker red line shows the
    binomial-smoothed trend.
    </div>
    """,
    unsafe_allow_html=True
)