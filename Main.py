# maritime_dashboard.py
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np

# Import data cleaning functions
from data_cleaner import clean_maritime_data
# Import chart functions from individual files
from map_charts import create_overview_map, create_maritime_map
from bar_charts import create_event_type_chart, create_country_chart
from line_charts import create_timeline_chart, create_monthly_trend_chart
from pie_charts import create_event_type_pie, create_country_pie, create_sub_event_pie
from heatmap_charts import create_heatmap_chart, create_temporal_heatmap
from scatter_charts import create_lat_lon_scatter, create_time_scatter

# ---------- Enhanced Styling Configuration ----------
# Modern color palette
COLORS = {
    'primary': '#6366f1',
    'secondary': '#8b5cf6', 
    'accent': '#ec4899',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#06b6d4'
}

# Font configuration
FONT_FAMILY = "'Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif"

# ---------- Dash App ----------
app = dash.Dash(__name__)
app.title = "Maritime Risk Dashboard"

# Load cleaned data using the data cleaner
cleaned_data = clean_maritime_data()

# Cache for original data to avoid reloading
_original_data_cache = None

def load_original_data():
    """Load original data without any cleaning - with caching"""
    global _original_data_cache
    if _original_data_cache is not None:
        return _original_data_cache
        
    csv_file = '2024-01-01-2024-12-31.csv'
    columns_needed = ['Event_Date', 'Event_Type', 'Sub_Event_Type', 'Country', 
                     'Location', 'Latitude', 'Longitude', 'Notes']
    
    df_original = pd.read_csv(csv_file, 
                             usecols=columns_needed,
                             dtype={'Country': 'category',
                                   'Event_Type': 'category', 
                                   'Sub_Event_Type': 'category',
                                   'Location': 'string',
                                   'Latitude': 'float32',
                                   'Longitude': 'float32'})
    
    df_original['Event_Date'] = pd.to_datetime(df_original['Event_Date'], format='%m/%d/%Y %H:%M')
    
    _original_data_cache = df_original
    return df_original

# Load both datasets
df_original = load_original_data()
df_cleaned = cleaned_data['df_events']

# Extract variables from cleaned data package
countries_cleaned = cleaned_data['countries']
events_cleaned = cleaned_data['events']

# Cache computed statistics to avoid recalculation
_stats_cache = {
    'countries_original': df_original['Country'].cat.categories.tolist(),
    'events_original': df_original['Event_Type'].cat.categories.tolist(),
    'countries_cleaned_actual': df_cleaned['Country'].unique().tolist(),
    'events_cleaned_actual': df_cleaned['Event_Type'].unique().tolist(),
    'len_df_original': len(df_original),
    'len_df_cleaned': len(df_cleaned)
}

# Extract cached values for easy access
countries_original = _stats_cache['countries_original']
events_original = _stats_cache['events_original']
countries_cleaned_actual = _stats_cache['countries_cleaned_actual']
events_cleaned_actual = _stats_cache['events_cleaned_actual']

# Startup info (only once)
print(f"✓ Dashboard loaded: {_stats_cache['len_df_original']:,} original events → {_stats_cache['len_df_cleaned']:,} maritime events")

# Enhanced layout with sidebar and tabs
app.layout = html.Div([
    # Sidebar
    html.Div([
        # Compact Header
        html.Div([
            html.H2("🌊 Maritime Dashboard", 
                    style={
                        'color': 'white',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '700',
                        'margin': '0',
                        'textAlign': 'center'
                    })
        ], style={
            'padding': '15px',
            'borderBottom': '1px solid rgba(255,255,255,0.1)',
            'marginBottom': '15px'
        }),
        
        # Compact Navigation
        html.Div([
            html.Div([
                html.Span("📊", style={'marginRight': '8px', 'fontSize': '1rem'}),
                html.Span("Dashboard", style={'fontFamily': FONT_FAMILY, 'fontWeight': '600', 'fontSize': '0.9rem'})
            ], style={
                'padding': '8px 15px',
                'backgroundColor': 'rgba(255,255,255,0.1)',
                'borderRadius': '6px',
                'color': 'white',
                'cursor': 'pointer'
            })
        ], style={'marginBottom': '20px'}),
        
        # Compact Stats (Dynamic based on active tab)
        html.Div([
            html.H4("Stats", 
                    style={
                        'color': 'white',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '0.9rem',
                        'fontWeight': '600',
                        'margin': '0 0 10px 0'
                    }),
            html.Div(id='sidebar-stats')
        ], style={
            'padding': '12px',
            'backgroundColor': 'rgba(255,255,255,0.1)',
            'borderRadius': '8px',
            'marginBottom': '15px'
        }),
        
        # Compact Filters
        html.Div([
            html.Label("Date Range", 
                      style={
                          'color': 'rgba(255,255,255,0.9)',
                          'fontFamily': FONT_FAMILY,
                          'fontSize': '0.8rem',
                          'marginBottom': '6px',
                          'display': 'block',
                          'fontWeight': '600'
                      }),
            dcc.DatePickerRange(
                id='date-picker',
                start_date='2024-01-01',
                end_date='2024-12-31',
                display_format='DD/MM/YYYY',
                calendar_orientation='horizontal',
                clearable=False,
                with_portal=False
            ),
            html.Button(
                'Reset Date Filter',
                id='reset-date-btn',
                style={
                    'width': '100%',
                    'padding': '8px 12px',
                    'marginTop': '8px',
                    'backgroundColor': '#ef4444',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '6px',
                    'fontFamily': FONT_FAMILY,
                    'fontSize': '0.875rem',
                    'fontWeight': '600',
                    'cursor': 'pointer',
                    'transition': 'all 0.2s ease',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                }
            )
        ], style={
            'padding': '12px',
            'backgroundColor': 'rgba(255,255,255,0.1)',
            'borderRadius': '8px',
            'marginBottom': '15px'
        })
    ], style={
        'width': '280px',
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'padding': '0',
        'height': '100vh',
        'position': 'fixed',
        'left': '0',
        'top': '0',
        'overflow': 'hidden',
        'boxShadow': '2px 0 10px rgba(0,0,0,0.1)',
        'zIndex': '1000'
    }),
    
    # Main Content Area with Tabs
    html.Div([
        # Tab Navigation
        dcc.Tabs([
            # Overview Tab
            dcc.Tab(
                label='📊 Overview',
                value='overview',
                style={
                    'backgroundColor': '#f8fafc',
                    'color': '#6b7280',
                    'fontFamily': FONT_FAMILY,
                    'fontWeight': '600',
                    'padding': '12px 20px',
                    'border': 'none',
                    'borderBottom': '2px solid #e5e7eb'
                },
                selected_style={
                    'backgroundColor': 'white',
                    'color': COLORS['primary'],
                    'fontFamily': FONT_FAMILY,
                    'fontWeight': '700',
                    'padding': '12px 20px',
                    'border': 'none',
                    'borderBottom': f'2px solid {COLORS["primary"]}'
                }
            ),
            # Maritime Tab
            dcc.Tab(
                label='🌊 Maritime',
                value='maritime',
                style={
                    'backgroundColor': '#f8fafc',
                    'color': '#6b7280',
                    'fontFamily': FONT_FAMILY,
                    'fontWeight': '600',
                    'padding': '12px 20px',
                    'border': 'none',
                    'borderBottom': '2px solid #e5e7eb'
                },
                selected_style={
                    'backgroundColor': 'white',
                    'color': COLORS['primary'],
                    'fontFamily': FONT_FAMILY,
                    'fontWeight': '700',
                    'padding': '12px 20px',
                    'border': 'none',
                    'borderBottom': f'2px solid {COLORS["primary"]}'
                }
            )
        ], id='tabs', value='overview', style={
            'backgroundColor': '#f8fafc',
            'borderRadius': '0',  # Remove border radius to fill full width
            'border': '1px solid #e5e7eb',
            'height': '50px',  # Fixed height for tab navigation
            'flexShrink': '0',  # Don't shrink this element
            'width': '100%'  # Fill full width
        }),
        
        # Tab Content
        html.Div(id='tab-content', style={
            'backgroundColor': 'white', 
            'borderRadius': '0',  # Remove border radius to fill full width
            'border': '1px solid #e5e7eb',
            'borderTop': 'none',
            'height': 'calc(100vh - 50px)',  # Fill remaining screen height (50px tab height)
            'padding': '20px', 
            'overflow': 'auto',  # Allow scrolling if content is too tall
            'flex': '1',  # Take remaining space in flex container
            'width': '100%'  # Fill full width
        })
    ], style={
        'marginLeft': '280px',
        'padding': '0',  # Remove padding to fill full width
        'backgroundColor': '#f4f4f4',
        'height': '100vh',  # Full viewport height
        'display': 'flex',
        'flexDirection': 'column',
        'width': 'calc(100vw - 280px)'  # Fill remaining width after sidebar
    })

], style={
    'fontFamily': FONT_FAMILY,
    'backgroundColor': '#f4f4f4',
    'margin': '0',
    'padding': '0',
    'minHeight': '100vh',
    'display': 'flex'
})

# Callback to update sidebar stats based on active tab and date range
@app.callback(
    Output('sidebar-stats', 'children'),
    [Input('tabs', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_sidebar_stats(active_tab, start_date, end_date):
    # Filter data based on date range
    if start_date and end_date:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        # Filter original data
        df_original_filtered = df_original[
            (df_original['Event_Date'] >= start_dt) & 
            (df_original['Event_Date'] <= end_dt)
        ]
        
        # Filter cleaned data
        df_cleaned_filtered = df_cleaned[
            (df_cleaned['Event_Date'] >= start_dt) & 
            (df_cleaned['Event_Date'] <= end_dt)
        ]
        
        # Get filtered statistics
        countries_original_filtered = df_original_filtered['Country'].unique().tolist()
        events_original_filtered = df_original_filtered['Event_Type'].unique().tolist()
        countries_cleaned_filtered = df_cleaned_filtered['Country'].unique().tolist()
        events_cleaned_filtered = df_cleaned_filtered['Event_Type'].unique().tolist()
        
        len_df_original_filtered = len(df_original_filtered)
        len_df_cleaned_filtered = len(df_cleaned_filtered)
    else:
        # Use cached values if no date filter
        len_df_original_filtered = _stats_cache['len_df_original']
        len_df_cleaned_filtered = _stats_cache['len_df_cleaned']
        countries_original_filtered = _stats_cache['countries_original']
        events_original_filtered = _stats_cache['events_original']
        countries_cleaned_filtered = _stats_cache['countries_cleaned_actual']
        events_cleaned_filtered = _stats_cache['events_cleaned_actual']
    
    if active_tab == 'overview':
        return [
            html.Div([
                html.Span("Events: ", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.7)'}),
                html.Span(f"{len_df_original_filtered:,}", style={'fontSize': '0.9rem', 'fontWeight': '700', 'color': 'white'})
            ], style={'marginBottom': '5px'}),
            html.Div([
                html.Span("Countries: ", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.7)'}),
                html.Span(f"{len(countries_original_filtered)}", style={'fontSize': '0.9rem', 'fontWeight': '700', 'color': 'white'})
            ], style={'marginBottom': '5px'}),
            html.Div([
                html.Span("Types: ", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.7)'}),
                html.Span(f"{len(events_original_filtered)}", style={'fontSize': '0.9rem', 'fontWeight': '700', 'color': 'white'})
            ])
        ]
    else:  # maritime tab
        return [
            html.Div([
                html.Span("Events: ", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.7)'}),
                html.Span(f"{len_df_cleaned_filtered:,}", style={'fontSize': '0.9rem', 'fontWeight': '700', 'color': 'white'})
            ], style={'marginBottom': '5px'}),
            html.Div([
                html.Span("Coastal Countries: ", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.7)'}),
                html.Span(f"{len(countries_cleaned_filtered)}", style={'fontSize': '0.9rem', 'fontWeight': '700', 'color': 'white'})
            ], style={'marginBottom': '5px'}),
            html.Div([
                html.Span("Types: ", style={'fontSize': '0.75rem', 'color': 'rgba(255,255,255,0.7)'}),
                html.Span(f"{len(events_cleaned_filtered)}", style={'fontSize': '0.9rem', 'fontWeight': '700', 'color': 'white'})
            ])
        ]

# Callback to update tab content with date filtering
@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def render_tab_content(tab, start_date, end_date):
    # Filter data based on date range
    if start_date and end_date:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        # Filter original data
        df_original_filtered = df_original[
            (df_original['Event_Date'] >= start_dt) & 
            (df_original['Event_Date'] <= end_dt)
        ]
        
        # Filter cleaned data
        df_cleaned_filtered = df_cleaned[
            (df_cleaned['Event_Date'] >= start_dt) & 
            (df_cleaned['Event_Date'] <= end_dt)
        ]
        
        # Get filtered statistics
        countries_original_filtered = df_original_filtered['Country'].unique().tolist()
        events_original_filtered = df_original_filtered['Event_Type'].unique().tolist()
        countries_cleaned_filtered = df_cleaned_filtered['Country'].unique().tolist()
        events_cleaned_filtered = df_cleaned_filtered['Event_Type'].unique().tolist()
        
        len_df_original_filtered = len(df_original_filtered)
        len_df_cleaned_filtered = len(df_cleaned_filtered)
    else:
        # Use cached values if no date filter
        df_original_filtered = df_original
        df_cleaned_filtered = df_cleaned
        len_df_original_filtered = _stats_cache['len_df_original']
        len_df_cleaned_filtered = _stats_cache['len_df_cleaned']
        countries_original_filtered = _stats_cache['countries_original']
        events_original_filtered = _stats_cache['events_original']
        countries_cleaned_filtered = _stats_cache['countries_cleaned_actual']
        events_cleaned_filtered = _stats_cache['events_cleaned_actual']
    
    if tab == 'overview':
        return html.Div([
            html.H1("📊 Overview Dashboard", style={
                'color': '#1f2937',
                'fontFamily': FONT_FAMILY,
                'fontSize': '2rem',
                'fontWeight': '700',
                'marginBottom': '30px'
            }),
            
            # Metrics Row
            html.Div([
                html.Div([
                    html.H3("Total Events", style={'margin': '0 0 10px 0', 'fontSize': '1.2rem', 'fontWeight': '600'}),
                    html.P(f"{len_df_original_filtered:,}", style={'margin': '0', 'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['primary']})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)', 'border': '1px solid #e5e7eb', 'width': 'calc(25% - 15px)'}),
                
                html.Div([
                    html.H3("Countries", style={'margin': '0 0 10px 0', 'fontSize': '1.2rem', 'fontWeight': '600'}),
                    html.P(f"{len(countries_original_filtered)}", style={'margin': '0', 'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['secondary']})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)', 'border': '1px solid #e5e7eb', 'width': 'calc(25% - 15px)'}),
                
                html.Div([
                    html.H3("Event Types", style={'margin': '0 0 10px 0', 'fontSize': '1.2rem', 'fontWeight': '600'}),
                    html.P(f"{len(events_original_filtered)}", style={'margin': '0', 'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['accent']})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)', 'border': '1px solid #e5e7eb', 'width': 'calc(25% - 15px)'}),
                
                html.Div([
                    html.H3("Data Quality", style={'margin': '0 0 10px 0', 'fontSize': '1.2rem', 'fontWeight': '600'}),
                    html.P("Raw", style={'margin': '0', 'fontSize': '1.5rem', 'fontWeight': '700', 'color': COLORS['warning']})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)', 'border': '1px solid #e5e7eb', 'width': 'calc(25% - 15px)'})
            ], style={
                'display': 'flex', 
                'gap': '20px', 
                'marginBottom': '30px',
                'width': '100%'
            }),
            
            # Overview Content
            html.Div([
                html.H2("Raw Data Overview", style={
                    'color': '#374151',
                    'fontFamily': FONT_FAMILY,
                    'fontSize': '1.5rem',
                    'fontWeight': '600',
                    'marginBottom': '20px'
                }),
                html.P("This tab shows the original dataset without any cleaning or filtering applied. All 38,512 events from the CSV file are displayed here.", style={
                    'color': '#6b7280',
                    'fontFamily': FONT_FAMILY,
                    'fontSize': '1rem',
                    'lineHeight': '1.6',
                    'marginBottom': '20px'
                }),
                html.P("Switch to the Maritime tab to see the cleaned and filtered data with only relevant maritime incidents.", style={
                    'color': '#6b7280',
                    'fontFamily': FONT_FAMILY,
                    'fontSize': '1rem',
                    'lineHeight': '1.6'
                })
            ], style={
                'backgroundColor': '#f9fafb',
                'padding': '30px',
                'borderRadius': '12px',
                'border': '1px solid #e5e7eb',
                'marginBottom': '20px'
            }),
            
            # Map for Overview tab
            html.Div([
                html.H3("All Events Map", style={
                    'color': '#374151',
                    'fontFamily': FONT_FAMILY,
                    'fontSize': '1.4rem',
                    'fontWeight': '600',
                    'marginBottom': '15px'
                }),
                dcc.Graph(
                    id='overview-map',
                    figure=create_overview_map(df_original_filtered),
                    style={'height': '500px', 'width': '100%'}
                )
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '12px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                'border': '1px solid #e5e7eb'
            })
        ])
    
    elif tab == 'maritime':
        return html.Div([
            html.H1("🌊 Maritime Analysis", style={
                'color': '#1f2937',
                'fontFamily': FONT_FAMILY,
                'fontSize': '2rem',
                'fontWeight': '700',
                'marginBottom': '30px'
            }),
            
            # Metrics Row
            html.Div([
                html.Div([
                    html.H3("Clean Events", style={'margin': '0 0 10px 0', 'fontSize': '1.2rem', 'fontWeight': '600'}),
                    html.P(f"{len_df_cleaned_filtered:,}", style={'margin': '0', 'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['primary']})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)', 'border': '1px solid #e5e7eb', 'width': 'calc(25% - 15px)'}),
                
                html.Div([
                    html.H3("Coastal Countries", style={'margin': '0 0 10px 0', 'fontSize': '1.2rem', 'fontWeight': '600'}),
                    html.P(f"{len(countries_cleaned_filtered)}", style={'margin': '0', 'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['secondary']})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)', 'border': '1px solid #e5e7eb', 'width': 'calc(25% - 15px)'}),
                
                html.Div([
                    html.H3("Maritime Types", style={'margin': '0 0 10px 0', 'fontSize': '1.2rem', 'fontWeight': '600'}),
                    html.P(f"{len(events_cleaned_filtered)}", style={'margin': '0', 'fontSize': '2rem', 'fontWeight': '700', 'color': COLORS['accent']})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)', 'border': '1px solid #e5e7eb', 'width': 'calc(25% - 15px)'}),
                
                html.Div([
                    html.H3("Data Quality", style={'margin': '0 0 10px 0', 'fontSize': '1.2rem', 'fontWeight': '600'}),
                    html.P("Clean", style={'margin': '0', 'fontSize': '1.5rem', 'fontWeight': '700', 'color': COLORS['success']})
                ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)', 'border': '1px solid #e5e7eb', 'width': 'calc(25% - 15px)'})
            ], style={
                'display': 'flex', 
                'gap': '20px', 
                'marginBottom': '30px',
                'width': '100%'
            }),
            
            # Maritime-specific content
            html.Div([
                html.H2("Cleaned Maritime Data", style={
                    'color': '#374151',
                    'fontFamily': FONT_FAMILY,
                    'fontSize': '1.5rem',
                    'fontWeight': '600',
                    'marginBottom': '20px'
                }),
                html.P("This section shows the cleaned and filtered maritime data. Only events that meet all criteria are included:", style={
                    'color': '#6b7280',
                    'fontFamily': FONT_FAMILY,
                    'fontSize': '1rem',
                    'lineHeight': '1.6',
                    'marginBottom': '20px'
                }),
                html.Ul([
                    html.Li("Contain maritime keywords in Notes", style={'color': '#6b7280', 'fontFamily': FONT_FAMILY, 'fontSize': '1rem', 'marginBottom': '8px'}),
                    html.Li("Are in ocean coordinates", style={'color': '#6b7280', 'fontFamily': FONT_FAMILY, 'fontSize': '1rem', 'marginBottom': '8px'}),
                    html.Li("Are in coastal countries", style={'color': '#6b7280', 'fontFamily': FONT_FAMILY, 'fontSize': '1rem', 'marginBottom': '8px'}),
                    html.Li("Are not riots/protests", style={'color': '#6b7280', 'fontFamily': FONT_FAMILY, 'fontSize': '1rem', 'marginBottom': '8px'}),
                    html.Li("Do not contain 'Township' in Notes", style={'color': '#6b7280', 'fontFamily': FONT_FAMILY, 'fontSize': '1rem', 'marginBottom': '8px'})
                ], style={'marginBottom': '20px'}),

            ], style={
                'backgroundColor': '#f9fafb',
                'padding': '30px',
                'borderRadius': '12px',
                'border': '1px solid #e5e7eb',
                'marginBottom': '20px'
            }),
            
            # Map for Maritime tab
            html.Div([
                html.H3("Maritime Events Map", style={
                    'color': '#374151',
                    'fontFamily': FONT_FAMILY,
                    'fontSize': '1.4rem',
                    'fontWeight': '600',
                    'marginBottom': '15px'
                }),
                dcc.Graph(
                    id='maritime-map',
                    figure=create_maritime_map(df_cleaned_filtered),
                    style={'height': '500px', 'width': '100%'}
                )
            ], style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '12px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                'border': '1px solid #e5e7eb',
                'marginBottom': '20px'
            }),
            
            # Charts Grid - Row 1: Bar Charts
            html.Div([
                html.Div([
                    html.H3("Event Type Distribution", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_event_type_chart(df_cleaned_filtered, "Maritime Event Types"),
                        style={'height': '400px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(50% - 10px)',
                    'height': '460px',
                    'overflow': 'hidden'
                }),
                
                html.Div([
                    html.H3("Top Maritime Countries", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_country_chart(df_cleaned_filtered, "Countries with Most Maritime Events"),
                        style={'height': '400px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(50% - 10px)',
                    'height': '460px',
                    'overflow': 'hidden'
                })
            ], style={
                'display': 'flex',
                'gap': '20px',
                'marginBottom': '20px',
                'width': '100%'
            }),
            
            # Charts Grid - Row 2: Line Charts
            html.Div([
                html.Div([
                    html.H3("Daily Timeline", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_timeline_chart(df_cleaned_filtered, "Maritime Events Over Time"),
                        style={'height': '400px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(50% - 10px)',
                    'height': '460px',
                    'overflow': 'hidden'
                }),
                
                html.Div([
                    html.H3("Monthly Trends", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_monthly_trend_chart(df_cleaned_filtered, "Monthly Maritime Event Trends"),
                        style={'height': '400px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(50% - 10px)',
                    'height': '460px',
                    'overflow': 'hidden'
                })
            ], style={
                'display': 'flex',
                'gap': '20px',
                'marginBottom': '20px',
                'width': '100%'
            }),
            
            # Charts Grid - Row 3: Pie Charts
            html.Div([
                html.Div([
                    html.H3("Event Type Breakdown", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_event_type_pie(df_cleaned_filtered, "Maritime Event Type Distribution"),
                        style={'height': '400px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(33.33% - 14px)',
                    'height': '460px',
                    'overflow': 'hidden'
                }),
                
                html.Div([
                    html.H3("Top Countries", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_country_pie(df_cleaned_filtered, "Top Maritime Countries", 8),
                        style={'height': '400px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(33.33% - 14px)',
                    'height': '460px',
                    'overflow': 'hidden'
                }),
                
                html.Div([
                    html.H3("Sub-Event Types", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_sub_event_pie(df_cleaned_filtered, "Sub-Event Type Distribution"),
                        style={'height': '400px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(33.33% - 14px)',
                    'height': '460px',
                    'overflow': 'hidden'
                })
            ], style={
                'display': 'flex',
                'gap': '20px',
                'marginBottom': '20px',
                'width': '100%'
            }),
            
            # Charts Grid - Row 4: Heatmaps
            html.Div([
                html.Div([
                    html.H3("Country vs Event Type Heatmap", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_heatmap_chart(df_cleaned_filtered, "Maritime Events by Country and Type"),
                        style={'height': '500px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(50% - 10px)',
                    'height': '560px',
                    'overflow': 'hidden'
                }),
                
                html.Div([
                    html.H3("Temporal Heatmap", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_temporal_heatmap(df_cleaned_filtered, "Maritime Events by Month and Type"),
                        style={'height': '500px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(50% - 10px)',
                    'height': '560px',
                    'overflow': 'hidden'
                })
            ], style={
                'display': 'flex',
                'gap': '20px',
                'marginBottom': '20px',
                'width': '100%'
            }),
            
            # Charts Grid - Row 5: Scatter Plots
            html.Div([
                html.Div([
                    html.H3("Geographic Scatter Plot", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_lat_lon_scatter(df_cleaned_filtered, "Maritime Events by Coordinates"),
                        style={'height': '500px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(50% - 10px)',
                    'height': '560px',
                    'overflow': 'hidden'
                }),
                
                html.Div([
                    html.H3("Time Scatter Plot", style={
                        'color': '#374151',
                        'fontFamily': FONT_FAMILY,
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'marginBottom': '15px'
                    }),
                    dcc.Graph(
                        figure=create_time_scatter(df_cleaned_filtered, "Maritime Events Timeline by Type"),
                        style={'height': '500px', 'width': '100%'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.05)',
                    'border': '1px solid #e5e7eb',
                    'width': 'calc(50% - 10px)',
                    'height': '560px',
                    'overflow': 'hidden'
                })
            ], style={
                'display': 'flex',
                'gap': '20px',
                'marginBottom': '20px',
                'width': '100%'
            })
        ])

# Callback to reset date filter
@app.callback(
    [Output('date-picker', 'start_date'),
     Output('date-picker', 'end_date')],
    Input('reset-date-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_date_filter(n_clicks):
    if n_clicks:
        return '2024-01-01', '2024-12-31'
    return dash.no_update, dash.no_update

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
