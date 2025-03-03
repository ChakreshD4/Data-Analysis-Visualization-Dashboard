import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    load_and_validate_data,
    create_workload_stress_plot,
    create_burnout_distribution,
    create_absenteeism_plot,
    predict_burnout,
    calculate_key_metrics
)

# Page configuration
st.set_page_config(
    page_title="Medical Provider Burnout Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header
st.title("🏥 Medical Provider Burnout Prevention Dashboard")
st.markdown("""
This dashboard provides insights into medical provider burnout patterns and predictions 
using AI-powered analysis.
""")

# File upload
st.sidebar.header("Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload your burnout data CSV",
    type=['csv'],
    help="Upload a CSV file containing provider burnout data"
)

if uploaded_file is not None:
    # Load and validate data
    data, error = load_and_validate_data(uploaded_file)
    
    if error:
        st.error(error)
    else:
        # Calculate and display key metrics
        metrics = calculate_key_metrics(data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Burnout Risk", f"{metrics['avg_burnout']:.1f}%")
        with col2:
            st.metric("High Risk Providers", metrics['high_risk_count'])
        with col3:
            st.metric("Avg Satisfaction Score", f"{metrics['avg_satisfaction']:.1f}/10")
        with col4:
            st.metric("Total Providers", metrics['total_providers'])
        
        # Tabs for different visualizations
        tab1, tab2, tab3 = st.tabs([
            "Workload Analysis",
            "Burnout Distribution",
            "Absenteeism Impact"
        ])
        
        with tab1:
            st.plotly_chart(
                create_workload_stress_plot(data),
                use_container_width=True
            )
            
        with tab2:
            st.plotly_chart(
                create_burnout_distribution(data),
                use_container_width=True
            )
            
        with tab3:
            st.plotly_chart(
                create_absenteeism_plot(data),
                use_container_width=True
            )
        
        # AI Predictions
        st.header("AI-Powered Burnout Predictions")
        
        predictions, coefficients = predict_burnout(data)
        
        st.markdown("""
        The AI model analyzes workload hours and stress levels to predict burnout risk.
        Key factors influencing burnout:
        """)
        
        st.markdown(f"""
        - Impact of workload: {coefficients[0]:.2f}% per additional hour
        - Impact of stress: {coefficients[1]:.2f}% per stress level point
        """)
        
        # Filters
        st.sidebar.header("Filters")
        
        min_workload = st.sidebar.slider(
            "Minimum Workload Hours",
            min_value=int(data['workload_hours'].min()),
            max_value=int(data['workload_hours'].max()),
            value=int(data['workload_hours'].min())
        )
        
        filtered_data = data[data['workload_hours'] >= min_workload]
        
        # Show filtered results
        st.subheader("Filtered Results")
        st.dataframe(
            filtered_data[['provider_id', 'workload_hours', 'stress_level', 'burnout_risk']],
            height=200
        )

else:
    # Show placeholder content
    st.info("Please upload a CSV file to begin the analysis.")
    st.markdown("""
    ### Expected CSV Format:
    The CSV should contain the following columns:
    - `provider_id`: Unique ID for each healthcare provider
    - `workload_hours`: Number of hours worked per week
    - `stress_level`: Stress level score (1-10)
    - `absenteeism_days`: Number of days absent per month
    - `satisfaction_score`: Job satisfaction score (1-10)
    - `burnout_risk`: Current burnout risk (0-100%)
    """)
