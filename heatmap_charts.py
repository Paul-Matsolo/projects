# heatmap_charts.py - Heatmap visualization functions
import plotly.express as px
import pandas as pd

def create_heatmap_chart(df, title="Event Type by Country Heatmap"):
    """
    Create a heatmap showing event types by country
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Heatmap figure
    """
    # Create pivot table
    pivot_data = df.groupby(['Country', 'Event_Type'], observed=False).size().unstack(fill_value=0)
    
    # Take top 20 countries for readability
    top_countries = df['Country'].value_counts().head(20).index
    pivot_data = pivot_data.loc[pivot_data.index.isin(top_countries)]
    
    fig = px.imshow(
        pivot_data,
        title=title,
        labels=dict(x="Event Type", y="Country", color="Count"),
        aspect="auto"
    ).update_layout(
        height=600,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_temporal_heatmap(df, title="Events by Month and Event Type"):
    """
    Create a heatmap showing events by month and event type
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Heatmap figure
    """
    # Create month column
    df_copy = df.copy()
    df_copy['Month'] = pd.to_datetime(df_copy['Event_Date']).dt.month_name()
    
    # Create pivot table
    pivot_data = df_copy.groupby(['Month', 'Event_Type'], observed=False).size().unstack(fill_value=0)
    
    # Reorder months
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    pivot_data = pivot_data.reindex(month_order)
    
    fig = px.imshow(
        pivot_data,
        title=title,
        labels=dict(x="Event Type", y="Month", color="Count"),
        aspect="auto"
    ).update_layout(
        height=500,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig
