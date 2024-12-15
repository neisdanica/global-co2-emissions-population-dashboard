# Second Tab shows the population trend of each country.
import plotly.express as px
from co2_data import clean_data

def create_population_trend_figure(selected_countries, start_date, end_date):

    # Filter data based on selected countries and date range
    co2_data = clean_data("owid-co2-data.csv")

    # Check if start_date and end_date are None (or empty)
    if start_date is None or end_date is None:
        # Optionally handle the case where no date range is selected (e.g., use the full range or return an error)
        return px.bar(
            title="Please select a valid date range.",
            labels={"emissions": "Total Emissions", "year": "Year"}
        )

    # Ensure valid date range format (YYYY-MM-DD) and convert to year integer
    try:
        start_year = int(start_date[:4])
        end_year = int(end_date[:4])
    except ValueError:
        return px.bar(
            title="Invalid date range selected.",
            labels={"emissions": "Total Emissions", "year": "Year"}
        )

    co2_data = co2_data[co2_data['year'].between(int(start_date[:4]), int(end_date[:4]))]

    # Handle the case where no country is selected (None or empty)
    if not selected_countries or selected_countries == 'all':
        selected_countries = co2_data['country'].unique()  # Default to all countries
    else:
        # Ensure selected_countries is always a list
        if isinstance(selected_countries, str):
            selected_countries = [selected_countries]

    # Filter data for the selected countries
    co2_data = co2_data[co2_data['country'].isin(selected_countries)]

    # Selecting the necessary columns for the graph
    population_by_country = co2_data[['country', 'year', 'population']]

    # Create interactive line chart
    fig = px.line(
        population_by_country,
        x="year",
        y="population",
        color="country",
        title="Population Growth Trend",
        labels={"population": "Population (in millions)", "year": "Year"},
    )

    # Define the custom color palette
    color_palette = px.colors.qualitative.Set1

    # Apply the color palette to the chart
    fig.update_traces(marker=dict(line=dict(width=2, color='white')), 
                      line=dict(width=2), 
                      marker_color=color_palette)

    # Customize the layout for light background, plot area with light blue, and border
    fig.update_layout(
        title=dict(
            text="Population Trend by Country",
            x=0.5,  # Center the title
            y=0.95,  # Adjust the position
            font=dict(size=24, color="black")  # Black title color
        ),
        paper_bgcolor='white',  # White background for the overall chart
        font=dict(color="black", family="Roboto, sans-serif"),  # Black text color
        plot_bgcolor='white',  # Light blue plot area background (hex code)
        xaxis=dict(
            tickfont=dict(color="black"),  # Black color for x-axis ticks
            title_font=dict(color="black"),  # Black color for x-axis title
            showgrid=False,  # No grid lines
            linecolor="gray",  # Border color for x-axis
            linewidth=2,  # Line width for x-axis border
        ),
        yaxis=dict(
            tickfont=dict(color="black"),  # Black color for y-axis ticks
            title_font=dict(color="black"),  # Black color for y-axis title
            showgrid=False,  # No grid lines
            linecolor="black",  # Border color for y-axis
            linewidth=2,  # Line width for y-axis border
        ),
        margin=dict(l=50, r=50, t=50, b=50),  # Adjusting margins for better space
    )

    return fig

