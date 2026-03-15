
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt
import vega_datasets
from great_tables import GT, html

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    # Title and icon for the browser's tab bar:
    page_title="Dashboard",
    #page_icon="🌦️",
    # Make the content take up the width of the page:
    layout="wide",

)

"""
## Products Subject to Section 232, where El Salvador exports to U.S.A > 0

"""


full_df = vega_datasets.data("seattle_weather")


""  # Add a little vertical space. Same as st.write("").
""



@st.cache_data
def get_slv_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/seccion_232.csv'
    df = pd.read_csv(DATA_FILENAME)


    NOMBRES_FILENAME = Path(__file__).parent/'data/nombres_hs8.csv'

    nombres = pd.read_csv(NOMBRES_FILENAME)

    df = df.merge(nombres, left_on = "hs8", right_on = "HS8")

    df["total_for_all_countries"] *=1_000_000
    df["el_salvador"] *=1_000_000

    return df


df_slv = get_slv_data()[["Description", "sector", "total_for_all_countries", "participation_in_us_imports_china", "participation_in_us_imports_mexico", "el_salvador"]]

table = (
    GT(df_slv)
    .data_color(
        columns="total_for_all_countries", 
        palette=["snow", "#EEC900", "#E8C32E", "#D69C4E"],
        #palette=["#00A600", "#E6E600", "#E8C32E", "#D69C4E", "#Dc863B", "sienna", "sienna4", "tomato4", "brown"],
        domain=[df_slv["total_for_all_countries"].min(), df_slv["total_for_all_countries"].max()]
    )
    .data_color(
        columns="el_salvador", 
        palette=["snow", "#EEC900", "#E8C32E", "#D69C4E"],
        #palette=["#00A600", "#E6E600", "#E8C32E", "#D69C4E", "#Dc863B", "sienna", "sienna4", "tomato4", "brown"],
        domain=[df_slv["el_salvador"].min(), df_slv["el_salvador"].max()]
    )
    .data_color(
        columns= ["participation_in_us_imports_china", "participation_in_us_imports_mexico"], 
        palette=["snow", "#EEC900", "#E8C32E", "#D69C4E"],
        #palette=["#00A600", "#E6E600", "#E8C32E", "#D69C4E", "#Dc863B", "sienna", "sienna4", "tomato4", "brown"],
        domain=[0, 1]
    )
    .tab_header(
        title="",
        subtitle=""
    )
    .cols_label(
        Description = html("Descripción"),
        sector = html("Sector"),
        total_for_all_countries= html("Market size in U.S (Total U.S Imports)"),
        participation_in_us_imports_china= html("China Share of U.S Imports (%)"),
        participation_in_us_imports_mexico= html("Mexico Share of U.S Imports (%)"),
        el_salvador= html("El Salvador exports to U.S"),
    ).fmt_percent(columns=["participation_in_us_imports_china", "participation_in_us_imports_mexico"], decimals=0)
    .fmt_number(
        columns=["total_for_all_countries", "el_salvador"],
        compact=True,
        pattern="${x}",
        n_sigfig=3,
    )
)

with st.container():
    st.html(table)
