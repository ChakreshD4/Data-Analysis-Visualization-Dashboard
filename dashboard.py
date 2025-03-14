import streamlit as st
import pandas as pd
from utils import process_csv, create_plot

# Set up the page layout and title
st.set_page_config(page_title="Healthcare Data Dashboard", layout="wide")

st.title("Healthcare Data Dashboard")

# File uploader widget
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Process the uploaded CSV file
    df, message = process_csv(uploaded_file)
    
    if df is not None:
        st.success(message)

        # Show the data in a nice format
        st.subheader("Preview of Uploaded Data:")
        st.dataframe(df.head(), use_container_width=True)

        # Filter options
        st.sidebar.subheader("Filters")

        # Select unique options for filtering
        filter_column = st.sidebar.selectbox("Choose a filter column", df.columns)
        filter_value = None

        if filter_column in df.columns:
            filter_value = st.sidebar.selectbox(f"Select {filter_column}", df[filter_column].unique())

        # Select plot type
        st.sidebar.subheader("Select Plot Type")
        plot_type = st.sidebar.selectbox("Choose a plot type", 
                                         ["Scatter Plot", "Bar Chart", "Bubble Chart", "Pie Chart"])

        # Visualize data interactively
        st.subheader(f"Interactive {plot_type} Visualization")
        x_col = st.selectbox("Select X-axis", df.columns)
        y_col = st.selectbox("Select Y-axis", df.columns)

        # Generate plot using the selected columns and filter
        if x_col and y_col:
            fig = create_plot(df, plot_type, x_col, y_col, filter_col=filter_column, filter_value=filter_value)
            st.plotly_chart(fig)

        # Displaying basic insights
        st.subheader("Basic Data Insights")
        st.write(f"Total records in dataset: {len(df)}")

        # Summary Statistics
        st.subheader("Summary Statistics")
        st.write(df.describe())

    else:
        st.error(message)

else:
    st.info("Please upload a CSV file to get started.")
