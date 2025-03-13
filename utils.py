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
        required_columns = ["Type", "Provider Identifier", "ProviderType", "ServiceArea", "Specialty",
                            "UserType", "ReportingPeriodStartDate", "ReportingPeriodEndDate", "Metric",
                            "Numerator", "Denominator", "Value"]
        return all(col in self.data.columns for col in required_columns)

    def filter_data(self, provider_type_filter, specialty_filter):
        filtered_data = self.data.copy()
        if provider_type_filter:
            filtered_data = filtered_data[filtered_data['ProviderType'].isin(provider_type_filter)]
        if specialty_filter:
            filtered_data = filtered_data[filtered_data['Specialty'].isin(specialty_filter)]
        return filtered_data

class Visualizer:
    def __init__(self, data):
        self.data = data

    def plot_time_in_vs_orders(self):
        in_basket_data = self.data[self.data['Metric'] == "Time in In Basket per Day"]
        orders_data = self.data[self.data['Metric'] == "Time in Orders per Day"]
        if not in_basket_data.empty and not orders_data.empty:
            fig, ax = plt.subplots()
            ax.scatter(in_basket_data['Value'], orders_data['Value'])
            ax.set_xlabel("Time in In Basket per Day")
            ax.set_ylabel("Time in Orders per Day")
            st.pyplot(fig)
        else:
            st.write("No data to display for Time in In Basket vs Orders.")

    def plot_appointment_efficiency(self):
        efficiency_metrics = ["Appointments per Day", "Percent of Appointments Closed Same Day"]
        efficiency_data = self.data[self.data['Metric'].isin(efficiency_metrics)]
        if not efficiency_data.empty:
            fig, ax = plt.subplots()
            sns.barplot(x='Metric', y='Value', data=efficiency_data, ax=ax)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.write("No data to display for appointment efficiency.")

    def plot_time_metrics_line(self):
        time_metrics = self.data[self.data['Metric'].str.contains("Time in")]
        if not time_metrics.empty:
            fig, ax = plt.subplots()
            ax.plot(time_metrics['Metric'], time_metrics['Value'])
            plt.xticks(rotation=45, ha='right')
            ax.set_ylabel("Value")
            st.pyplot(fig)
        else:
            st.write("No data to display for Time metrics.")

    def plot_documentation_histogram(self):
        doc_data = self.data[self.data['Metric'] == "Documentation Length"]
        if not doc_data.empty:
            fig, ax = plt.subplots()
            ax.hist(doc_data['Value'], bins=10)
            ax.set_xlabel("Documentation Length Value")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
        else:
            st.write("No data to display for Documentation Length histogram.")