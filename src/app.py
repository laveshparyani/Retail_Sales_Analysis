import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from sqlalchemy import create_engine
import urllib.parse
import os
from dotenv import load_dotenv
import sqlite3
import traceback

# Load environment variables
load_dotenv()

# Initialize the Dash app with modern theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        "/static/css/style.css"
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

def connect_to_database():
    """Connect to database and fetch data from SQL Server (customers, products) and Excel (sales)"""
    print("\n=== Data Collection Started ===")
    
    try:
        # 1. Get SQL Server data (customers and products only)
        print("\n=== SQL Server Connection Attempt ===")
        conn_str = (
            'DRIVER={SQL Server};'
            'SERVER=DESKTOP-GP07DFE;'
            'DATABASE=RetailSalesDB;'
            'Trusted_Connection=yes;'
        )
        print(f"Connection string: {conn_str}")
        
        # Create engine
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}")
        
        with engine.connect() as conn:
            print("\n=== Fetching Customer and Product Data ===")
            
            # Get customer data from SQL
            customers_df = pd.read_sql_query("SELECT * FROM Customers", conn)
            print(f"Found {len(customers_df)} customers")
            print("Customer IDs:", customers_df['CustomerID'].tolist())
            
            # Get product data from SQL
            products_df = pd.read_sql_query("SELECT * FROM Products", conn)
            print(f"Found {len(products_df)} products")
            print("Product IDs:", products_df['ProductID'].tolist())
            
        # 2. Get sales data from Excel
        print("\n=== Reading Sales Data from Excel ===")
        try:
            sales_df = pd.read_excel('data/sales_data.xlsx')
            print(f"Found {len(sales_df)} sales records in Excel")
            
            # Ensure date format consistency
            sales_df['Date'] = pd.to_datetime(sales_df['Date']).dt.date
            
            # Validate sales data against customers and products
            valid_customer_ids = set(customers_df['CustomerID'].tolist())
            valid_product_ids = set(products_df['ProductID'].tolist())
            
            # Filter out invalid records
            valid_sales = (
                sales_df['CustomerID'].isin(valid_customer_ids) & 
                sales_df['ProductID'].isin(valid_product_ids)
            )
            
            invalid_count = len(sales_df) - valid_sales.sum()
            if invalid_count > 0:
                print(f"Warning: Found {invalid_count} sales records with invalid customer or product IDs")
            
            sales_df = sales_df[valid_sales].copy()
            print(f"Using {len(sales_df)} valid sales records")
            
            # Sort by date
            sales_df = sales_df.sort_values('Date')
            
        except Exception as e:
            print(f"Error reading Excel data: {str(e)}")
            print("Cannot proceed without sales data")
            raise
        
        print("\n=== Data Collection Completed ===")
        return customers_df, products_df, sales_df
            
    except Exception as e:
        print(f"\n=== Database Error ===")
        print(f"Error: {str(e)}")
        print("Stack trace:", traceback.format_exc())
        raise

def create_visualizations(customers_df, products_df, sales_df):
    """Create interactive visualizations"""
    print("\n=== Creating Visualizations ===")
    
    # Merge data
    print("Merging dataframes...")
    print(f"Before merge - Sales: {len(sales_df)}, Customers: {len(customers_df)}, Products: {len(products_df)}")
    
    merged_data = pd.merge(sales_df, customers_df, on='CustomerID')
    print(f"After first merge: {len(merged_data)} rows")
    
    merged_data = pd.merge(merged_data, products_df, on='ProductID')
    print(f"After second merge: {len(merged_data)} rows")
    
    # Convert Date to datetime
    merged_data['Date'] = pd.to_datetime(merged_data['Date'])
    
    # Calculate metrics
    total_revenue = (merged_data['QuantitySold'] * merged_data['Price']).sum()
    total_customers = merged_data['CustomerID'].nunique()
    total_products = merged_data['ProductID'].nunique()
    
    print(f"\nCalculated Metrics:")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Unique Customers: {total_customers}")
    print(f"Unique Products: {total_products}")
    
    # Create visualizations
    print("\nGenerating plots...")
    
    # Sales Trends - Create complete date range and fill missing values
    print("Creating sales trends visualization...")
    
    # Get unique dates and categories
    all_dates = pd.date_range(
        start=merged_data['Date'].min(),
        end=merged_data['Date'].max(),
        freq='D'
    )
    all_categories = merged_data['Category'].unique()
    
    # Create a complete date-category combination DataFrame
    date_category_combos = pd.MultiIndex.from_product(
        [all_dates, all_categories],
        names=['Date', 'Category']
    )
    
    # Create complete DataFrame with all possible combinations
    trends_data = pd.DataFrame(index=date_category_combos).reset_index()
    
    # Merge with actual data
    daily_sales = merged_data.groupby(['Date', 'Category']).agg({
        'QuantitySold': 'sum',
        'Price': lambda x: (x * merged_data.loc[x.index, 'QuantitySold']).sum()
    }).reset_index()
    
    # Merge complete date range with actual data
    trends_data = trends_data.merge(
        daily_sales,
        on=['Date', 'Category'],
        how='left'
    )
    
    # Fill missing values with 0
    trends_data = trends_data.fillna(0)
    
    # Sort by date and category
    trends_data = trends_data.sort_values(['Date', 'Category'])
    
    # Create the sales trends visualization
    fig1 = px.line(
        trends_data,
        x='Date',
        y='Price',
        color='Category',
        title='Sales Trends by Category',
        template='plotly_white',
        labels={
            'Date': 'Date',
            'Price': 'Revenue ($)',
            'Category': 'Product Category'
        }
    )
    
    # Customize the layout
    fig1.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        legend_title="Product Category",
        hovermode='x unified',
        xaxis=dict(
            tickformat='%Y-%m-%d',
            tickmode='auto',
            nticks=10,
            showgrid=True
        ),
        yaxis=dict(
            tickprefix='$',
            tickformat=',.0f',
            showgrid=True
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02
        ),
        margin=dict(r=150)  # Add right margin for legend
    )
    
    # Update line styling
    for trace in fig1.data:
        trace.update(
            mode='lines+markers',  # Add markers at data points
            line=dict(width=2),    # Make lines thicker
            marker=dict(size=6)    # Set marker size
        )
    
    # Update hover template
    fig1.update_traces(
        hovertemplate="<br>".join([
            "<b>%{fullData.name}</b>",
            "Date: %{x|%Y-%m-%d}",
            "Revenue: $%{y:,.2f}",
            "<extra></extra>"
        ])
    )
    
    # Top Locations
    location_data = merged_data.groupby('Location')['QuantitySold'].sum().reset_index().nlargest(5, 'QuantitySold')
    print(f"Location data points: {len(location_data)}")
    fig2 = px.bar(
        location_data,
        x='Location',
        y='QuantitySold',
        title='Top 5 Locations by Sales',
        template='plotly_white'
    )
    
    # Category Distribution
    category_data = merged_data.groupby('Category')['QuantitySold'].sum().reset_index()
    print(f"Category data points: {len(category_data)}")
    fig3 = px.pie(
        category_data,
        values='QuantitySold',
        names='Category',
        title='Sales Distribution by Category',
        template='plotly_white'
    )
    
    # Customer Patterns
    pattern_data = merged_data.groupby('CustomerID').agg({
        'QuantitySold': 'sum',
        'Price': 'mean'
    }).reset_index()
    print(f"Pattern data points: {len(pattern_data)}")
    fig4 = px.scatter(
        pattern_data,
        x='QuantitySold',
        y='Price',
        title='Customer Purchase Patterns',
        template='plotly_white'
    )
    
    print("=== Visualization Creation Complete ===\n")
    return fig1, fig2, fig3, fig4, total_revenue, total_customers, total_products

# Create the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Retail Sales Analysis Dashboard", 
                   className="dashboard-title")
        ], width=12)
    ]),
    
    # Auto-refresh interval - checks every 5 seconds
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    ),
    
    # Last updated timestamp
    dbc.Row([
        dbc.Col([
            html.Div(id='last-updated', className="text-muted text-end")
        ], width=12)
    ], className="mb-3"),
    
    # Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-dollar-sign fa-2x"),
                        html.H3("Total Revenue", className="metric-label"),
                        html.H2(id="total-revenue", className="metric-value")
                    ])
                ])
            ], className="metric-card")
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-users fa-2x"),
                        html.H3("Total Customers", className="metric-label"),
                        html.H2(id="total-customers", className="metric-value")
                    ])
                ])
            ], className="metric-card")
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-box fa-2x"),
                        html.H3("Total Products", className="metric-label"),
                        html.H2(id="total-products", className="metric-value")
                    ])
                ])
            ], className="metric-card")
        ], width=4)
    ], className="mb-4"),
    
    # Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Filters", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Date Range"),
                            dcc.DatePickerRange(
                                id='date-range',
                                start_date=datetime(2024, 1, 1),
                                end_date=datetime(2024, 1, 8),
                                className="mb-2"
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Category"),
                            dcc.Dropdown(
                                id='category-filter',
                                multi=True,
                                className="mb-2"
                            )
                        ], width=6)
                    ])
                ])
            ], className="filter-section")
        ], width=12)
    ]),
    
    # Visualizations
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Sales Trends by Category", className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='sales-trends-graph')
                ])
            ])
        ], width=12, className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Top Locations by Sales", className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='locations-graph')
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Sales Distribution by Category", className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='category-distribution-graph')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("Customer Purchase Patterns", className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='customer-patterns-graph')
                ])
            ])
        ], width=12)
    ]),
    
    # Loading indicator
    dcc.Loading(
        id="loading",
        type="circle",
        children=[html.Div(id="loading-output")]
    )
    
], fluid=True, className="px-4 py-3")

# Callbacks
@app.callback(
    [Output('sales-trends-graph', 'figure'),
     Output('locations-graph', 'figure'),
     Output('category-distribution-graph', 'figure'),
     Output('customer-patterns-graph', 'figure'),
     Output('total-revenue', 'children'),
     Output('total-customers', 'children'),
     Output('total-products', 'children'),
     Output('category-filter', 'options'),
     Output('last-updated', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('category-filter', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_dashboard(start_date, end_date, selected_categories, n_intervals):
    print("\n=== Dashboard Update Triggered ===")
    print(f"Date Range: {start_date} to {end_date}")
    print(f"Selected Categories: {selected_categories}")
    print(f"Update number: {n_intervals}")
    
    try:
        # Fetch data
        customers_df, products_df, sales_df = connect_to_database()
        
        if customers_df is None or products_df is None:
            raise Exception("Failed to load customer or product data")
            
        if sales_df is None:
            raise Exception("Failed to load sales data")
        
        print("\n=== Data Processing ===")
        print(f"Initial data shapes:")
        print(f"Customers: {customers_df.shape}")
        print(f"Products: {products_df.shape}")
        print(f"Sales: {sales_df.shape}")
        
        # Convert dates
        sales_df['Date'] = pd.to_datetime(sales_df['Date'])
        
        # Apply date filter
        if start_date and end_date:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            sales_df = sales_df[
                (sales_df['Date'] >= start_date) & 
                (sales_df['Date'] <= end_date)
            ]
        
        # Merge data
        print("\nMerging data...")
        merged_data = sales_df.merge(customers_df, on='CustomerID', how='left')
        merged_data = merged_data.merge(products_df, on='ProductID', how='left')
        print(f"Merged data shape: {merged_data.shape}")
        
        # Apply category filter
        if selected_categories and len(selected_categories) > 0:
            merged_data = merged_data[merged_data['Category'].isin(selected_categories)]
        
        # Calculate metrics
        total_revenue = (merged_data['QuantitySold'] * merged_data['Price']).sum()
        total_customers = len(customers_df)  # Show total customers in database
        total_products = len(products_df)    # Show total products in database
        
        print("\n=== Metrics ===")
        print(f"Total Revenue: ${total_revenue:,.2f}")
        print(f"Total Customers: {total_customers}")
        print(f"Total Products: {total_products}")
        
        # Create visualizations
        print("\n=== Creating Visualizations ===")
        
        # Sales Trends - Create complete date range and fill missing values
        print("Creating sales trends visualization...")
        
        # Get unique dates and categories
        all_dates = pd.date_range(
            start=merged_data['Date'].min(),
            end=merged_data['Date'].max(),
            freq='D'
        )
        all_categories = merged_data['Category'].unique()
        
        # Create a complete date-category combination DataFrame
        date_category_combos = pd.MultiIndex.from_product(
            [all_dates, all_categories],
            names=['Date', 'Category']
        )
        
        # Create complete DataFrame with all possible combinations
        trends_data = pd.DataFrame(index=date_category_combos).reset_index()
        
        # Merge with actual data
        daily_sales = merged_data.groupby(['Date', 'Category']).agg({
            'QuantitySold': 'sum',
            'Price': lambda x: (x * merged_data.loc[x.index, 'QuantitySold']).sum()
        }).reset_index()
        
        # Merge complete date range with actual data
        trends_data = trends_data.merge(
            daily_sales,
            on=['Date', 'Category'],
            how='left'
        )
        
        # Fill missing values with 0
        trends_data = trends_data.fillna(0)
        
        # Sort by date and category
        trends_data = trends_data.sort_values(['Date', 'Category'])
        
        # Create the sales trends visualization
        fig1 = px.line(
            trends_data,
            x='Date',
            y='Price',
            color='Category',
            title='Sales Trends by Category',
            template='plotly_white',
            labels={
                'Date': 'Date',
                'Price': 'Revenue ($)',
                'Category': 'Product Category'
            }
        )
        
        # Customize the layout
        fig1.update_layout(
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            legend_title="Product Category",
            hovermode='x unified',
            xaxis=dict(
                tickformat='%Y-%m-%d',
                tickmode='auto',
                nticks=10,
                showgrid=True
            ),
            yaxis=dict(
                tickprefix='$',
                tickformat=',.0f',
                showgrid=True
            ),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02
            ),
            margin=dict(r=150)  # Add right margin for legend
        )
        
        # Update line styling
        for trace in fig1.data:
            trace.update(
                mode='lines+markers',  # Add markers at data points
                line=dict(width=2),    # Make lines thicker
                marker=dict(size=6)    # Set marker size
            )
        
        # Update hover template
        fig1.update_traces(
            hovertemplate="<br>".join([
                "<b>%{fullData.name}</b>",
                "Date: %{x|%Y-%m-%d}",
                "Revenue: $%{y:,.2f}",
                "<extra></extra>"
            ])
        )
        
        # Top Locations
        location_data = merged_data.groupby('Location').agg({
            'QuantitySold': 'sum',
            'Price': lambda x: (x * merged_data.loc[x.index, 'QuantitySold']).sum()
        }).reset_index()
        location_data = location_data.nlargest(5, 'Price')
        fig2 = px.bar(
            location_data,
            x='Location',
            y='Price',
            title='Top 5 Locations by Revenue',
            template='plotly_white',
            color='Price',
            color_continuous_scale='Blues'
        )
        fig2.update_layout(
            xaxis_title="Location",
            yaxis_title="Revenue ($)",
            showlegend=False
        )
        
        # Category Distribution
        category_data = merged_data.groupby('Category').agg({
            'QuantitySold': 'sum',
            'Price': lambda x: (x * merged_data.loc[x.index, 'QuantitySold']).sum()
        }).reset_index()
        fig3 = px.pie(
            category_data,
            values='Price',
            names='Category',
            title='Revenue Distribution by Category',
            template='plotly_white',
            hole=0.4
        )
        
        # Customer Patterns
        pattern_data = merged_data.groupby('CustomerID').agg({
            'QuantitySold': 'sum',
            'Price': lambda x: (x * merged_data.loc[x.index, 'QuantitySold']).sum() / merged_data.loc[x.index, 'QuantitySold'].sum()
        }).reset_index()
        fig4 = px.scatter(
            pattern_data,
            x='QuantitySold',
            y='Price',
            title='Customer Purchase Patterns',
            template='plotly_white',
            labels={
                'QuantitySold': 'Total Quantity Purchased',
                'Price': 'Average Spending per Item ($)'
            }
        )
        fig4.update_traces(marker=dict(size=10))
        
        # Get category options
        category_options = [{'label': cat, 'value': cat} 
                          for cat in sorted(products_df['Category'].unique())]
        
        # Format metrics
        formatted_revenue = f"${total_revenue:,.2f}"
        formatted_customers = f"{total_customers:,}"
        formatted_products = f"{total_products:,}"
        
        # Get current timestamp
        last_updated = f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        print("Dashboard update completed successfully")
        return (fig1, fig2, fig3, fig4, formatted_revenue, formatted_customers, 
                formatted_products, category_options, last_updated)
                
    except Exception as e:
        print(f"\n=== Error updating dashboard ===")
        print(f"Error details: {str(e)}")
        print("Stack trace:", traceback.format_exc())
        
        # Return empty figures and error messages
        empty_fig = px.scatter(title="No data available")
        return (empty_fig, empty_fig, empty_fig, empty_fig, 
                "Error", "Error", "Error", [], 
                f"Error: Failed to load data")

if __name__ == '__main__':
    app.run(debug=True) 