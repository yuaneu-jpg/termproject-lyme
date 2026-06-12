import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="Lyme Disease Climate Dashboard",
    layout="wide"
)

alt.data_transformers.disable_max_rows()

#HTML stuff---------------------
st.markdown(
    """
    <style>
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
        padding: 1rem 1.25rem;
        background-color: rgba(255, 255, 255, 0.94);
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    p, li, label, div, span {
        font-family: Helvetica, Arial, sans-serif !important;
    }

    .custom-heading {
        font-family: Helvetica, Arial, sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.025em !important;
        color: #111111 !important;
        border: 1.5px solid #111111;
        padding: 1.35rem 1.6rem;
        background-color: rgba(255, 255, 255, 0.94);
        margin-top: 3rem;
        margin-bottom: 1.2rem;
        line-height: 1.25;
    }

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

    section[data-testid="stSidebar"] [data-testid="stSlider"] * {
        color: #111111 !important;
    }

    div[data-testid="stAltairChart"] {
        background-color: rgba(255, 255, 255, 0.96);
        border: 1.5px solid #111111;
        padding: 1rem;
        margin-bottom: 1.5rem;
    }

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

#color theme

LYME_RED = "#d9474b"
TEMP_RED = "#c85c5c"
MOUSE_RED = "#a94442"
RAW_LINE = "#d7b3b3"
RAW_POINT = "#caa4a4"
DARK = "#111111"
LIGHT_GRAY = "#e6e6e6"

REGION_COLORS = {
    "Midwest": "#9db7cf",
    "Northeast": "#f2a65a",
    "South": "#f28b82",
    "West": "#8ab7a1"
}

#load file path -------------

BASE = Path(__file__).parent / "Files"

LYME_XLSX = BASE / "lyme_1992_2023_state_year_cases_wide_clean.xlsx"
LYME_CSV = BASE / "lyme_1992_2023_state_year_cases_wide_FINAL.csv"
TEMP_CSV = BASE / "combined_state_average_temperature_1992_2023_all_states.csv"
MOUSE_CSV = BASE / "gbif_white_footed_mouse_state_year_1992_2023.csv"

#sort region

STATE_TO_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
}

ABBR_TO_STATE = {v: k for k, v in STATE_TO_ABBR.items()}

def normalize_state(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in STATE_TO_ABBR:
        return STATE_TO_ABBR[value]

    value_upper = value.upper()

    if value_upper in ABBR_TO_STATE:
        return value_upper

    return value


def assign_region(state):
    northeast = ["CT", "ME", "MA", "NH", "RI", "VT", "NJ", "NY", "PA"]
    midwest = ["IL", "IN", "MI", "OH", "WI", "IA", "KS", "MN", "MO", "NE", "ND", "SD"]
    south = ["DE", "FL", "GA", "MD", "NC", "SC", "VA", "WV", "AL", "KY", "MS", "TN", "AR", "LA", "OK", "TX"]
    west = ["AZ", "CO", "ID", "MT", "NV", "NM", "UT", "WY", "AK", "CA", "HI", "OR", "WA"]

    if state in northeast:
        return "Northeast"
    elif state in midwest:
        return "Midwest"
    elif state in south:
        return "South"
    elif state in west:
        return "West"
    else:
        return "Other"

# YEAR FOCUS CHANGE SIDEBAR------------------------------

st.sidebar.title("Change Year Focus")

year_range = st.sidebar.slider(
    "Year range",
    min_value=1992,
    max_value=2023,
    value=(1992, 2023)
)

#HEADLINE _---------------------------

st.title("Climate Change and Lyme Disease")

st.markdown(
    """
    <div class="intro-card">
        <div class="intro-title">Lyme has been on an increase in the last 3 decades.</div>
        <div class="intro-body">
            Climate change is a devastating anthropogenic phenomenon that strikes the natural world through a gamut of mechanisms. One aspect is the increase in zoonotic diseases through the creation of conditions that enable greater transmission from host to human. An example of a prominent zoonotic disease in North America is Lyme borreliosis (AKA Lyme disease), spread through the bites of infected blacklegged ticks that are carried through reservoir hosts such as white-tailed deer and white-footed mice (the principal reservoir host).
            This dashboard is an investigation into how climate change is one of the causes for the rise in Lyme disease cases in the US – focusing on increase in temperature across each state and unconventional migration behavior of reservoir hosts. 
            These relationships can be examined through foundational knowledge in that warmer conditions foster Lyme transmission and reservoir hosts carry Lyme across their usual containment area furthering host to human infections. 
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

#DEFINE FUNCTIONS HERE------------------------------------------

def read_csv_safe(path):
    for enc in ["utf-8", "utf-8-sig", "latin1", "cp1252"]:
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue

    return pd.read_csv(path, encoding="latin1", encoding_errors="replace")


@st.cache_data
def load_data():
    # Lyme
    if LYME_XLSX.exists():
        try:
            lyme_wide = pd.read_excel(LYME_XLSX)
        except ImportError:
            st.warning(
                "openpyxl is not installed, so the Excel file could not be read. "
                "Trying the Lyme CSV instead."
            )
            if not LYME_CSV.exists():
                st.error(f"Could not find Lyme CSV fallback at:\n{LYME_CSV}")
                st.stop()
            lyme_wide = read_csv_safe(LYME_CSV)
    elif LYME_CSV.exists():
        lyme_wide = read_csv_safe(LYME_CSV)
    else:
        st.error(f"Could not find Lyme file at:\n{LYME_XLSX}\nor\n{LYME_CSV}")
        st.stop()

    if "State" not in lyme_wide.columns:
        st.error("The Lyme file does not contain a 'State' column.")
        st.write("Columns found:", list(lyme_wide.columns))
        st.stop()

    lyme = lyme_wide.melt(
        id_vars="State",
        var_name="year",
        value_name="lyme_cases"
    )

    lyme = lyme.rename(columns={"State": "state"})
    lyme["state"] = lyme["state"].apply(normalize_state)
    lyme["year"] = pd.to_numeric(lyme["year"], errors="coerce")
    lyme = lyme.dropna(subset=["year", "state"])
    lyme["year"] = lyme["year"].astype(int)
    lyme["lyme_cases"] = pd.to_numeric(lyme["lyme_cases"], errors="coerce").fillna(0)

    # temp
    if not TEMP_CSV.exists():
        st.error(f"Could not find temperature file at:\n{TEMP_CSV}")
        st.stop()

    temp = read_csv_safe(TEMP_CSV)

    if "state" not in temp.columns or "year" not in temp.columns or "avg_temp_F" not in temp.columns:
        st.error("The temperature file must contain 'state', 'year', and 'avg_temp_F' columns.")
        st.write("Columns found:", list(temp.columns))
        st.stop()

    temp["state"] = temp["state"].apply(normalize_state)
    temp["year"] = pd.to_numeric(temp["year"], errors="coerce")
    temp = temp.dropna(subset=["year", "state"])
    temp["year"] = temp["year"].astype(int)
    temp["avg_temp_F"] = pd.to_numeric(temp["avg_temp_F"], errors="coerce")

    # Mouse
    if not MOUSE_CSV.exists():
        st.error(f"Could not find mouse file at:\n{MOUSE_CSV}")
        st.stop()

    mouse = read_csv_safe(MOUSE_CSV)

    if (
        "state" not in mouse.columns
        or "year" not in mouse.columns
        or "white_footed_mouse_occurrence_records" not in mouse.columns
    ):
        st.error(
            "The mouse file must contain 'state', 'year', and "
            "'white_footed_mouse_occurrence_records' columns."
        )
        st.write("Columns found:", list(mouse.columns))
        st.stop()

    mouse["state"] = mouse["state"].apply(normalize_state)
    mouse["year"] = pd.to_numeric(mouse["year"], errors="coerce")
    mouse = mouse.dropna(subset=["year", "state"])
    mouse["year"] = mouse["year"].astype(int)
    mouse["white_footed_mouse_occurrence_records"] = pd.to_numeric(
        mouse["white_footed_mouse_occurrence_records"],
        errors="coerce"
    ).fillna(0)

    return lyme, temp, mouse


def binomial_filter(series):
    weights = np.array([1, 4, 6, 4, 1]) / 16
    values = series.to_numpy()

    if len(values) < 5:
        return pd.Series([np.nan] * len(values), index=series.index)

    filtered = np.convolve(values, weights, mode="same")
    filtered[:2] = np.nan
    filtered[-2:] = np.nan

    return pd.Series(filtered, index=series.index)


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
    ).configure_legend(
        labelFont="Helvetica",
        titleFont="Helvetica",
        labelColor=DARK,
        titleColor=DARK
    ).configure_view(
        stroke=None
    )


def style_combined_chart(chart):
    return chart.properties(
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
    ).configure_legend(
        labelFont="Helvetica",
        titleFont="Helvetica",
        labelColor=DARK,
        titleColor=DARK
    ).configure_view(
        stroke=None
    )


def custom_heading(text):
    st.markdown(
        f"""
        <div class="custom-heading">{text}</div>
        """,
        unsafe_allow_html=True
    )

#ALL DATA PUT HERE--------------------------------------------------------

lyme, temp, mouse = load_data()

#national datasets----------------------------------------------------

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

national_lyme["lyme_cases_ma5"] = (
    national_lyme["lyme_cases"]
    .rolling(window=5, center=True)
    .mean()
)
national_temp["avg_temp_F_ma5"] = (
    national_temp["avg_temp_F"]
    .rolling(window=5, center=True)
    .mean()
)

national_mouse["mouse_records_ma5"] = (
    national_mouse["white_footed_mouse_occurrence_records"]
    .rolling(window=5, center=True)
    .mean()
)
national_lyme["lyme_cases_binomial"] = binomial_filter(national_lyme["lyme_cases"])
national_temp["avg_temp_F_binomial"] = binomial_filter(national_temp["avg_temp_F"])
national_mouse["mouse_records_binomial"] = binomial_filter(
    national_mouse["white_footed_mouse_occurrence_records"]
)

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

#intro after explanation---------------------------------------

custom_heading("Disease Trend Overview")

st.markdown(
    """
    <div class="section-card">
    Reported Lyme disease cases form the foundation of this dashboard. Before we continue into comparative analysis with aspects of climate change, let's see how Lyme has been trending across the US from 1992-2023, based on available data from the CDC.
    We observe that there is a rising increase in reported cases, why would that be? 
    </div>
    """,
    unsafe_allow_html=True
)

intro_chart_placeholder = st.empty()

intro_trend_type = "Raw trendline"
intro_zoom = alt.selection_interval(
    name="intro_zoom",
    bind="scales",
    encodings=["x"]
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
                title="Total Reported Lyme Disease Cases",
                scale=alt.Scale(domain=[0, 100000])
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
            y=alt.Y(
                "lyme_cases:Q",
                scale=alt.Scale(domain=[0, 100000])
            ),
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
                title="Total Reported Lyme Disease Cases",
                scale=alt.Scale(domain=[0, 100000])
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
            y=alt.Y(
                "lyme_cases:Q",
                scale=alt.Scale(domain=[0, 100000])
            ),
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
                title="Total Reported Lyme Disease Cases",
                scale=alt.Scale(domain=[0, 100000])
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
                title="Total Reported Lyme Disease Cases",
                scale=alt.Scale(domain=[0, 100000])
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

intro_chart_placeholder.altair_chart(intro_lyme_chart, use_container_width=True)

#national trends intro

custom_heading("National Trends")

st.markdown(
    """
    <div class="section-card">
    We utilized different trend filters, raw, binomial, and moving average to conclude that we are seeing an increase in all 3 major variables in this analysis. Without further analysis, this concludes that correlationally, there seems to be an existing pattern of positive growth in all three major categories of Lyme incidence, temperature, and principal host - human contact (given by occurence values, which indicate a meeting between humans and white-footed mouse). 
    </div>
    """,
    unsafe_allow_html=True
)

trend_col, blank_col = st.columns([1, 2.4])

with trend_col:
    national_trend_type = st.selectbox(
        "Choose Type of Filter for National Trend Graphs",
        [
            "Raw trendline",
            "Moving average",
            "Binomial filter"
        ],
        key="national_trend_type"
    )

#LYME CHART ---------------------------------------------

lyme_zoom = alt.selection_interval(
    name="lyme_zoom",
    bind="scales",
    encodings=["x"]
)

lyme_base = alt.Chart(national_lyme_f).encode(
    x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d"))
)

if national_trend_type == "Raw trendline":
    lyme_chart_body = alt.layer(
        lyme_base.mark_line(color=LYME_RED, strokeWidth=3).encode(
            y=alt.Y("lyme_cases:Q", title="Reported Lyme Disease Cases"),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Lyme Cases", format=",")
            ]
        ),
        lyme_base.mark_circle(color=LYME_RED, size=45, opacity=0.8).encode(
            y="lyme_cases:Q",
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Lyme Cases", format=",")
            ]
        )
    )

elif national_trend_type == "Moving average":
    lyme_chart_body = alt.layer(
        lyme_base.mark_line(color=RAW_LINE, strokeWidth=2, opacity=0.8).encode(
            y=alt.Y("lyme_cases:Q", title="Reported Lyme Disease Cases"),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Raw Lyme Cases", format=",")
            ]
        ),
        lyme_base.mark_line(color=LYME_RED, strokeWidth=3.2).encode(
            y=alt.Y("lyme_cases_ma5:Q", title="Reported Lyme Disease Cases"),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases_ma5:Q", title="5-Year Moving Average", format=",.0f")
            ]
        )
    )

else:
    lyme_chart_body = alt.layer(
        lyme_base.mark_line(color=RAW_LINE, strokeWidth=2, opacity=0.8).encode(
            y=alt.Y("lyme_cases:Q", title="Reported Lyme Disease Cases"),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases:Q", title="Raw Lyme Cases", format=",")
            ]
        ),
        lyme_base.mark_line(color=LYME_RED, strokeWidth=3.2).encode(
            y=alt.Y("lyme_cases_binomial:Q", title="Reported Lyme Disease Cases"),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("lyme_cases_binomial:Q", title="Binomial Filter", format=",.0f")
            ]
        )
    )

lyme_chart = style_chart(
    lyme_chart_body.add_params(lyme_zoom).properties(
        title=f"Lyme disease cases, 1992–2023: {national_trend_type}"
    ),
    width=520,
    height=320
)

#TEMP CHART ------------------------------------------------------

temp_zoom = alt.selection_interval(
    name="temp_zoom",
    bind="scales",
    encodings=["x"]
)

temp_base = alt.Chart(national_temp_f).encode(
    x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d"))
)

if national_trend_type == "Raw trendline":
    temp_chart_body = alt.layer(
        temp_base.mark_line(color=TEMP_RED, strokeWidth=3).encode(
            y=alt.Y(
                "avg_temp_F:Q",
                title="Average Temperature (°F)",
                scale=alt.Scale(zero=False)
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F:Q", title="Average Temperature (°F)", format=".2f")
            ]
        ),
        temp_base.mark_circle(color=TEMP_RED, size=45, opacity=0.8).encode(
            y=alt.Y("avg_temp_F:Q", scale=alt.Scale(zero=False)),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F:Q", title="Average Temperature (°F)", format=".2f")
            ]
        )
    )

elif national_trend_type == "Moving average":
    temp_chart_body = alt.layer(
        temp_base.mark_line(color=RAW_LINE, strokeWidth=2, opacity=0.8).encode(
            y=alt.Y(
                "avg_temp_F:Q",
                title="Average Temperature (°F)",
                scale=alt.Scale(zero=False)
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F:Q", title="Raw Avg Temp (°F)", format=".2f")
            ]
        ),
        temp_base.mark_line(color=TEMP_RED, strokeWidth=3.2).encode(
            y=alt.Y(
                "avg_temp_F_ma5:Q",
                title="Average Temperature (°F)",
                scale=alt.Scale(zero=False)
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F_ma5:Q", title="5-Year Moving Average", format=".2f")
            ]
        )
    )

else:
    temp_chart_body = alt.layer(
        temp_base.mark_line(color=RAW_LINE, strokeWidth=2, opacity=0.8).encode(
            y=alt.Y(
                "avg_temp_F:Q",
                title="Average Temperature (°F)",
                scale=alt.Scale(zero=False)
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F:Q", title="Raw Avg Temp (°F)", format=".2f")
            ]
        ),
        temp_base.mark_line(color=TEMP_RED, strokeWidth=3.2).encode(
            y=alt.Y(
                "avg_temp_F_binomial:Q",
                title="Average Temperature (°F)",
                scale=alt.Scale(zero=False)
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F_binomial:Q", title="Binomial Filter", format=".2f")
            ]
        )
    )

temp_chart = style_chart(
    temp_chart_body.add_params(temp_zoom).properties(
        title=f"Average temperature, 1992–2023: {national_trend_type}"
    ),
    width=520,
    height=320
)

# MOUSE CHART!------------------------------

mouse_zoom = alt.selection_interval(
    name="mouse_zoom",
    bind="scales",
    encodings=["x"]
)

mouse_base = alt.Chart(national_mouse_f).encode(
    x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d"))
)

if national_trend_type == "Raw trendline":
    mouse_chart_body = alt.layer(
        mouse_base.mark_line(color=MOUSE_RED, strokeWidth=3).encode(
            y=alt.Y(
                "white_footed_mouse_occurrence_records:Q",
                title="Total Occurrence Records"
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip(
                    "white_footed_mouse_occurrence_records:Q",
                    title="Mouse Occurrence Records",
                    format=","
                )
            ]
        ),
        mouse_base.mark_circle(color=MOUSE_RED, size=45, opacity=0.8).encode(
            y="white_footed_mouse_occurrence_records:Q",
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip(
                    "white_footed_mouse_occurrence_records:Q",
                    title="Mouse Occurrence Records",
                    format=","
                )
            ]
        )
    )

elif national_trend_type == "Moving average":
    mouse_chart_body = alt.layer(
        mouse_base.mark_line(color=RAW_LINE, strokeWidth=2, opacity=0.8).encode(
            y=alt.Y(
                "white_footed_mouse_occurrence_records:Q",
                title="Total Occurrence Records"
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip(
                    "white_footed_mouse_occurrence_records:Q",
                    title="Raw Mouse Records",
                    format=","
                )
            ]
        ),
        mouse_base.mark_line(color=MOUSE_RED, strokeWidth=3.2).encode(
            y=alt.Y(
                "mouse_records_ma5:Q",
                title="Total Occurrence Records"
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("mouse_records_ma5:Q", title="5-Year Moving Average", format=",.0f")
            ]
        )
    )

else:
    mouse_chart_body = alt.layer(
        mouse_base.mark_line(color=RAW_LINE, strokeWidth=2, opacity=0.8).encode(
            y=alt.Y(
                "white_footed_mouse_occurrence_records:Q",
                title="Total Occurrence Records"
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip(
                    "white_footed_mouse_occurrence_records:Q",
                    title="Raw Mouse Records",
                    format=","
                )
            ]
        ),
        mouse_base.mark_line(color=MOUSE_RED, strokeWidth=3.2).encode(
            y=alt.Y(
                "mouse_records_binomial:Q",
                title="Total Occurrence Records"
            ),
            tooltip=[
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("mouse_records_binomial:Q", title="Binomial Filter", format=",.0f")
            ]
        )
    )

mouse_chart = style_chart(
    mouse_chart_body.add_params(mouse_zoom).properties(
        title=f"White-footed mouse occurrence records, 1992–2023: {national_trend_type}"
    ),
    width=1080,
    height=340
)

col1, col2 = st.columns(2)

with col1:
    st.altair_chart(lyme_chart, use_container_width=True)

with col2:
    st.altair_chart(temp_chart, use_container_width=True)

st.altair_chart(mouse_chart, use_container_width=True)

#-----------------comparatiev graphs 

custom_heading("Relationship Between Lyme Disease, Temperature, and White-Footed Mouse Occurrence")

st.markdown(
    """
    <div class="section-card">
    This section compares Lyme disease with temperature and reservoir-host variables. The first
    scatterplot uses a one-year lag, comparing the previous year's average temperature with
    the current year's Lyme disease cases. This lag is important to keep in mind that temperature does not have immediate effects in nature and changes can realize after time passes and the envrionment adapts.
    The second scatterplot compares temperature,
    Lyme disease cases, and white-footed mouse occurrence records together in a triple-variable scatter.
    We observe that, nationally, there exists a normal distribution across both graphs, where Lyme incidence explodes at a certain temperature threshold. Users can additionally observe regional trends and patterns.
    Click any point
    in either graph to isolate that point's region across both graphs. Click empty space to reset.
    </div>
    """,
    unsafe_allow_html=True
)

#  1 year lagg
temp_lag = temp[["state", "year", "avg_temp_F"]].copy()
temp_lag["year"] = temp_lag["year"] + 1
temp_lag = temp_lag.rename(columns={"avg_temp_F": "previous_year_avg_temp_F"})

lag_df = lyme.merge(
    temp_lag,
    on=["state", "year"],
    how="inner"
)

lag_df["region"] = lag_df["state"].apply(assign_region)
lag_df["state_name"] = lag_df["state"].map(ABBR_TO_STATE).fillna(lag_df["state"])

lag_df = lag_df[
    (lag_df["year"] >= start_year) &
    (lag_df["year"] <= end_year) &
    (lag_df["region"] != "Other")
].copy()

# triple variable dataframe
scatter_df = (
    lyme.merge(
        temp[["state", "year", "avg_temp_F"]],
        on=["state", "year"],
        how="inner"
    )
    .merge(
        mouse[["state", "year", "white_footed_mouse_occurrence_records"]],
        on=["state", "year"],
        how="left"
    )
)

scatter_df["white_footed_mouse_occurrence_records"] = (
    scatter_df["white_footed_mouse_occurrence_records"].fillna(0)
)

scatter_df["region"] = scatter_df["state"].apply(assign_region)
scatter_df["state_name"] = scatter_df["state"].map(ABBR_TO_STATE).fillna(scatter_df["state"])

scatter_df = scatter_df[
    (scatter_df["year"] >= start_year) &
    (scatter_df["year"] <= end_year) &
    (scatter_df["region"] != "Other")
].copy()

if lag_df.empty or scatter_df.empty:
    st.warning(
        "One or both relationship graphs have no merged rows. Check whether state names and years "
        "match across the Lyme, temperature, and mouse files."
    )
    st.write("Lag rows:", len(lag_df))
    st.write("Triple-variable rows:", len(scatter_df))

else:
    region_click = alt.selection_point(
        name="region_click",
        fields=["region"],
        empty=True
    )

    region_color = alt.Color(
        "region:N",
        title="Region",
        scale=alt.Scale(
            domain=["Midwest", "Northeast", "South", "West"],
            range=[
                REGION_COLORS["Midwest"],
                REGION_COLORS["Northeast"],
                REGION_COLORS["South"],
                REGION_COLORS["West"]
            ]
        ),
        legend=alt.Legend(
            titleColor=DARK,
            labelColor=DARK,
            titleFont="Helvetica",
            labelFont="Helvetica"
        )
    )

    lag_chart = (
        alt.Chart(lag_df)
        .mark_circle(opacity=0.68, stroke=DARK, strokeWidth=0.25)
        .encode(
            x=alt.X(
                "previous_year_avg_temp_F:Q",
                title="Previous Year Average Temperature (°F)",
                scale=alt.Scale(zero=False)
            ),
            y=alt.Y(
                "lyme_cases:Q",
                title="Reported Lyme Disease Cases"
            ),
            color=region_color,
            size=alt.value(70),
            tooltip=[
                alt.Tooltip("state_name:N", title="State"),
                alt.Tooltip("region:N", title="Region"),
                alt.Tooltip("year:Q", title="Lyme Case Year", format="d"),
                alt.Tooltip(
                    "previous_year_avg_temp_F:Q",
                    title="Previous Year Avg Temp (°F)",
                    format=".2f"
                ),
                alt.Tooltip("lyme_cases:Q", title="Lyme Cases", format=",")
            ]
        )
        .transform_filter(region_click)
        .properties(
            width=1080,
            height=430,
            title="One-Year Lag: Previous Year Temperature vs. Current Year Lyme Disease Cases"
        )
    )

    triple_chart = (
        alt.Chart(scatter_df)
        .mark_circle(opacity=0.62, stroke=DARK, strokeWidth=0.25)
        .encode(
            x=alt.X(
                "avg_temp_F:Q",
                title="Average Temperature (°F)",
                scale=alt.Scale(zero=False)
            ),
            y=alt.Y(
                "lyme_cases:Q",
                title="Reported Lyme Disease Cases"
            ),
            size=alt.Size(
                "white_footed_mouse_occurrence_records:Q",
                title="Mouse Occurrence Records",
                scale=alt.Scale(range=[15, 900]),
                legend=alt.Legend(
                    titleColor=DARK,
                    labelColor=DARK,
                    titleFont="Helvetica",
                    labelFont="Helvetica"
                )
            ),
            color=region_color,
            tooltip=[
                alt.Tooltip("state_name:N", title="State"),
                alt.Tooltip("region:N", title="Region"),
                alt.Tooltip("year:Q", title="Year", format="d"),
                alt.Tooltip("avg_temp_F:Q", title="Average Temperature (°F)", format=".2f"),
                alt.Tooltip("lyme_cases:Q", title="Lyme Cases", format=","),
                alt.Tooltip(
                    "white_footed_mouse_occurrence_records:Q",
                    title="Mouse Occurrence Records",
                    format=","
                )
            ]
        )
        .transform_filter(region_click)
        .properties(
            width=1080,
            height=520,
            title="Temperature, Lyme Cases, and White-Footed Mouse Occurrence Records by Region"
        )
    )

    relationship_charts = alt.vconcat(
        lag_chart,
        triple_chart,
        spacing=40
    ).add_params(
        region_click
    ).resolve_scale(
        size="independent"
    )

    relationship_charts = style_combined_chart(relationship_charts)

    st.altair_chart(relationship_charts, use_container_width=True)

#--------custom stuff

custom_heading("Custom Scatterplot Builder")

st.markdown(
    """
    <div class="section-card">
    Many relationships between the three focus areas in this dashboard are left out, however, users can generate their own scatter plots to view these relationships at hand.
    A limitation of this study is that records of Lyme incidence spans only 3 decades, and earlier data sets are not available. Thus, many relationships cannot be substatiated due to fluctuations in all three variables.
    All in all, users can preem and discover relationships of their own, noting that relationships can be sparsely correlated due to aforementioned limitations. Please kindly keep this in mind while forming extrapolations.
    </div>
    """,
    unsafe_allow_html=True
)

custom_scatter_df = scatter_df.copy()

variable_map = {
    "Lyme cases": "lyme_cases",
    "Average temperature": "avg_temp_F",
    "Mouse occurrence records": "white_footed_mouse_occurrence_records"
}

axis_title_map = {
    "lyme_cases": "Reported Lyme Disease Cases",
    "avg_temp_F": "Average Temperature (°F)",
    "white_footed_mouse_occurrence_records": "White-Footed Mouse Occurrence Records"
}

col_x, col_y, col_size = st.columns(3)

with col_x:
    x_variable_label = st.selectbox(
        "Choose x-axis variable",
        [
            "Average temperature",
            "Mouse occurrence records",
            "Lyme cases"
        ],
        index=0,
        key="custom_x_variable"
    )

with col_y:
    y_variable_label = st.selectbox(
        "Choose y-axis variable",
        [
            "Lyme cases",
            "Average temperature",
            "Mouse occurrence records"
        ],
        index=0,
        key="custom_y_variable"
    )

with col_size:
    size_variable_label = st.selectbox(
        "Choose point size",
        [
            "None",
            "Mouse occurrence records",
            "Lyme cases"
        ],
        index=0,
        key="custom_size_variable"
    )

custom_regions = st.multiselect(
    "Filter regions for custom scatterplot",
    options=["Midwest", "Northeast", "South", "West"],
    default=["Midwest", "Northeast", "South", "West"],
    key="custom_scatter_region_filter"
)

custom_scatter_df = custom_scatter_df[
    custom_scatter_df["region"].isin(custom_regions)
].copy()

x_field = variable_map[x_variable_label]
y_field = variable_map[y_variable_label]

if x_field == y_field:
    st.warning("Choose two different variables for the x-axis and y-axis.")

elif custom_scatter_df.empty:
    st.warning("Select at least one region to display the custom scatterplot.")

else:
    custom_scatter_zoom = alt.selection_interval(
        name="custom_scatter_zoom",
        bind="scales"
    )

    custom_region_click = alt.selection_point(
        name="custom_region_click",
        fields=["region"],
        empty=True
    )

    custom_region_color = alt.Color(
        "region:N",
        title="Region",
        scale=alt.Scale(
            domain=["Midwest", "Northeast", "South", "West"],
            range=[
                REGION_COLORS["Midwest"],
                REGION_COLORS["Northeast"],
                REGION_COLORS["South"],
                REGION_COLORS["West"]
            ]
        ),
        legend=alt.Legend(
            titleColor=DARK,
            labelColor=DARK,
            titleFont="Helvetica",
            labelFont="Helvetica"
        )
    )

    scatter_encoding = {
        "x": alt.X(
            f"{x_field}:Q",
            title=axis_title_map[x_field],
            scale=alt.Scale(zero=False)
        ),
        "y": alt.Y(
            f"{y_field}:Q",
            title=axis_title_map[y_field],
            scale=alt.Scale(zero=False)
        ),
        "color": custom_region_color,
        "opacity": alt.condition(
            custom_region_click,
            alt.value(0.72),
            alt.value(0.15)
        ),
        "tooltip": [
            alt.Tooltip("state_name:N", title="State"),
            alt.Tooltip("region:N", title="Region"),
            alt.Tooltip("year:Q", title="Year", format="d"),
            alt.Tooltip("lyme_cases:Q", title="Lyme Cases", format=","),
            alt.Tooltip("avg_temp_F:Q", title="Average Temperature (°F)", format=".2f"),
            alt.Tooltip(
                "white_footed_mouse_occurrence_records:Q",
                title="Mouse Occurrence Records",
                format=","
            )
        ]
    }

    if size_variable_label == "Mouse occurrence records":
        scatter_encoding["size"] = alt.Size(
            "white_footed_mouse_occurrence_records:Q",
            title="Mouse Occurrence Records",
            scale=alt.Scale(range=[20, 800]),
            legend=alt.Legend(
                titleColor=DARK,
                labelColor=DARK,
                titleFont="Helvetica",
                labelFont="Helvetica"
            )
        )

    elif size_variable_label == "Lyme cases":
        scatter_encoding["size"] = alt.Size(
            "lyme_cases:Q",
            title="Lyme Cases",
            scale=alt.Scale(range=[20, 800]),
            legend=alt.Legend(
                titleColor=DARK,
                labelColor=DARK,
                titleFont="Helvetica",
                labelFont="Helvetica"
            )
        )

    else:
        scatter_encoding["size"] = alt.value(70)

    custom_scatter_chart = (
        alt.Chart(custom_scatter_df)
        .mark_circle(stroke=DARK, strokeWidth=0.25)
        .encode(**scatter_encoding)
        .add_params(custom_scatter_zoom, custom_region_click)
        .properties(
            width=1080,
            height=520,
            title=f"{y_variable_label} vs. {x_variable_label}"
        )
    )

    custom_scatter_chart = style_chart(
        custom_scatter_chart,
        width=1080,
        height=520
    )

    st.altair_chart(custom_scatter_chart, use_container_width=True)
    st.caption("Note: Climate change in this project is defined as the recent long-term shifts in climate systems caused by anthropogenic burning of fossil fuels and destruction of habitats, resulting in global warming and other disastrous effects to ecosystems.")