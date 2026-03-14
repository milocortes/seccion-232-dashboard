import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Dashboard'
)

st.title("Average Participation in US Imports 2023-2025")

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

    df["participation_in_us_imports_mexico"]*=100
    df["participation_in_us_imports_china"]*=100
    df["participation_in_us_imports_el_salvador"]*=100

    return df

df = get_gdp_data()

img_03 = alt.Chart(df, title="").mark_circle().encode(
    alt.X('el_salvador:Q').title("El Salvador"),
    alt.Y('participation_in_us_imports_china:Q').title("China"),
    alt.Size("total_for_all_countries").title("Total for All Countries(Millions-USD)"), 
    alt.Color("participation_in_us_imports_mexico").title("Mexico"), 
    alt.Text("description"), 
    tooltip=["description"]
)

# Text layer with specific formatting
text_03 = alt.Chart(df).mark_text(
    align='left',
    baseline='middle',
    dx=3 # Offset the text slightly to the right of the bar
).encode(
    alt.X('el_salvador:Q').scale(type="log"),
    alt.Y('participation_in_us_imports_china:Q'),
    alt.Text("hs8")
)

st.altair_chart(img_03 + text_03)

