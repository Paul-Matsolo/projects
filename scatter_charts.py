# scatter_charts.py - Scatter plot visualization functions
import plotly.express as px
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
    fig = px.scatter(
        df,
        x='Longitude',
        y='Latitude',
        color='Event_Type',
        hover_data=['Country', 'Location'],
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
    
    fig = px.scatter(
        df_copy,
        x='Date',
        y='Event_Type',
        color='Event_Type',
        hover_data=['Country', 'Location'],
        title=title
    ).update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

