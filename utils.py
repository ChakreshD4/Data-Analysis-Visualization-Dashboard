import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.file_path)
            return self.data
        except FileNotFoundError:
            st.error("File not found.")
            return None
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None

    def is_valid(self):
        if self.data is None:
            return False
        required_columns = ['Provider ID', 'ProviderType', 'Specialty', 'ReportingMetric', 'Value']
        return all(col in self.data.columns for col in required_columns)

    def filter_data(self, provider_type_filter, specialty_filter):
        filtered_data = self.data.copy()
        if provider_type_filter:
            filtered_data = filtered_data[filtered_data['ProviderType'].isin(provider_type_filter)]
        if specialty_filter:
            filtered_data = filtered_data[filtered_data['Specialty'].isin(specialty_filter)]
        return filtered_data

    def get_unique_metrics(self):
        if self.data is not None:
            return self.data['ReportingMetric'].unique()
        return []

class Visualizer:
    def __init__(self, data):
        self.data = data

    def plot_selected_rows(self, selected_rows, metric_to_visualize):
        if not selected_rows:
            st.warning("Please select rows to compare.")
            return

        comparison_data = self.data[self.data.index.isin(selected_rows)]

        if comparison_data.empty:
            st.warning("No data found for the selected rows.")
            return

        if metric_to_visualize not in comparison_data['ReportingMetric'].values:
            st.warning(f"'{metric_to_visualize}' not found in the selected rows.")
            return

        comparison_data = comparison_data[comparison_data['ReportingMetric'] == metric_to_visualize]

        if comparison_data.empty:
            st.warning(f"No data found for '{metric_to_visualize}' in the selected rows.")
            return

        fig, ax = plt.subplots()
        ax.bar(comparison_data.index, comparison_data['Value'])
        ax.set_xlabel("Row Index")
        ax.set_ylabel("Value")
        ax.set_title(f"Comparison of '{metric_to_visualize}'")
        st.pyplot(fig)