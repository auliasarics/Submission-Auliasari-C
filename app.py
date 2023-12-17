import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
combined_df = pd.read_csv('data_air_quality.csv')

# Tittle
st.title('Dashboard Air Quality')

# Parameter Ranges
parameter_ranges = {
    'PM2.5': [12, 35.4, 150.4, float('inf')],
    'PM10': [54, 154, 254, float('inf')],
    'SO2': [35, 75, 185, float('inf')],
    'NO2': [53, 100, 360, float('inf')],
    'CO': [4400, 9400, 12400, float('inf')],
    'O3': [54, 70, 85, float('inf')],
}

# Line plots for parameter trends
st.header('Parameter Trends Over Time')

# Sidebar for selecting a specific parameter
selected_param = st.sidebar.selectbox("Select Parameter", list(parameter_ranges.keys()))

# Line plot based on selected parameter
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=combined_df, x='year', y=selected_param, hue='station', ax=ax)
ax.set_title(f'Trend of {selected_param} across Stations')
ax.set_xlabel('Year')
ax.set_ylabel(selected_param)
st.pyplot(fig)

# Heatmap of correlation between weather and air quality parameters
st.header('Heatmap of Correlation between Weather and Air Quality Parameters')

# Select weather and air quality columns
weather_columns = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
air_quality_columns = list(parameter_ranges.keys())

# Create correlation matrix
correlation_matrix = combined_df[weather_columns + air_quality_columns].corr()

# Plot heatmap
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5, ax=ax)
plt.title('Heatmap of Correlation between Parameters')

# Display the plot in Streamlit
st.pyplot(fig)

st.set_option('deprecation.showPyplotGlobalUse', False)

# Comparison Bar Chart
start_year = st.sidebar.slider("Select Start Year", min_value=combined_df['year'].min(), max_value=combined_df['year'].max(), value=2015)
end_year = st.sidebar.slider("Select End Year", min_value=combined_df['year'].min(), max_value=combined_df['year'].max(), value=2017)

st.header(f'Comparison of Air Quality across Stations ({start_year}-{end_year})')

# Air quality parameters
air_quality_parameters = list(parameter_ranges.keys())

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
fig.suptitle(f'Comparison of Air Quality Parameters ({start_year}-{end_year})', fontsize=16)

for i, parameter in enumerate(air_quality_parameters):
    row = i // 3
    col = i % 3

    axs[row, col].set_title(parameter)
    
    for station in combined_df['station'].unique():
        filtered_data = combined_df[(combined_df['year'] >= start_year) & (combined_df['year'] <= end_year) & (combined_df['station'] == station)]
        axs[row, col].bar(station, filtered_data[parameter].mean(), label=station)

    axs[row, col].set_xlabel('Station')
    axs[row, col].set_ylabel('Mean Air Quality')
    axs[row, col].legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(fig)



