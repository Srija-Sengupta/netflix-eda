import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Netflix EDA Dashboard",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    df['country'] = df['country'].fillna('Unknown')
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🎛️ Filter Options")

type_list = df['type'].dropna().unique().tolist()
country_list = sorted(set(
    sum([str(c).split(',') for c in df['country'].dropna()], [])
))
country_list = [c.strip() for c in country_list if c.strip() != ""]

selected_type = st.sidebar.radio("Select Type", options=type_list, index=0)
selected_country = st.sidebar.selectbox("Select Country", country_list, index=0)
year_range = st.sidebar.slider("Select Release Year Range",
                               int(df['release_year'].min()),
                               int(df['release_year'].max()),
                               (2000, 2020))

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df[
    (df['type'] == selected_type) &
    (df['country'].str.contains(selected_country, na=False)) &
    (df['release_year'] >= year_range[0]) &
    (df['release_year'] <= year_range[1])
]

# -----------------------------
# Dashboard Header
# -----------------------------
st.title("🍿 Netflix Titles - Exploratory Data Analysis Dashboard")
st.markdown("Analyze Netflix data interactively using filters on the left.")

# -----------------------------
# Dataset Overview
# -----------------------------
st.subheader("🎯 Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df['type'] == "Movie"]))
col3.metric("TV Shows", len(filtered_df[filtered_df['type'] == "TV Show"]))

st.dataframe(filtered_df.head(10), use_container_width=True)

# -----------------------------
# Visuals Section
# -----------------------------
st.markdown("---")
st.subheader("📊 Visual Insights")

tab1, tab2, tab3 = st.tabs(["By Year", "By Rating", "Top Countries"])

# --- Plot 1: Release Year ---
with tab1:
    year_count = filtered_df['release_year'].value_counts().sort_index()
    fig1 = px.bar(
        x=year_count.index, y=year_count.values,
        labels={'x': 'Release Year', 'y': 'Count'},
        title='Titles Released Over the Years'
    )
    st.plotly_chart(fig1, use_container_width=True)

# --- Plot 2: Rating Distribution ---
with tab2:
    rating_count = filtered_df['rating'].value_counts()
    fig2 = px.pie(
        names=rating_count.index,
        values=rating_count.values,
        title='Distribution of Ratings'
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Plot 3: Top Countries ---
with tab3:
    top_countries = (
        df['country']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
    )
    fig3 = px.bar(
        x=top_countries.index, y=top_countries.values,
        labels={'x': 'Country', 'y': 'Number of Titles'},
        title='Top 10 Countries with Most Titles'
    )
    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("© 2025 Netflix EDA Dashboard | Built with Streamlit")

