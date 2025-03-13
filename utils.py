# utils.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """
        Load the dataset and perform initial data preprocessing.
        """
        try:
            self.data = pd.read_csv(self.file_path)
            logging.info("Data loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise ValueError(f"Error loading data: {e}")
        return self.data

    def is_valid(self):
        """
        Validate if the dataset contains the required columns.
        """
        required_columns = [
            "Type", "Provider Identifier", "ProviderType", "ServiceArea", "Specialty",
            "UserType", "ReportingPeriodStartDate", "ReportingPeriodEndDate", "Metric",
            "Numerator", "Denominator", "Value"
        ]
        if all(col in self.data.columns for col in required_columns):
            logging.info("Dataset is valid.")
            return True
        else:
            logging.error("Dataset is missing required columns.")
            return False

    def filter_data(self, provider_type_filter, specialty_filter):
        """
        Filter the dataset based on user selections.
        """
        filtered_data = self.data.copy()
        if provider_type_filter:
            filtered_data = filtered_data[filtered_data['ProviderType'].isin(provider_type_filter)]
        if specialty_filter:
            filtered_data = filtered_data[filtered_data['Specialty'].isin(specialty_filter)]
        logging.info(f"Data filtered: {len(filtered_data)} records")
        return filtered_data

class Visualizer:
    def __init__(self, data):
        self.data = data

    def plot_work_hours_by_role(self):
        """
        Plot work hours by provider type.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x="ProviderType", y="Value", hue="Metric", data=self.data[self.data['Metric'] == 'Work Hours'])
        plt.title("Work Hours by Role")
        plt.xlabel("Provider Type")
        plt.ylabel("Work Hours")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

    def plot_stress_level_by_department(self):
        """
        Plot stress level by service area.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x="ServiceArea", y="Value", hue="Metric", data=self.data[self.data['Metric'] == 'Stress Level'])
        plt.title("Stress Level by Department")
        plt.xlabel("Service Area")
        plt.ylabel("Stress Level")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

    def plot_burnout_by_gender(self):
        """
        Plot burnout by gender.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x="UserType", y="Value", hue="Metric", data=self.data[self.data['Metric'] == 'Burnout'])
        plt.title("Burnout by Gender")
        plt.xlabel("Gender")
        plt.ylabel("Burnout Level")
        plt.tight_layout()
        st.pyplot(plt)

    def plot_sleep_stress_correlation(self):
        """
        Plot correlation between sleep and stress.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="Numerator", y="Denominator", data=self.data[(self.data['Metric'] == 'Sleep') | (self.data['Metric'] == 'Stress Level')])
        plt.title("Sleep vs Stress Correlation")
        plt.xlabel("Sleep (Numerator)")
        plt.ylabel("Stress Level (Denominator)")
        plt.tight_layout()
        st.pyplot(plt)

    def plot_work_hours_burnout(self):
        """
        Plot work hours vs burnout.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="Numerator", y="Denominator", data=self.data[(self.data['Metric'] == 'Work Hours') | (self.data['Metric'] == 'Burnout')])
        plt.title("Work Hours vs Burnout")
        plt.xlabel("Work Hours (Numerator)")
        plt.ylabel("Burnout Level (Denominator)")
        plt.tight_layout()
        st.pyplot(plt)

    def plot_age_distribution(self):
        """
        Plot age distribution of providers.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data['Value'], bins=20, kde=True)
        plt.title("Age Distribution of Providers")
        plt.xlabel("Age")
        plt.ylabel("Frequency")
        plt.tight_layout()
        st.pyplot(plt)
