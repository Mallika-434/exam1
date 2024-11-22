import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Title and App Info
st.title("Interactive EDA App - Automobile Dataset")
st.write("This app allows you to explore and visualize the Automobile dataset interactively.")

# Load Dataset
st.header("1. Load Dataset")
path = 'https://raw.githubusercontent.com/klamsal/Fall2024Exam/refs/heads/main/CleanedAutomobile.csv'

@st.cache_data
def load_data():
    df = pd.read_csv(path)
    # Convert numeric columns to float, handling non-numeric values
    numeric_columns = ['normalized-losses', 'wheel-base', 'length', 'width', 'height', 
                      'curb-weight', 'engine-size', 'bore', 'stroke', 'compression-ratio', 
                      'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'price']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

# Dataset Overview
if st.checkbox("Show Dataset Overview"):
    st.subheader("Preview of Dataset")
    st.dataframe(df.head())
    
    st.subheader("Basic Information")
    st.write(f"Number of Rows: {df.shape[0]}")
    st.write(f"Number of Columns: {df.shape[1]}")
    st.write("Column Data Types:")
    st.write(df.dtypes)

# Filtering Dataset
st.header("2. Filter Dataset")
columns = df.columns.tolist()
selected_columns = st.multiselect("Select Columns to View", columns, default=columns[:5])
filtered_df = df[selected_columns]
st.write("Filtered Data Preview:")
st.dataframe(filtered_df)

# Interactive Visualizations
st.header("3. Interactive Visualizations")
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if numeric_columns:
    st.subheader("Scatterplot Generator")
    x_feature = st.selectbox("Select X-axis Feature", numeric_columns)
    y_feature = st.selectbox("Select Y-axis Feature", numeric_columns)

    if st.button("Generate Scatterplot"):
        fig, ax = plt.subplots()
        sns.regplot(data=df, x=x_feature, y=y_feature, ax=ax)
        plt.title(f"{x_feature} vs {y_feature}")
        st.pyplot(fig)
        plt.close()

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    if st.checkbox("Show Correlation Heatmap"):
        selected_corr_columns = st.multiselect(
            "Select Columns for Correlation Heatmap",
            numeric_columns,
            default=numeric_columns[:5]
        )
        
        if selected_corr_columns:
            corr_matrix = df[selected_corr_columns].corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
            plt.title("Correlation Heatmap")
            st.pyplot(fig)
            plt.close()

# Grouping and Aggregation
st.header("4. Grouping and Aggregation")
categorical_columns = df.select_dtypes(include=['object']).columns
if len(categorical_columns) > 0:
    group_column = st.selectbox("Select Categorical Column for Grouping", categorical_columns)
    agg_column = st.selectbox("Select Numeric Column for Aggregation", numeric_columns)

    if st.button("Show Grouped Data"):
        grouped_data = df.groupby(group_column)[agg_column].mean().reset_index()
        st.write(grouped_data)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=grouped_data, x=group_column, y=agg_column, ax=ax)
        plt.xticks(rotation=45)
        plt.title(f"Average {agg_column} by {group_column}")
        st.pyplot(fig)
        plt.close()

# Statistical Analysis
st.header("5. Statistical Analysis")
if 'price' in numeric_columns:
    analysis_feature = st.selectbox("Select a Feature for Correlation with Price", 
                                  [col for col in numeric_columns if col != 'price'])

    if st.button("Calculate Pearson Correlation"):
        valid_data = df[[analysis_feature, 'price']].dropna()
        if len(valid_data) > 0:
            pearson_coef, p_value = stats.pearsonr(valid_data[analysis_feature], 
                                                 valid_data['price'])
            st.write(f"**Selected Feature:** {analysis_feature}")
            st.write(f"**Pearson Correlation Coefficient:** {pearson_coef:.3f}")
            st.write(f"**P-value:** {p_value:.3e}")
            if p_value < 0.05:
                st.success("The correlation is statistically significant.")
            else:
                st.warning("The correlation is not statistically significant.")
        else:
            st.error("Not enough valid data points for correlation analysis.")

# Footer
st.write("---")
st.write("This app was created to explore the Automobile dataset interactively.")
