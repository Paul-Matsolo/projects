# bar_charts.py - Bar chart visualization functions
import plotly.express as px

def create_event_type_chart(df, title="Event Type Distribution"):
    """
    Create a bar chart showing event type distribution
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    # Only show event types that actually exist in the filtered data
    event_counts = df['Event_Type'].value_counts()
    # Remove any zero counts (shouldn't happen with unused categories removed, but safety check)
    event_counts = event_counts[event_counts > 0]
    
    fig = px.bar(
        x=event_counts.index,
        y=event_counts.values,
        title=title,
        labels={'x': 'Event Type', 'y': 'Count'},
        color=event_counts.values,
        color_continuous_scale='Viridis'
    ).update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        title=dict(
            font=dict(size=18, color='#1e293b'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            zeroline=False,
            title=dict(font=dict(size=14, color='#64748b')),
            tickangle=-45
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            zeroline=False,
            title=dict(font=dict(size=14, color='#64748b'))
        ),
        coloraxis_colorbar=dict(
            title="Count",
            titlefont=dict(size=12, color='#64748b'),
            tickfont=dict(size=10, color='#64748b')
        )
    )
    
    return fig

def create_country_chart(df, title="Top Countries by Event Count"):
    """
    Create a horizontal bar chart showing top countries by event count
    
    Args:
        df (pd.DataFrame): Dataset to analyze
        title (str): Chart title
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    # Only show countries that actually exist in the filtered data
    country_counts = df['Country'].value_counts().head(15)
    # Remove any zero counts (shouldn't happen with unused categories removed, but safety check)
    country_counts = country_counts[country_counts > 0]
    
    fig = px.bar(
        x=country_counts.values,
        y=country_counts.index,
        orientation='h',
        title=title,
        labels={'x': 'Event Count', 'y': 'Country'},
        color=country_counts.values,
        color_continuous_scale='Plasma'
    ).update_layout(
        height=500,
        margin=dict(l=100, r=50, t=50, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        title=dict(
            font=dict(size=18, color='#1e293b'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            zeroline=False,
            title=dict(font=dict(size=14, color='#64748b'))
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            zeroline=False,
            title=dict(font=dict(size=14, color='#64748b'))
        ),
        coloraxis_colorbar=dict(
            title="Count",
            titlefont=dict(size=12, color='#64748b'),
            tickfont=dict(size=10, color='#64748b')
        )
    )
    
    return fig
