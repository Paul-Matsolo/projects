# map_charts.py - Map visualization functions
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_overview_map(df_original):
    """
    Create a map showing all events from the original dataset (optimized for performance)
    
    Args:
        df_original (pd.DataFrame): Original unfiltered dataset
        
    Returns:
        plotly.graph_objects.Figure: Map figure
    """
    # Sample data if too many points for performance
    if len(df_original) > 5000:
        df_sample = df_original.sample(n=5000, random_state=42)
    else:
        df_sample = df_original
    
    # Create optimized figure
    fig = go.Figure()
    
    # Add scattergeo trace with optimized settings
    fig.add_trace(go.Scattergeo(
        lat=df_sample['Latitude'],
        lon=df_sample['Longitude'],
        mode='markers',
        marker=dict(
            size=6,
            opacity=0.7,
            color=df_sample['Event_Type'].astype('category').cat.codes,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Event Type")
        ),
        text=df_sample['Country'].astype(str) + '<br>' + df_sample['Event_Type'].astype(str) + '<br>' + df_sample['Location'].astype(str),
        hoverinfo='text',
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    # Optimized layout
    fig.update_layout(
        title='All Events Worldwide',
        geo=dict(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            showocean=True,
            oceancolor='rgb(204, 229, 255)',
            showcountries=True,
            countrycolor='rgb(255, 255, 255)',
            coastlinecolor='rgb(128, 128, 128)',
            projection_type='natural earth',
            showframe=False,
            showcoastlines=True,
            coastlinewidth=1
        ),
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False
    )
    
    return fig

def create_maritime_map(df_cleaned):
    """
    Create a map showing only maritime events from the cleaned dataset (optimized for performance)
    
    Args:
        df_cleaned (pd.DataFrame): Cleaned maritime dataset
        
    Returns:
        plotly.graph_objects.Figure: Map figure
    """
    # Sample data if too many points for performance
    if len(df_cleaned) > 2000:
        df_sample = df_cleaned.sample(n=2000, random_state=42)
    else:
        df_sample = df_cleaned
    
    # Create optimized figure
    fig = go.Figure()
    
    # Add scattergeo trace with optimized settings
    fig.add_trace(go.Scattergeo(
        lat=df_sample['Latitude'],
        lon=df_sample['Longitude'],
        mode='markers',
        marker=dict(
            size=8,
            opacity=0.8,
            color=df_sample['Event_Type'].astype('category').cat.codes,
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="Maritime Event Type")
        ),
        text=df_sample['Country'].astype(str) + '<br>' + df_sample['Event_Type'].astype(str) + '<br>' + df_sample['Location'].astype(str),
        hoverinfo='text',
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    # Optimized layout
    fig.update_layout(
        title='Maritime Events Worldwide',
        geo=dict(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            showocean=True,
            oceancolor='rgb(204, 229, 255)',
            showcountries=True,
            countrycolor='rgb(255, 255, 255)',
            coastlinecolor='rgb(128, 128, 128)',
            projection_type='natural earth',
            showframe=False,
            showcoastlines=True,
            coastlinewidth=1
        ),
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False
    )
    
    return fig
