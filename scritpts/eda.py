# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
data = pd.read_csv("data\cleaned_bird_data.csv")

# Ensure 'date' is in datetime format
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Extract additional temporal features
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data['season'] = data['month'].apply(lambda x: 'Winter' if x in [12, 1, 2] else
                                                 'Spring' if x in [3, 4, 5] else
                                                 'Summer' if x in [6, 7, 8] else
                                                 'Fall')

# Set up visualization styles
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# -------------------------------
# 1. Temporal Analysis
# -------------------------------

# Seasonal Trends
def seasonal_trends(data):
    seasonal_data = data.groupby(['season', 'year']).size().reset_index(name='observation_count')
    sns.lineplot(data=seasonal_data, x='year', y='observation_count', hue='season', marker='o')
    plt.title("Seasonal Trends in Bird Observations")
    plt.xlabel("Year")
    plt.ylabel("Number of Observations")
    plt.legend(title="Season")
    plt.show()

# Observation Time Analysis
def observation_time_analysis(data):
    data['start_hour'] = pd.to_datetime(data['start_time'], format='%H:%M:%S', errors='coerce').dt.hour
    data['end_hour'] = pd.to_datetime(data['end_time'], format='%H:%M:%S', errors='coerce').dt.hour
    sns.histplot(data['start_hour'], bins=24, kde=False, color='blue', label='Start Time')
    sns.histplot(data['end_hour'], bins=24, kde=False, color='orange', label='End Time')
    plt.title("Observation Time Analysis")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Observations")
    plt.legend()
    plt.show()

# -------------------------------
# 2. Spatial Analysis
# -------------------------------

# Location Insights
def location_insights(data):
    location_data = data.groupby('location_type')['scientific_name'].nunique().reset_index()
    sns.barplot(data=location_data, x='location_type', y='scientific_name', palette='viridis')
    plt.title("Biodiversity by Habitat Type")
    plt.xlabel("Habitat Type")
    plt.ylabel("Number of Unique Species")
    plt.show()

# Plot-Level Analysis
def plot_level_analysis(data):
    plot_data = data.groupby('plot_name')['scientific_name'].nunique().reset_index().sort_values(by='scientific_name', ascending=False).head(10)
    sns.barplot(data=plot_data, x='scientific_name', y='plot_name', palette='coolwarm')
    plt.title("Top 10 Biodiversity Hotspots (Plots)")
    plt.xlabel("Number of Unique Species")
    plt.ylabel("Plot Name")
    plt.show()

# -------------------------------
# 3. Species Analysis
# -------------------------------

# Diversity Metrics
def diversity_metrics(data):
    diversity_data = data.groupby('location_type')['scientific_name'].nunique().reset_index()
    sns.barplot(data=diversity_data, x='location_type', y='scientific_name', palette='magma')
    plt.title("Species Diversity Across Habitat Types")
    plt.xlabel("Habitat Type")
    plt.ylabel("Number of Unique Species")
    plt.show()

# Activity Patterns
def activity_patterns(data):
    activity_data = data['id_method'].value_counts().reset_index()
    activity_data.columns = ['id_method', 'count']
    sns.barplot(data=activity_data, x='count', y='id_method', palette='plasma')
    plt.title("Activity Patterns (ID Method)")
    plt.xlabel("Number of Observations")
    plt.ylabel("ID Method")
    plt.show()

# Sex Ratio
def sex_ratio(data):
    sex_data = data['sex'].value_counts().reset_index()
    sex_data.columns = ['sex', 'count']
    sns.barplot(data=sex_data, x='sex', y='count', palette='pastel')
    plt.title("Sex Ratio of Observed Birds")
    plt.xlabel("Sex")
    plt.ylabel("Number of Observations")
    plt.show()

# -------------------------------
# 4. Environmental Conditions
# -------------------------------

# Weather Correlation
def weather_correlation(data):
    sns.scatterplot(data=data, x='temperature', y='humidity', hue='sky', style='wind', palette='coolwarm')
    plt.title("Weather Correlation: Temperature vs Humidity")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    plt.legend(title="Sky Condition")
    plt.show()

# Disturbance Effect
def disturbance_effect(data):
    disturbance_data = data['disturbance'].value_counts().reset_index()
    disturbance_data.columns = ['disturbance', 'count']
    sns.barplot(data=disturbance_data, x='count', y='disturbance', palette='cubehelix')
    plt.title("Impact of Disturbance on Bird Observations")
    plt.xlabel("Number of Observations")
    plt.ylabel("Disturbance Type")
    plt.show()

# -------------------------------
# 5. Distance and Behavior
# -------------------------------

# Distance Analysis
def distance_analysis(data):
    distance_data = data['distance'].value_counts().reset_index()
    distance_data.columns = ['distance', 'count']
    sns.barplot(data=distance_data, x='count', y='distance', palette='viridis')
    plt.title("Distance Analysis")
    plt.xlabel("Number of Observations")
    plt.ylabel("Distance")
    plt.show()

# Flyover Frequency
def flyover_frequency(data):
    flyover_data = data['flyover_observed'].value_counts().reset_index()
    flyover_data.columns = ['flyover_observed', 'count']
    sns.barplot(data=flyover_data, x='flyover_observed', y='count', palette='coolwarm')
    plt.title("Flyover Frequency")
    plt.xlabel("Flyover Observed")
    plt.ylabel("Number of Observations")
    plt.show()

# -------------------------------
# 6. Observer Trends
# -------------------------------

# Observer Bias
def observer_bias(data):
    observer_data = data['observer'].value_counts().reset_index().head(10)
    observer_data.columns = ['observer', 'count']
    sns.barplot(data=observer_data, x='count', y='observer', palette='mako')
    plt.title("Top 10 Observers by Number of Observations")
    plt.xlabel("Number of Observations")
    plt.ylabel("Observer")
    plt.show()

# Visit Patterns
def visit_patterns(data):
    visit_data = data['visit'].value_counts().reset_index()
    visit_data.columns = ['visit', 'count']
    sns.barplot(data=visit_data, x='visit', y='count', palette='rocket')
    plt.title("Visit Patterns")
    plt.xlabel("Visit Count")
    plt.ylabel("Number of Observations")
    plt.show()

# -------------------------------
# 7. Conservation Insights
# -------------------------------

# Watchlist Trends
def watchlist_trends(data):
    watchlist_data = data['pif_watchlist_status'].value_counts().reset_index()
    watchlist_data.columns = ['pif_watchlist_status', 'count']
    sns.barplot(data=watchlist_data, x='pif_watchlist_status', y='count', palette='pastel')
    plt.title("PIF Watchlist Status Distribution")
    plt.xlabel("PIF Watchlist Status")
    plt.ylabel("Number of Observations")
    plt.show()

# AOU Code Patterns
def aou_code_patterns(data):
    aou_data = data['aou_code'].value_counts().reset_index().head(10)
    aou_data.columns = ['aou_code', 'count']
    sns.barplot(data=aou_data, x='count', y='aou_code', palette='coolwarm')
    plt.title("Top 10 AOU Codes")
    plt.xlabel("Number of Observations")
    plt.ylabel("AOU Code")
    plt.show()

# -------------------------------
# Run EDA Functions
# -------------------------------

# Temporal Analysis
seasonal_trends(data)
observation_time_analysis(data)

# Spatial Analysis
location_insights(data)
plot_level_analysis(data)

# Species Analysis
diversity_metrics(data)
activity_patterns(data)
sex_ratio(data)

# Environmental Conditions
weather_correlation(data)
disturbance_effect(data)

# Distance and Behavior
distance_analysis(data)
flyover_frequency(data)

# Observer Trends
observer_bias(data)
visit_patterns(data)

# Conservation Insights
watchlist_trends(data)
aou_code_patterns(data)
