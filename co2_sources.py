import pandas as pd
import plotly.express as px
from co2_data import clean_data

def update_co2_sources_graph(selected_country, start_date, end_date):

    # Load and clean the dataset
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

    # Prepare the dataset for the CO2 emission sources analysis
    co2_sources_by_country = co2_data[['country', 'year', 'cement_co2', 'coal_co2', 'gas_co2', 'flaring_co2', 'oil_co2']]

    # Aggregate CO2 sources by country
    co2_sources_by_country = co2_sources_by_country.groupby(['country', 'year'], as_index=False)[['cement_co2', 'coal_co2', 'gas_co2', 'flaring_co2', 'oil_co2']].sum()

    # Melt the dataframe for visualization
    co2_source_melted = co2_sources_by_country.melt(
        id_vars=['country', 'year'],
        value_vars=['cement_co2', 'coal_co2', 'gas_co2', 'flaring_co2', 'oil_co2'],
        var_name='source',
        value_name='emissions'
    )

    # Filter the data based on the start and end dates
    filtered_data = co2_source_melted[
        (co2_source_melted['year'] >= start_year) & 
        (co2_source_melted['year'] <= end_year)
    ]

    if selected_country == 'all':
        aggregated_data = filtered_data.groupby(['year', 'source'], as_index=False)['emissions'].sum()
        title = "CO2 Emission Sources (All Countries)"
    else:
        if not isinstance(selected_country, list):
            selected_country = [selected_country]
        filtered_data = filtered_data[filtered_data['country'].str.strip().isin(selected_country)]
        if filtered_data.empty:
            return px.bar(
                title="No Data Available for the Selected Filters",
                labels={"emissions": "Total Emissions", "source": "CO2 Emission Sources"}
            )
        aggregated_data = filtered_data
        title = f"CO2 Emission Sources for {', '.join(selected_country)}"

    # Create the bar chart
    fig = px.bar(
        aggregated_data,
        x='emissions',
        y='source',
        color='source',
        animation_frame='year',
        animation_group='source',
        title=title,
        labels={
            "emissions": "Total Emissions (in metric tons)",
            "source": "CO2 Emission Sources",
            "year": "Year"
        },
        color_discrete_map={
            "coal_co2": "blue",
            "cement_co2": "orange",
            "flaring_co2": "yellow",
            "gas_co2": "red",
            "oil_co2": "green"
        }
    )

    # Customize layout for aesthetics and readability
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,  # Center the title
            y=0.95,
            font=dict(size=24, color="black")
        ),
        paper_bgcolor='white',
        font=dict(color="black", family="Roboto, sans-serif"),
        plot_bgcolor='white',
        xaxis=dict(
            title="Total Emissions (in metric tons)",
            tickfont=dict(color="black"),
            title_font=dict(color="black"),
            showgrid=False,
            linecolor="gray",
            linewidth=2
        ),
        yaxis=dict(
            title="CO2 Emission Sources",
            tickfont=dict(color="black"),
            title_font=dict(color="black"),
            showgrid=False,
            linecolor="gray",
            linewidth=2,
            categoryorder='total ascending'
        ),
        margin=dict(l=50, r=50, t=50, b=50),
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 10},
                "showactive": True,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": -0.37,  # Adjusted to align with the year slider
                "yanchor": "bottom",
            }
        ]
    )

    return fig
