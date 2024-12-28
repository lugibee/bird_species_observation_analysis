# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(file_path):
    """
    Load the cleaned dataset and preprocess it.
    """
    data = pd.read_csv(file_path)
    
    # Ensure 'date' is in datetime format
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    
    # Extract 'month' from 'date'
    data['month'] = data['date'].dt.month
    
    return data

# Load the data
data = load_data("data\cleaned_bird_data.csv")

# Sidebar filters
st.sidebar.header("Filters")

# Habitat filter
habitat = st.sidebar.selectbox("Select Habitat", ["All", "Forest", "Grassland"])
filtered_data = data.copy()
if habitat != "All":
    filtered_data = filtered_data[filtered_data['location_type'] == habitat]

# Species filter
species = st.sidebar.multiselect("Select Species", options=data['common_name'].unique(), default=None)
if species:
    filtered_data = filtered_data[filtered_data['common_name'].isin(species)]

# Observer filter
observer = st.sidebar.multiselect("Select Observer", options=data['observer'].unique(), default=None)
if observer:
    filtered_data = filtered_data[filtered_data['observer'].isin(observer)]

# Main dashboard
st.title("Bird Species Observation Analysis")

# Key metrics
st.subheader("Key Metrics")
st.metric("Total Observations", len(filtered_data))
st.metric("Unique Species", filtered_data['scientific_name'].nunique())
st.metric("Unique Observers", filtered_data['observer'].nunique())

# Temporal analysis: Observation frequency by month
st.subheader("Observation Frequency by Month")
if 'month' in filtered_data.columns:
    monthly_data = filtered_data.groupby(['month', 'common_name']).size().reset_index(name='observation_count')
    if species:
        # Highlight selected species in the plot
        fig = px.bar(
            monthly_data,
            x='month',
            y='observation_count',
            color='common_name',
            title="Observation Frequency by Month (Differentiated by Species)",
            labels={'observation_count': 'Number of Observations', 'month': 'Month'},
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
    else:
        # General plot without species differentiation
        monthly_data = filtered_data.groupby('month').size().reset_index(name='observation_count')
        fig = px.bar(
            monthly_data,
            x='month',
            y='observation_count',
            title="Observation Frequency by Month",
            labels={'observation_count': 'Number of Observations', 'month': 'Month'},
            color_discrete_sequence=['#636EFA']
        )
    st.plotly_chart(fig)

# Spatial analysis: Biodiversity hotspots (Top 10 plots)
st.subheader("Top 10 Biodiversity Hotspots (Plots)")
if 'plot_name' in filtered_data.columns and 'scientific_name' in filtered_data.columns:
    plot_data = filtered_data.groupby(['plot_name', 'common_name'])['scientific_name'].nunique().reset_index()
    plot_data = plot_data.sort_values(by='scientific_name', ascending=False).head(10)
    if species:
        # Highlight selected species in the plot
        fig = px.bar(
            plot_data,
            x='scientific_name',
            y='plot_name',
            color='common_name',
            orientation='h',
            title="Top 10 Biodiversity Hotspots (Differentiated by Species)",
            labels={'scientific_name': 'Number of Unique Species', 'plot_name': 'Plot Name'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
    else:
        # General plot without species differentiation
        plot_data = filtered_data.groupby('plot_name')['scientific_name'].nunique().reset_index()
        plot_data = plot_data.sort_values(by='scientific_name', ascending=False).head(10)
        fig = px.bar(
            plot_data,
            x='scientific_name',
            y='plot_name',
            orientation='h',
            title="Top 10 Biodiversity Hotspots",
            labels={'scientific_name': 'Number of Unique Species', 'plot_name': 'Plot Name'},
            color_discrete_sequence=['#636EFA']
        )
    st.plotly_chart(fig)

# Distance analysis
st.subheader("Distance Analysis")
if 'distance' in filtered_data.columns:
    distance_data = filtered_data['distance'].value_counts().reset_index()
    distance_data.columns = ['distance', 'count']
    fig = px.bar(
        distance_data,
        x='distance',
        y='count',
        title="Distance Analysis",
        labels={'count': 'Number of Observations', 'distance': 'Distance'},
        color_discrete_sequence=['#AB63FA']
    )
    st.plotly_chart(fig)

# Flyover frequency
st.subheader("Flyover Frequency")
if 'flyover_observed' in filtered_data.columns:
    flyover_data = filtered_data['flyover_observed'].value_counts().reset_index()
    flyover_data.columns = ['flyover_observed', 'count']
    fig = px.pie(
        flyover_data,
        names='flyover_observed',
        values='count',
        title="Flyover Frequency",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig)

# Weather correlation: Sky and Wind
st.subheader("Weather Correlation")
if 'sky' in filtered_data.columns and 'wind' in filtered_data.columns:
    weather_data = filtered_data.groupby(['sky', 'wind']).size().reset_index(name='observation_count')
    fig = px.bar(
        weather_data,
        x='sky',
        y='observation_count',
        color='wind',
        title="Weather Correlation (Sky and Wind)",
        labels={'observation_count': 'Number of Observations', 'sky': 'Sky Condition', 'wind': 'Wind Condition'},
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig)

# Visit patterns
st.subheader("Visit Patterns")
if 'visit' in filtered_data.columns:
    visit_data = filtered_data['visit'].value_counts().reset_index()
    visit_data.columns = ['visit', 'count']
    fig = px.bar(
        visit_data,
        x='visit',
        y='count',
        title="Visit Patterns",
        labels={'count': 'Number of Observations', 'visit': 'Visit Count'},
        color_discrete_sequence=['#FFA15A']
    )
    st.plotly_chart(fig)

# AOU Code patterns
st.subheader("AOU Code Patterns")
if 'aou_code' in filtered_data.columns:
    aou_data = filtered_data['aou_code'].value_counts().reset_index()
    aou_data.columns = ['aou_code', 'count']
    fig = px.bar(
        aou_data,
        x='aou_code',
        y='count',
        title="AOU Code Patterns",
        labels={'count': 'Number of Observations', 'aou_code': 'AOU Code'},
        color_discrete_sequence=['#19D3F3']
    )
    st.plotly_chart(fig)

# Spatial analysis: Observations by Admin Unit
st.subheader("Observations by Administrative Unit")
if 'admin_unit_code' in filtered_data.columns:
    admin_data = filtered_data['admin_unit_code'].value_counts().reset_index()
    admin_data.columns = ['admin_unit_code', 'observation_count']
    fig = px.bar(
        admin_data,
        x='admin_unit_code',
        y='observation_count',
        title="Observations by Administrative Unit",
        labels={'observation_count': 'Number of Observations', 'admin_unit_code': 'Administrative Unit'},
        color_discrete_sequence=['#636EFA']
    )
    st.plotly_chart(fig)

# Spatial analysis: Observations by Plot
st.subheader("Observations by Plot")
if 'plot_name' in filtered_data.columns:
    plot_data = filtered_data['plot_name'].value_counts().reset_index()
    plot_data.columns = ['plot_name', 'observation_count']
    fig = px.bar(
        plot_data,
        x='observation_count',
        y='plot_name',
        orientation='h',
        title="Observations by Plot",
        labels={'observation_count': 'Number of Observations', 'plot_name': 'Plot Name'},
        color_discrete_sequence=['#EF553B']
    )
    st.plotly_chart(fig)
