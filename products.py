
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



# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
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


    df["participation_in_us_imports_mexico"]*=100
    df["participation_in_us_imports_china"]*=100
    df["participation_in_us_imports_el_salvador"]*=100

    return df



df = get_gdp_data()

img_03 = alt.Chart(df, title="").mark_circle(
        opacity=0.7,
        stroke='black',
        strokeWidth=1.2,
        strokeOpacity=0.9,
        size = 300,
).encode(
    alt.X('el_salvador:Q').scale(type="log").title("El Salvador exports to U.S.A (million USD)"),
    alt.Y('participation_in_us_imports_china:Q').title("China Share of U.S. Imports (%)"),
    alt.Size("log_total_for_all_countries").title(["Market size", "(Log USD imports)"]), 
    alt.Color("participation_in_us_imports_mexico", 
                    scale=alt.Scale(scheme='cividis')).title(["Mexico Share of U.S.", "Imports (%)"]), 
    alt.Text("Description"), 
    tooltip=["Description"]
).properties(
    width=1200,  # Set a fixed width in pixels
    height=400  # Set a fixed height in pixels
)


st.altair_chart(img_03, use_container_width=False)
