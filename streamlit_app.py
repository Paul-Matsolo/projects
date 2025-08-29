# streamlit_app.py - Modern Streamlit version of the Maritime Dashboard
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

# Modern CSS with gradients, shadows, and better styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="waves" x="0" y="0" width="100" height="20" patternUnits="userSpaceOnUse"><path d="M0 10 Q25 5, 50 10 T100 10" stroke="rgba(255,255,255,0.1)" fill="none" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23waves)"/></svg>');
        opacity: 0.3;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header .subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Metric Cards */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }
    
    .metric-card:hover::before {
        transform: translateX(100%);
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(90deg, #f1f5f9 0%, #e2e8f0 100%);
        padding: 0.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #64748b;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .section-header h2 {
        margin: 0;
        color: #1e293b;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
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
with st.spinner("🌊 Loading maritime data..."):
    data = load_data()
    df = data['df_events']

# Modern Header
st.markdown("""
<div class="main-header">
    <h1>🌊 Maritime Risk Dashboard</h1>
    <div class="subtitle">Advanced Analytics for Maritime Security & Risk Assessment</div>
</div>
""", unsafe_allow_html=True)

# Sidebar with modern styling
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h3>🎯 Filters & Controls</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Date range filter
    st.markdown("**📅 Date Range**")
    min_date = df['Event_Date'].min().date()
    max_date = df['Event_Date'].max().date()
    date_range = st.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Country filter
    st.markdown("**🌍 Country**")
    all_countries = ["All Countries"] + sorted(df['Country'].unique().tolist())
    selected_country = st.selectbox(
        "Select country",
        all_countries,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Event type filter
    st.markdown("**⚡ Event Type**")
    all_events = ["All Events"] + sorted(df['Event_Type'].unique().tolist())
    selected_event = st.selectbox(
        "Select event type",
        all_events,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("**📊 Quick Stats**")
    st.markdown(f"**Total Records:** {len(df):,}")
    st.markdown(f"**Date Range:** {min_date.strftime('%b %d, %Y')} - {max_date.strftime('%b %d, %Y')}")
    st.markdown(f"**Countries:** {df['Country'].nunique()}")
    st.markdown(f"**Event Types:** {df['Event_Type'].nunique()}")

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

# Modern Metrics Display
st.markdown("""
<div class="metric-container">
    <div class="metric-card">
        <span class="metric-icon">📊</span>
        <div class="metric-value">{}</div>
        <div class="metric-label">Total Events</div>
    </div>
    <div class="metric-card">
        <span class="metric-icon">🌍</span>
        <div class="metric-value">{}</div>
        <div class="metric-label">Countries</div>
    </div>
    <div class="metric-card">
        <span class="metric-icon">⚡</span>
        <div class="metric-value">{}</div>
        <div class="metric-label">Event Types</div>
    </div>
    <div class="metric-card">
        <span class="metric-icon">📅</span>
        <div class="metric-value">{}</div>
        <div class="metric-label">Date Range</div>
    </div>
</div>
""".format(
    f"{len(filtered_df):,}",
    f"{filtered_df['Country'].nunique():,}",
    f"{filtered_df['Event_Type'].nunique():,}",
    f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}"
), unsafe_allow_html=True)

# Main content with modern tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🗺️ Maps", "📊 Charts", "🔍 Analysis"])

with tab1:
    st.markdown('<div class="section-header"><h2>📈 Dashboard Overview</h2></div>', unsafe_allow_html=True)
    
    # Timeline chart
    st.markdown('<div class="chart-container"><div class="chart-title">📈 Events Timeline</div>', unsafe_allow_html=True)
    timeline_fig = create_timeline_chart(filtered_df, "Maritime Events Timeline")
    st.plotly_chart(timeline_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Event type distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container"><div class="chart-title">🥧 Event Types Distribution</div>', unsafe_allow_html=True)
        pie_fig = create_event_type_pie(filtered_df, "Event Type Distribution")
        st.plotly_chart(pie_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container"><div class="chart-title">🌍 Events by Country</div>', unsafe_allow_html=True)
        country_pie_fig = create_country_pie(filtered_df, "Events by Country")
        st.plotly_chart(country_pie_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header"><h2>🗺️ Geographic Analysis</h2></div>', unsafe_allow_html=True)
    
    # Maritime map
    st.markdown('<div class="chart-container"><div class="chart-title">🗺️ Maritime Events Map</div>', unsafe_allow_html=True)
    map_fig = create_maritime_map(filtered_df)
    st.plotly_chart(map_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Scatter plot
    st.markdown('<div class="chart-container"><div class="chart-title">📍 Geographic Scatter Plot</div>', unsafe_allow_html=True)
    scatter_fig = create_lat_lon_scatter(filtered_df, "Maritime Events by Coordinates")
    st.plotly_chart(scatter_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header"><h2>📊 Detailed Analytics</h2></div>', unsafe_allow_html=True)
    
    # Bar charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container"><div class="chart-title">📊 Events by Type</div>', unsafe_allow_html=True)
        bar_fig = create_event_type_chart(filtered_df, "Events by Type")
        st.plotly_chart(bar_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container"><div class="chart-title">🏆 Top Countries</div>', unsafe_allow_html=True)
        country_bar_fig = create_country_chart(filtered_df, "Events by Country")
        st.plotly_chart(country_bar_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Heatmaps
    st.markdown('<div class="section-header"><h2>🔥 Heatmap Analysis</h2></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container"><div class="chart-title">🔥 Event Type by Country</div>', unsafe_allow_html=True)
        heatmap_fig = create_heatmap_chart(filtered_df, "Event Type by Country Heatmap")
        st.plotly_chart(heatmap_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container"><div class="chart-title">📅 Temporal Heatmap</div>', unsafe_allow_html=True)
        temporal_heatmap_fig = create_temporal_heatmap(filtered_df, "Events by Month and Type")
        st.plotly_chart(temporal_heatmap_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-header"><h2>🔍 Deep Analysis</h2></div>', unsafe_allow_html=True)
    
    # Monthly trends
    st.markdown('<div class="chart-container"><div class="chart-title">📈 Monthly Trends Analysis</div>', unsafe_allow_html=True)
    trend_fig = create_monthly_trend_chart(filtered_df, "Monthly Event Trends")
    st.plotly_chart(trend_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Time scatter
    st.markdown('<div class="chart-container"><div class="chart-title">⏰ Time-based Analysis</div>', unsafe_allow_html=True)
    time_scatter_fig = create_time_scatter(filtered_df, "Maritime Events Timeline by Type")
    st.plotly_chart(time_scatter_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data table with modern styling
    st.markdown('<div class="chart-container"><div class="chart-title">📋 Raw Data Explorer</div>', unsafe_allow_html=True)
    st.dataframe(
        filtered_df,
        use_container_width=True,
        column_config={
            "Event_Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
            "Country": st.column_config.TextColumn("Country", width="medium"),
            "Event_Type": st.column_config.TextColumn("Event Type", width="medium"),
            "Location": st.column_config.TextColumn("Location", width="large"),
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Modern Footer
st.markdown("""
<div class="footer">
    <h3>🌊 Maritime Risk Dashboard</h3>
    <p>Advanced Analytics Platform for Maritime Security & Risk Assessment</p>
    <p>Powered by Streamlit • Built with ❤️ for Maritime Safety</p>
</div>
""", unsafe_allow_html=True)
