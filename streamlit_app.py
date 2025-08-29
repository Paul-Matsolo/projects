# streamlit_app.py - Streamlit version of the Maritime Dashboard
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Import data cleaning functions
from data_cleaner import clean_maritime_data
# Import chart functions from individual files
from map_charts import create_overview_map, create_maritime_map
from bar_charts import create_event_type_chart, create_country_chart
from line_charts import create_timeline_chart, create_monthly_trend_chart
from pie_charts import create_event_type_pie, create_country_pie, create_sub_event_pie
from heatmap_charts import create_heatmap_chart, create_temporal_heatmap
from scatter_charts import create_lat_lon_scatter, create_time_scatter

# Page configuration
st.set_page_config(
    page_title="Maritime Risk Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and cache the maritime data"""
    cleaned_data = clean_maritime_data()
    return cleaned_data

# Load data
with st.spinner("Loading maritime data..."):
    data = load_data()
    df = data['df_events']

# Header
st.markdown('<h1 class="main-header">🌊 Maritime Risk Dashboard</h1>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("📊 Filters")

# Date range filter
st.sidebar.subheader("Date Range")
min_date = df['Event_Date'].min().date()
max_date = df['Event_Date'].max().date()
date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Country filter
st.sidebar.subheader("Country")
all_countries = ["All Countries"] + sorted(df['Country'].unique().tolist())
selected_country = st.sidebar.selectbox("Select country", all_countries)

# Event type filter
st.sidebar.subheader("Event Type")
all_events = ["All Events"] + sorted(df['Event_Type'].unique().tolist())
selected_event = st.sidebar.selectbox("Select event type", all_events)

# Apply filters
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[
        (df['Event_Date'].dt.date >= start_date) &
        (df['Event_Date'].dt.date <= end_date)
    ]
else:
    filtered_df = df
    start_date = min_date
    end_date = max_date

if selected_country != "All Countries":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

if selected_event != "All Events":
    filtered_df = filtered_df[filtered_df['Event_Type'] == selected_event]

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Events", f"{len(filtered_df):,}")
    
with col2:
    st.metric("Countries", f"{filtered_df['Country'].nunique():,}")
    
with col3:
    st.metric("Event Types", f"{filtered_df['Event_Type'].nunique():,}")
    
with col4:
    st.metric("Date Range", f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🗺️ Maps", "📊 Charts", "🔍 Analysis"])

with tab1:
    st.header("📈 Overview")
    
    # Timeline chart
    st.subheader("Events Timeline")
    timeline_fig = create_timeline_chart(filtered_df, "Maritime Events Timeline")
    st.plotly_chart(timeline_fig, use_container_width=True)
    
    # Event type distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Event Types")
        pie_fig = create_event_type_pie(filtered_df, "Event Type Distribution")
        st.plotly_chart(pie_fig, use_container_width=True)
    
    with col2:
        st.subheader("Countries")
        country_pie_fig = create_country_pie(filtered_df, "Events by Country")
        st.plotly_chart(country_pie_fig, use_container_width=True)

with tab2:
    st.header("🗺️ Maps")
    
    # Maritime map
    st.subheader("Maritime Events Map")
    map_fig = create_maritime_map(filtered_df)
    st.plotly_chart(map_fig, use_container_width=True)
    
    # Scatter plot
    st.subheader("Geographic Scatter Plot")
    scatter_fig = create_lat_lon_scatter(filtered_df, "Maritime Events by Coordinates")
    st.plotly_chart(scatter_fig, use_container_width=True)

with tab3:
    st.header("📊 Charts")
    
    # Bar charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Event Types")
        bar_fig = create_event_type_chart(filtered_df, "Events by Type")
        st.plotly_chart(bar_fig, use_container_width=True)
    
    with col2:
        st.subheader("Countries")
        country_bar_fig = create_country_chart(filtered_df, "Events by Country")
        st.plotly_chart(country_bar_fig, use_container_width=True)
    
    # Heatmaps
    st.subheader("Heatmaps")
    col1, col2 = st.columns(2)
    
    with col1:
        heatmap_fig = create_heatmap_chart(filtered_df, "Event Type by Country Heatmap")
        st.plotly_chart(heatmap_fig, use_container_width=True)
    
    with col2:
        temporal_heatmap_fig = create_temporal_heatmap(filtered_df, "Events by Month and Type")
        st.plotly_chart(temporal_heatmap_fig, use_container_width=True)

with tab4:
    st.header("🔍 Analysis")
    
    # Monthly trends
    st.subheader("Monthly Trends")
    trend_fig = create_monthly_trend_chart(filtered_df, "Monthly Event Trends")
    st.plotly_chart(trend_fig, use_container_width=True)
    
    # Time scatter
    st.subheader("Time Analysis")
    time_scatter_fig = create_time_scatter(filtered_df, "Maritime Events Timeline by Type")
    st.plotly_chart(time_scatter_fig, use_container_width=True)
    
    # Data table
    st.subheader("Raw Data")
    st.dataframe(filtered_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🌊 **Maritime Risk Dashboard** - Powered by Streamlit")
