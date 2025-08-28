# pie_charts.py - Pie chart visualization functions
import plotly.express as px

def create_event_type_pie(df, title="Event Type Distribution"):
    """
    Create a pie chart showing event type distribution
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    # Only show event types that actually exist in the filtered data
    event_counts = df['Event_Type'].value_counts()
    # Remove any zero counts (shouldn't happen with unused categories removed, but safety check)
    event_counts = event_counts[event_counts > 0]
    
    fig = px.pie(
        values=event_counts.values,
        names=event_counts.index,
        title=title
    ).update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_country_pie(df, title="Top Countries Distribution", top_n=10):
    """
    Create a pie chart showing top countries distribution
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        top_n (int): Number of top countries to show
        
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    # Only show countries that actually exist in the filtered data
    country_counts = df['Country'].value_counts().head(top_n)
    # Remove any zero counts (shouldn't happen with unused categories removed, but safety check)
    country_counts = country_counts[country_counts > 0]
    
    fig = px.pie(
        values=country_counts.values,
        names=country_counts.index,
        title=title
    ).update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_sub_event_pie(df, title="Sub-Event Type Distribution"):
    """
    Create a pie chart showing sub-event type distribution
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    # Only show sub-event types that actually exist in the filtered data
    sub_event_counts = df['Sub_Event_Type'].value_counts()
    # Remove any zero counts (shouldn't happen with unused categories removed, but safety check)
    sub_event_counts = sub_event_counts[sub_event_counts > 0]
    
    fig = px.pie(
        values=sub_event_counts.values,
        names=sub_event_counts.index,
        title=title
    ).update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig
