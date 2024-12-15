import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from co2_data import clean_data
from population_trend import create_population_trend_figure
from co2_trend import create_co2_emission_trend_figure
from co2_population_corr import create_population_co2_correlation_figure
from co2_sources import update_co2_sources_graph

# Initialize Dash app
app = dash.Dash(__name__)

co2_data = clean_data("owid-co2-data.csv")

# App Layout
app.layout = html.Div(className="dashboard-container", children=[
    # Dashboard Title
    html.Div(className="dashboard-title", children="Global CO2 Emissions and Population Trends"),

    # Date Picker and Country Dropdown
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': 'All Countries', 'value': 'all'}] + 
                    [{'label': country, 'value': country} for country in sorted(co2_data['country'].unique())],
            value='all',
            multi=True,  # Allow multiple countries to be selected
            placeholder="Select a country",
            style={'width': '400px'}  # Adjust the width here
        ),
        # Year Input Range
        html.Div([
            html.Label('Start Year', style={'font-size': '12px', 'margin-right': '10px'}),
            dcc.Input(id='start-year-input', type='number', value=1850, min=1750, max=2023, style={'width': '100px'}),

            html.Label('End Year', style={'font-size': '12px', 'margin-left': '10px'}),
            dcc.Input(id='end-year-input', type='number', value=2023, min=1750, max=2023, style={'width': '100px'})
        ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),

    # Tabs
    dcc.Tabs(id="tabs", children=[
        # Tab 1: CO2 Emission Trend
        dcc.Tab(label="CO2 Emission Trend", children=[
            html.Div([ 
                # Contextual Description (Top Left)
                html.P(
                    "This chart shows the historical trend of CO2 emissions for selected countries. "
                    "Use the filter above to compare multiple countries and examine trends over time.",
                    style={'font-size': '16px', 'color': 'black', 'margin-bottom': '15px', 'text-align': 'left'}
                ),
                # CO2 Emission Trend Graph (Resized to accommodate the interactive guide)
                dcc.Graph(id="co2-emission-graph", figure=create_co2_emission_trend_figure('all', "1850-01-01", "2023-12-31"),
                          style={'width': '80%', 'height': '500px'}),
                
                # Interactive Guide (Right Side)
                html.Div(
                    html.P(
                        "Notice how CO2 emissions have changed over the years. Do any countries show "
                        "significant increases or decreases? Think about what could influence these changes.", 
                        style={'font-size': '15px','font-style': 'italic', 'color': 'black', 'text-align': 'right', 'width': '20%', 'margin-top': '-200px'}
                    ),
                    style={'display': 'flex', 'justify-content': 'flex-end', 'align-items': 'center', 'position': 'absolute', 'top': '350px', 'right': '50px'}
                ),
            ], style={'position': 'relative'}),
        ]),

        # Tab 2: Population Trend
        dcc.Tab(label="Population Trend", children=[
            html.Div([ 
                # Contextual Description (Top Left)
                html.P(
                    "This chart visualizes population growth over time." 
                    "Use the filter to explore different countries and understand how their populations have increased over the years",
                    style={'font-size': '16px', 'color': 'black', 'margin-bottom': '15px', 'text-align': 'left'}
                ),
                # Population Trend Graph (Resized to accommodate the interactive guide)
                dcc.Graph(id="population-trend-graph", figure=update_co2_sources_graph('all', "1850-01-01", "2023-12-31"),
                          style={'width': '80%', 'height': '500px'}),
                
                # Interactive Guide (Right Side)
                html.Div(
                    html.P(
                        "As the population grows, what other factors could contribute to CO2 emissions? "
                        "Explore the next tab to see how population growth relates to emissions.", 
                        style={'font-size': '15px','font-style': 'italic', 'color': 'black', 'text-align': 'right', 'width': '20%', 'margin-top': '-200px'}
                    ),
                    style={'display': 'flex', 'justify-content': 'flex-end', 'align-items': 'center', 'position': 'absolute', 'top': '350px', 'right': '50px'}
                ),
            ], style={'position': 'relative'}),
        ]),

        # Tab 3: Population-CO2 Correlation (Doesn't get affected by the date picker)
        dcc.Tab(label="Population-CO2 Correlation", children=[
            html.Div([ 
                # Contextual Description (Top Left)
                html.P(
                    "This scatter plot examines the relationship between population size and CO2 emissions over time. "
                    "Hover over each data point to view the year, population size, and CO2 emissions for that specific country and year.",
                    style={'font-size': '16px', 'color': 'black', 'margin-bottom': '15px', 'text-align': 'left'}
                ),
                # Correlation Graph (Resized to accommodate the interactive guide)
                dcc.Graph(id="correlation-graph", figure=create_population_co2_correlation_figure('all', "1850-01-01", "2023-12-31"),
                          style={'width': '80%', 'height': '500px'}),
                
                # Interactive Guide (Right Side)
                html.Div(
                    html.P(
                        "Does population growth consistently lead to increased CO2 emissions?  "
                        "Use the country filter to explore specific nations and observe how their trends vary over time. "
                        "Look for clusters or outliers to spot unique patterns.", 
                        style={'font-size': '15px','font-style': 'italic', 'color': 'black', 'text-align': 'right', 'width': '20%', 'margin-top': '-200px'}
                    ),
                    style={'display': 'flex', 'justify-content': 'flex-end', 'align-items': 'center', 'position': 'absolute', 'top': '350px', 'right': '50px'}
                ),
            ], style={'position': 'relative'}),
        ]),

        # Tab 4: CO2 Emission Sources
        dcc.Tab(label="CO2 Emission Sources", children=[
            html.Div([ 
                # Contextual Description (Top Left)
                html.P(
                    "This chart breaks down CO2 emissions by source—coal, oil, natural gas, flaring, and cement—for each country. "
                    "Use the filters to explore how the composition of CO2 sources varies between countries and over time.",
                    style={'font-size': '16px', 'color': 'black', 'margin-bottom': '15px', 'text-align': 'left'}
                ),
                # CO2 Emission Sources Graph (Resized to accommodate the interactive guide)
                dcc.Graph(id="co2-emission-sources-graph", figure=create_population_co2_correlation_figure('all', "1850-01-01", "2023-12-31"),
                          style={'width': '80%', 'height': '500px'}),
                
                # Interactive Guide (Right Side)
                html.Div(
                    html.P(
                        "Which sources contribute the most to CO2 emissions for each country? "
                        "Are there countries that rely heavily on a single source, such as coal or oil?", 
                        style={'font-size': '15px','font-style': 'italic', 'color': 'black', 'text-align': 'right', 'width': '20%', 'margin-top': '-200px'}
                    ),
                    style={'display': 'flex', 'justify-content': 'flex-end', 'align-items': 'center', 'position': 'absolute', 'top': '350px', 'right': '50px'}
                ),
            ], style={'position': 'relative'}),
        ]),
    ])
])

# Callback for CO2 Emission Trend and Population Trend (Tabs 1 and 2)
@app.callback(
    [Output('co2-emission-graph', 'figure'),
     Output('population-trend-graph', 'figure'),
     Output('correlation-graph', 'figure'),
     Output('co2-emission-sources-graph', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('start-year-input', 'value'),
     Input('end-year-input', 'value')]
)
def update_graphs(selected_countries, start_year, end_year):
    # Convert years to date format 'YYYY-01-01' and 'YYYY-12-31'
    start_date = f"{start_year}-01-01"
    end_date = f"{end_year}-12-31"

    if not selected_countries or selected_countries == ['all']:
        selected_countries = None  # This allows all countries if 'all' is selected or if no countries are selected

    # CO2 Emission Trend
    co2_fig = create_co2_emission_trend_figure(selected_countries, start_date, end_date)
    
    # Population Trend
    pop_fig = create_population_trend_figure(selected_countries, start_date, end_date)
    
    # Scatter Plot for Population and CO2
    scatter_fig = create_population_co2_correlation_figure(selected_countries, start_date, end_date)
    
    # CO2 Emission Sources Graph (from the second script)
    co2_source_fig = update_co2_sources_graph(selected_countries, start_date, end_date)  # Call the function from the second script
    
    return co2_fig, pop_fig, scatter_fig, co2_source_fig  # Return the updated figures
    

if __name__ == '__main__':
    app.run_server(debug=True)
