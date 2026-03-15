import streamlit as st

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    # Title and icon for the browser's tab bar:
    page_title="Dashboard",
    #page_icon="🌦️",
    # Make the content take up the width of the page:
    layout="wide",

)

pages = {
    "Products Subject to Section 232": [
        st.Page("products.py", title="El Salvador exports to U.S.A > 0"),
    ],
    "Tabla" : [
        st.Page("table.py", title = "Table"),
    ]
}

pg = st.navigation(pages, position="top")
pg.run()


