# scatter_charts.py - Scatter plot visualization functions
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_lat_lon_scatter(df, title="Events by Latitude and Longitude"):
    """
    Create a scatter plot showing events by latitude and longitude
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Scatter plot figure
    """
    # Filter out rows with missing coordinates
    df_clean = df.dropna(subset=['Latitude', 'Longitude'])
    
    if len(df_clean) == 0:
        # Return empty figure if no data
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        fig.update_layout(title=title, height=500)
        return fig
    
    # Avoid color grouping issues by not using color parameter
    fig = px.scatter(
        df_clean,
        x='Longitude',
        y='Latitude',
        hover_data=['Country', 'Location', 'Event_Type'],
        title=title
    ).update_layout(
        height=500,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_time_scatter(df, title="Events Over Time by Type"):
    """
    Create a scatter plot showing events over time colored by type
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Scatter plot figure
    """
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Event_Date'])
    
    # Filter out rows with missing dates
    df_clean = df_copy.dropna(subset=['Date', 'Event_Type'])
    
    if len(df_clean) == 0:
        # Return empty figure if no data
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        fig.update_layout(title=title, height=400)
        return fig
    
    # Avoid color grouping issues by not using color parameter
    fig = px.scatter(
        df_clean,
        x='Date',
        y='Event_Type',
        hover_data=['Country', 'Location'],
        title=title
    ).update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

