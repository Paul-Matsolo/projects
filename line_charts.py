# line_charts.py - Line chart visualization functions
import plotly.express as px
import pandas as pd

def create_timeline_chart(df, title="Events Over Time"):
    """
    Create a line chart showing events over time
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Line chart figure
    """
    # Group by date and count events
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Event_Date']).dt.date
    daily_counts = df_copy.groupby('Date').size().reset_index(name='count')
    
    fig = px.line(
        daily_counts,
        x='Date',
        y='count',
        title=title,
        labels={'Date': 'Date', 'count': 'Number of Events'}
    ).update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_monthly_trend_chart(df, title="Monthly Event Trends"):
    """
    Create a line chart showing monthly event trends
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Line chart figure
    """
    # Group by month and count events
    df_copy = df.copy()
    df_copy['Month'] = pd.to_datetime(df_copy['Event_Date']).dt.to_period('M')
    monthly_counts = df_copy.groupby('Month').size().reset_index(name='count')
    monthly_counts['Month'] = monthly_counts['Month'].astype(str)
    
    fig = px.line(
        monthly_counts,
        x='Month',
        y='count',
        title=title,
        labels={'Month': 'Month', 'count': 'Number of Events'}
    ).update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis_tickangle=-45
    )
    
    return fig

