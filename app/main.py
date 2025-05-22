import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Load data ---
@st.cache_data
def load_data(country):
    filename_map = {
        "Benin": "benin_clean.csv",
        "Sierra Leone": "sierraleone_clean.csv",
        "Togo": "togo_clean.csv"
    }
    return pd.read_csv(os.path.join("data", filename_map[country]))

# --- Sidebar widgets ---
countries = ['Benin', 'Sierra Leone', 'Togo']
selected_countries = st.sidebar.multiselect("Select Country", countries, default=countries)

metrics = ['GHI', 'DNI', 'DHI']

# --- Cached boxplot function ---
@st.cache_data
def create_boxplot(df, metric, country):
    fig = px.box(df, y=metric, title=f"{country} - {metric} Distribution")
    return fig

# --- Main content ---
for country in selected_countries:
    df = load_data(country)
    st.header(f"{country} Solar Data")

    # Boxplots for GHI, DNI, DHI
    for metric in metrics:
        #  Apply sampling to reduce lag
        sample_df = df.sample(n=1000) if len(df) > 1000 else df

        with st.expander(f"{metric} Distribution"):
            fig = create_boxplot(sample_df, metric, country)
            st.plotly_chart(fig, use_container_width=True)

        # Show raw data in a separate expander (not nested)
        with st.expander(f"{metric} - Show Raw Data"):
            st.dataframe(df.head())

    # Summary statistics
    st.subheader("Summary Statistics")
    summary = df[metrics].agg(['mean', 'median', 'std']).round(2)
    st.dataframe(summary)
