import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page title and layout
# Using "wide" layout gives our charts more space
st.set_page_config(layout="wide", page_title="Solar Data Analysis Dashboard")


# --- Data Loading ---
# We cache the data so it only loads once
@st.cache_data
def load_data():
    # Load the three cleaned datasets
    # We add error handling in case a file is missing
    try:
        df_benin = pd.read_csv('dashboard_data/benin_clean.csv',
                               parse_dates=['Timestamp'],
                               index_col='Timestamp')

        df_sl = pd.read_csv('dashboard_data/sierraleone_clean.csv',
                            parse_dates=['Timestamp'],
                            index_col='Timestamp')

        df_togo = pd.read_csv('dashboard_data/togo_clean.csv',
                              parse_dates=['Timestamp'],
                              index_col='Timestamp')
    except FileNotFoundError as e:
        st.error(f"Error: {e}. Make sure the cleaned data files (e.g., 'benin_clean.csv') are in the 'data/' folder.")
        return pd.DataFrame()  # Return empty dataframe on error

    # Add a 'Country' column to each
    df_benin['Country'] = 'Benin'
    df_sl['Country'] = 'Sierra Leone'
    df_togo['Country'] = 'Togo'

    # Concatenate them into a single DataFrame
    df_all = pd.concat([df_benin, df_sl, df_togo])

    # Reset index so 'Timestamp' is a column, which is easier for Plotly
    df_all = df_all.reset_index()
    return df_all


# Load the data
df_all = load_data()

# Stop the app if data loading failed
if df_all.empty:
    st.stop()

# --- App Layout ---
st.title('☀️ Solar Farm Analysis Dashboard')
st.markdown("An interactive dashboard to analyze solar potential in Benin, Sierra Leone, and Togo.")

# --- Sidebar for User Inputs ---
st.sidebar.header("Dashboard Controls")

# Create a multiselect widget
countries_to_show = st.sidebar.multiselect(
    'Select Countries',
    options=df_all['Country'].unique(),
    # default=df_all['Country'].unique()  # Show all by default
    default=['Benin']
)

# Filter the main dataframe based on user selection
df_filtered = df_all[df_all['Country'].isin(countries_to_show)]

# Stop if no country is selected
if df_filtered.empty:
    st.warning("Please select at least one country in the sidebar.")
    st.stop()

# --- Main Page Content ---


# 1. Key Metrics & Summary Table
st.header("Cross-Country Comparison")
st.markdown(f"Displaying analysis for: **{', '.join(countries_to_show)}**")

# Calculate summary stats from Task 3
summary_table = df_filtered.groupby('Country')[['GHI', 'DNI', 'DHI']].agg(['mean', 'median', 'std'])

# --- FIX: Flatten MultiIndex columns to remove warnings ---
# Create new, unique column names like "GHI - mean", "DNI - median"
summary_table.columns = [f"{col[0]} - {col[1]}" for col in summary_table.columns]
# --- End of fix ---

st.subheader("Summary Statistics (Mean, Median, Std Dev)")
# We apply a number format to 2 decimal places
st.dataframe(summary_table.style.format("{:.2f}"))


# 2. Boxplots (from Task 3)
st.subheader("Solar Irradiance Comparison (GHI, DNI, DHI)")
st.markdown("This plot shows the distribution of solar irradiance. Higher values are better.")

# We'll create 3 columns to show plots side-by-side
col1, col2, col3 = st.columns(3)

with col1:
    fig_ghi = px.box(df_filtered, x='Country', y='GHI', title='GHI Comparison')
    st.plotly_chart(fig_ghi, use_container_width=True)

with col2:
    fig_dni = px.box(df_filtered, x='Country', y='DNI', title='DNI Comparison')
    st.plotly_chart(fig_dni, use_container_width=True)

with col3:
    fig_dhi = px.box(df_filtered, x='Country', y='DHI', title='DHI Comparison')
    st.plotly_chart(fig_dhi, use_container_width=True)

# 3. Time Series Plot (from Task 2)
st.subheader("Seasonal Solar Potential (Daily Average GHI)")
st.markdown("This plot shows how solar irradiance changes over the year. Note the seasonal dip around August.")

# Resample data to daily mean for a cleaner plot
# We group by Country *and* Timestamp
df_daily = df_filtered.set_index('Timestamp').groupby('Country').resample('D').mean(numeric_only=True).reset_index()

fig_ts = px.line(
    df_daily,
    x='Timestamp',
    y='GHI',
    color='Country',  # One line per country
    title='Daily Average GHI Over Time'
)
st.plotly_chart(fig_ts, use_container_width=True)

# --- 4. Deeper Analysis Tabs ---
st.header("Deeper Analysis")
st.markdown("Explore other key environmental factors from our analysis.")

tab1, tab2, tab3 = st.tabs(["Correlations", "Cleaning Impact", "Wind Analysis"])

with tab1:
    st.subheader("Correlation: Sun vs. Temp vs. Humidity")
    st.markdown("This plot shows that high GHI (sun) days are also high temperature but *low humidity* days.")

    # We'll use a smaller sample for the scatter plot to keep it fast
    df_sample = df_filtered.sample(min(len(df_filtered), 5000))

    fig_bubble = px.scatter(
        df_sample,
        x="GHI",
        y="Tamb",
        size="RH",
        color="RH",
        title="GHI vs. Ambient Temp (Bubble size = RH)",
        size_max=15
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

with tab2:
    st.subheader("Impact of Soiling & Cleaning")
    st.markdown(
        "This plot shows the average sensor reading based on whether a cleaning event was logged. This proves that regular cleaning is critical for efficiency.")

    # Calculate cleaning impact
    cleaning_impact = df_filtered.groupby(['Country', 'Cleaning'])[['ModA', 'ModB']].mean().reset_index()

    fig_clean = px.bar(
        cleaning_impact,
        x='Country',
        y=['ModA', 'ModB'],
        color='Cleaning',
        barmode='group',
        title='Average Sensor Reading vs. Cleaning Status'
    )
    st.plotly_chart(fig_clean, use_container_width=True)

with tab3:
    st.subheader("Wind Pattern Analysis (Wind Rose)")
    st.markdown(
        "This shows the prevailing wind direction and speed. Note that Benin and Sierra Leone have one main wind direction (SW), while Togo has two (SW and ENE).")

    # Create columns for each selected country's wind rose
    wind_cols = st.columns(len(countries_to_show))

    for i, country in enumerate(countries_to_show):
        with wind_cols[i]:
            st.markdown(f"**{country} Wind Rose**")

            # Filter for the specific country
            df_country = df_filtered[df_filtered['Country'] == country].copy()

            # Bin Wind Direction
            df_country['WD_binned'] = pd.cut(
                df_country['WD'], bins=16,
                labels=['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                        'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
            )
            # Bin Wind Speed
            df_country['WS_binned'] = pd.cut(
                df_country['WS'], bins=[0, 2, 4, 6, 8, 10, 100],
                labels=['0-2', '2-4', '4-6', '6-8', '8-10', '>10']
            )

            # Create the Wind Rose data
            wind_rose_data = df_country.groupby(['WD_binned', 'WS_binned']).size().reset_index(name='count')

            fig_rose = px.bar_polar(
                wind_rose_data,
                r="count",
                theta="WD_binned",
                color="WS_binned",
                title=f"Wind Rose for {country}",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Plasma_r
            )
            st.plotly_chart(fig_rose, use_container_width=True)