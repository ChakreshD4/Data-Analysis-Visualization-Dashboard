
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from utils import DataProcessor, Visualizer
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set Streamlit page config
st.set_page_config(page_title="Healthcare Provider Burnout Dashboard", layout="wide")

# Title and description
st.title("AI-Based Medical Provider Burnout Prevention Dashboard")
st.markdown("""
This interactive dashboard presents key insights into healthcare provider burnout.  
Explore trends in stress levels, work hours, and more!
""")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

# Ensure the necessary files and directories are present
DATA_DIRECTORY = Path("data/")
DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

# Check if a file is uploaded and handle it
if uploaded_file is not None:
    try:
        # Save the uploaded file locally
        file_path = DATA_DIRECTORY / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load the dataset
        data_processor = DataProcessor(file_path)
        data = data_processor.load_data()

        # Display basic information about the dataset
        st.write("### Dataset Preview", data.head())
        st.write("### Data Summary", data.describe())

        # If the dataset passes validation, proceed
        if data_processor.is_valid():
            st.success("Dataset loaded and validated successfully!")

            # Sidebar filters for data exploration
            st.sidebar.title("Filter Options")
            provider_type_filter = st.sidebar.multiselect('Select Provider Type:', data['ProviderType'].unique())
            specialty_filter = st.sidebar.multiselect('Select Specialty:', data['Specialty'].unique())

            filtered_data = data_processor.filter_data(provider_type_filter, specialty_filter)

            # Display visualizations using the Visualizer class
            visualizer = Visualizer(filtered_data)
            
            st.subheader("Work Hours by Role")
            visualizer.plot_work_hours_by_role()

            st.subheader("Stress Level by Department")
            visualizer.plot_stress_level_by_department()

            st.subheader("Burnout by Gender")
            visualizer.plot_burnout_by_gender()

            st.subheader("Sleep vs Stress Correlation")
            visualizer.plot_sleep_stress_correlation()

            st.subheader("Work Hours vs Burnout")
            visualizer.plot_work_hours_burnout()

            st.subheader("Age Distribution")
            visualizer.plot_age_distribution()

        else:
            st.error("Dataset is invalid. Please check the column names and data integrity.")

    except Exception as e:
        logging.error(f"Error occurred while processing the file: {e}")
        st.error("An error occurred while processing the file. Please try again.")
else:
    st.warning("Please upload a CSV file to proceed.")