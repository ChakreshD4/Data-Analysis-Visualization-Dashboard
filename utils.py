import pandas as pd
import plotly.express as px

# Function to read and process the CSV file
def process_csv(file):
    try:
        # Read CSV file into a DataFrame
        df = pd.read_csv(file)

        # Check for required columns
        required_columns = ["Type", "Provider Identifier", "ProviderType", "ServiceArea", 
                            "Specialty", "UserType", "ReportingPeriodStartDate", 
                            "ReportingPeriodEndDate", "Metric", "Numerator", "Denominator", "Value"]

        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return None, f"Missing columns: {', '.join(missing_columns)}"

        # Returning the dataframe and a success message
        return df, "CSV successfully processed"
    
    except Exception as e:
        return None, f"Error processing CSV: {str(e)}"

# Function to create different types of plots
def create_plot(df, plot_type, x_col, y_col, filter_col=None, filter_value=None):
    # If a filter is applied, filter the DataFrame
    if filter_col and filter_value:
        df = df[df[filter_col] == filter_value]
    
    if plot_type == 'Scatter Plot':
        # Scatter plot (circle chart)
        fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot of {y_col} vs {x_col}")
    
    elif plot_type == 'Bar Chart':
        # Bar chart
        fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart of {y_col} vs {x_col}")
    
    elif plot_type == 'Bubble Chart':
        # Bubble chart (using a third column for size)
        fig = px.scatter(df, x=x_col, y=y_col, size="Value", color="ProviderType", 
                         title=f"Bubble Chart of {y_col} vs {x_col} (Size by Value)")
    
    elif plot_type == 'Pie Chart':
        # Pie chart (can use a column for categories and sum values)
        fig = px.pie(df, names=x_col, values=y_col, title=f"Pie Chart of {y_col} by {x_col}")
    
    return fig
