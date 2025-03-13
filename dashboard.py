import streamlit as st
import pandas as pd
from utils import DataProcessor, Visualizer
from pathlib import Path

st.set_page_config(page_title="Healthcare Provider Burnout Dashboard", layout="wide")

st.title("AI-Based Medical Provider Burnout Prevention Dashboard")
st.markdown("""
This interactive dashboard presents key insights into healthcare provider burnout. 
Explore trends and compare selected rows!
""")

DATA_DIRECTORY = Path("data/")
DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    file_path = DATA_DIRECTORY / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    data_processor = DataProcessor(file_path)
    data = data_processor.load_data()

    if data_processor.is_valid():
        st.success("Dataset loaded and validated successfully!")
        st.write("### Dataset Preview", data.head())
        st.write("### Data Summary", data.describe())

        st.sidebar.title("Filter Options")
        provider_type_filter = st.sidebar.multiselect('Select Provider Type:', data['ProviderType'].unique())
        specialty_filter = st.sidebar.multiselect('Select Specialty:', data['Specialty'].unique())

        filtered_data = data_processor.filter_data(provider_type_filter, specialty_filter)

        st.subheader("Select Rows for Comparison")
        selected_rows = st.multiselect("Select rows by index:", filtered_data.index)

        metric_to_visualize = st.selectbox("Select metric to visualize:", data_processor.get_unique_metrics())

        visualizer = Visualizer(filtered_data)
        visualizer.plot_selected_rows(selected_rows, metric_to_visualize)

    else:
        st.error("Dataset is invalid. Please check the column names and data integrity.")
else:
    st.warning("Please upload a CSV file to proceed.")