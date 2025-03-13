import streamlit as st
import pandas as pd
from utils import DataProcessor, Visualizer
from pathlib import Path

st.set_page_config(page_title="Healthcare Provider Dashboard", layout="wide")

st.title("Healthcare Provider Performance Dashboard")

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

        visualizer = Visualizer(data)

        st.subheader("Time in In Basket vs Orders (Scatter Plot)")
        visualizer.plot_time_in_vs_orders()

        st.subheader("Appointment Efficiency (Bar Chart)")
        visualizer.plot_appointment_efficiency()

        st.subheader("Time Metrics (Line Chart)")
        visualizer.plot_time_metrics_line()

        st.subheader("Documentation Length Distribution (Histogram)")
        visualizer.plot_documentation_histogram()

    else:
        st.error("Dataset is invalid. Please check the column names and data integrity.")
else:
    st.warning("Please upload a CSV file to proceed.")