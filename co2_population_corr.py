import pandas as pd
import plotly.express as px
from co2_data import clean_data

def create_population_co2_correlation_figure(selected_countries, start_date, end_date):

    # Load and clean the data
    co2_data = clean_data("owid-co2-data.csv")

    # Check if start_date and end_date are None (or empty)
    if start_date is None or end_date is None:
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

    co2_data = co2_data[co2_data['year'].between(start_year, end_year)]

    # Handle the case where no country is selected (None or empty)
    if not selected_countries or selected_countries == 'all':
        selected_countries = co2_data['country'].unique()  # Default to all countries
    else:
        if isinstance(selected_countries, str):
            selected_countries = [selected_countries]

    # Filter data for the selected countries
    co2_data = co2_data[co2_data['country'].isin(selected_countries)]

    # Calculate correlation coefficient if a single country is selected
    correlation_text = ""
    if len(selected_countries) == 1:
        # Calculate correlation coefficient
        if len(co2_data) > 1:  # Ensure there are enough data points
            corr = co2_data['population'].corr(co2_data['co2'])
            if corr is not None:
                if corr > 0.7:
                    interpretation = "High Positive Correlation"
                elif corr > 0.3:
                    interpretation = "Low Positive Correlation"
                elif corr > -0.3:
                    interpretation = "No Correlation"
                elif corr > -0.7:
                    interpretation = "Low Negative Correlation"
                else:
                    interpretation = "High Negative Correlation"
                correlation_text = f"Correlation Coefficient = {corr:.2f} ({interpretation})"
        else:
            correlation_text = "Insufficient data for correlation"

    # Create scatter plot
    fig = px.scatter(
        co2_data,
        x="population",
        y="co2",
        color="country" if len(selected_countries) > 1 else None,
        hover_name="country" if len(selected_countries) > 1 else None,
        title="Correlation Between Population and CO2 Emissions",
        labels={"population": "Population (in millions)", "co2": "CO2 Emissions (in metric tons)"},
        hover_data=["year"]
    )

    # Add correlation text annotation if applicable
    if correlation_text:
        fig.add_annotation(
            x=0.5, y=-0.25, xref="paper", yref="paper", showarrow=False,
            text=correlation_text, font=dict(size=12, color="black"),
        )

    # Customize plot layout for better presentation
    fig.update_layout(
        title=dict(
            text="Correlation Between Population and CO2 Emissions",
            x=0.5, y=0.95, font=dict(size=24, color="black")
        ),
        paper_bgcolor='white',
        font=dict(color="black", family="Roboto, sans-serif"),
        plot_bgcolor='white',
        xaxis=dict(
            tickfont=dict(color="black"),
            title_font=dict(color="black"),
            showgrid=False,
            linecolor="gray",
            linewidth=2,
        ),
        yaxis=dict(
            tickfont=dict(color="black"),
            title_font=dict(color="black"),
            showgrid=False,
            linecolor="black",
            linewidth=2,
        ),
        margin=dict(l=50, r=50, t=50, b=100),
    )

    return fig
