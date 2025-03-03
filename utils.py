import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go

def load_and_validate_data(file):
    """Load and validate uploaded CSV data"""
    try:
        df = pd.read_csv(file)
        required_columns = [
            'provider_id', 'workload_hours', 'stress_level',
            'absenteeism_days', 'satisfaction_score', 'burnout_risk'
        ]
        
        if not all(col in df.columns for col in required_columns):
            return None, "Missing required columns in the dataset"
        
        return df, None
    except Exception as e:
        return None, f"Error loading data: {str(e)}"

def create_workload_stress_plot(data):
    """Create workload vs stress level scatter plot"""
    fig = px.scatter(
        data,
        x='workload_hours',
        y='stress_level',
        color='burnout_risk',
        color_continuous_scale='RdYlBu_r',
        title='Workload vs Stress Level',
        hover_data=['provider_id']
    )
    fig.update_layout(
        height=500,
        template='plotly_white'
    )
    return fig

def create_burnout_distribution(data):
    """Create burnout risk distribution plot"""
    fig = px.histogram(
        data,
        x='burnout_risk',
        nbins=20,
        title='Burnout Risk Distribution',
        color_discrete_sequence=['#0466C8']
    )
    fig.update_layout(
        height=400,
        template='plotly_white'
    )
    return fig

def create_absenteeism_plot(data):
    """Create absenteeism vs burnout risk scatter plot"""
    fig = px.scatter(
        data,
        x='absenteeism_days',
        y='burnout_risk',
        color='satisfaction_score',
        size='workload_hours',
        title='Absenteeism vs Burnout Risk',
        hover_data=['provider_id']
    )
    fig.update_layout(
        height=500,
        template='plotly_white'
    )
    return fig

def predict_burnout(data):
    """Predict burnout risk using linear regression"""
    X = data[['workload_hours', 'stress_level']]
    y = data['burnout_risk']
    
    model = LinearRegression()
    model.fit(X, y)
    
    predictions = model.predict(X)
    return predictions, model.coef_

def calculate_key_metrics(data):
    """Calculate key dashboard metrics"""
    metrics = {
        'avg_burnout': data['burnout_risk'].mean(),
        'high_risk_count': len(data[data['burnout_risk'] > 75]),
        'avg_satisfaction': data['satisfaction_score'].mean(),
        'total_providers': len(data['provider_id'].unique())
    }
    return metrics
