import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Title and Introduction
st.title("Interactive Data Analysis App")
st.markdown("""
Welcome to the **Interactive Data Analysis App**! 
This tool allows you to upload your dataset, explore it, and generate insightful visualizations and analyses.
""")

# File Upload Section
uploaded_file = st.file_uploader("Upload your data file (CSV format)", type=["csv"])
if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.write(df.head())

    # Basic Dataset Information
    st.subheader("Dataset Information")
    st.write("**Shape of the dataset:**", df.shape)
    st.write("**Data types:**")
    st.write(df.dtypes)

    # Show basic statistics
    st.subheader("Basic Statistics")
    st.write(df.describe())

    # Allow user to select columns for further analysis
    st.subheader("Select Columns for Analysis")
    columns = df.columns.tolist()
    selected_columns = st.multiselect("Select the columns you want to analyze:", columns)

    if selected_columns:
        st.write(f"You selected: {', '.join(selected_columns)}")
        selected_data = df[selected_columns]

        # Correlation Heatmap
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(selected_data.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # Univariate Analysis
        st.subheader("Univariate Analysis")
        col_to_analyze = st.selectbox("Select a column for distribution plot:", selected_columns)
        if col_to_analyze:
            fig, ax = plt.subplots()
            sns.histplot(selected_data[col_to_analyze], kde=True, ax=ax, color="skyblue")
            ax.set_title(f"Distribution of {col_to_analyze}")
            st.pyplot(fig)

        # Boxplot for Outlier Detection
        st.subheader("Boxplot for Outliers")
        col_to_boxplot = st.selectbox("Select a column for boxplot:", selected_columns)
        if col_to_boxplot:
            fig, ax = plt.subplots()
            sns.boxplot(x=selected_data[col_to_boxplot], ax=ax, color="lightgreen")
            ax.set_title(f"Boxplot of {col_to_boxplot}")
            st.pyplot(fig)

        # Hypothesis Testing
        st.subheader("Hypothesis Testing")
        st.markdown("### Perform a t-test between two numerical columns")
        numerical_columns = selected_data.select_dtypes(include=np.number).columns.tolist()
        if len(numerical_columns) >= 2:
            col1, col2 = st.selectbox("Select first column:", numerical_columns), st.selectbox("Select second column:", numerical_columns)
            if col1 != col2:
                t_stat, p_val = stats.ttest_ind(selected_data[col1], selected_data[col2], nan_policy='omit')
                st.write(f"T-Statistic: {t_stat:.4f}, P-Value: {p_val:.4f}")
                if p_val < 0.05:
                    st.success("The result is statistically significant (p < 0.05).")
                else:
                    st.info("The result is not statistically significant (p >= 0.05).")

    else:
        st.warning("Please select at least one column for analysis.")

else:
    st.warning("Please upload a CSV file to proceed.")
