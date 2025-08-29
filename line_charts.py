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
            title=dict(font=dict(size=14, color='#64748b'))
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            zeroline=False,
            title=dict(font=dict(size=14, color='#64748b'))
        )
    )
    
    # Update line styling
    fig.update_traces(
        line=dict(color='#667eea', width=3),
        marker=dict(size=6, color='#667eea'),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)'
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
            tickangle=-45,
            title=dict(font=dict(size=14, color='#64748b'))
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            zeroline=False,
            title=dict(font=dict(size=14, color='#64748b'))
        )
    )
    
    # Update line styling
    fig.update_traces(
        line=dict(color='#764ba2', width=3),
        marker=dict(size=6, color='#764ba2'),
        fill='tonexty',
        fillcolor='rgba(118, 75, 162, 0.1)'
    )
    
    return fig

