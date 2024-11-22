import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Sidebar for configuration
st.sidebar.header("Controls")

# Title and App Info
st.title("Interactive EDA App - Automobile Dataset")
st.image("https://your-image-url.com/banner.png", use_column_width=True)
st.write("This app allows you to explore and visualize the Automobile dataset interactively.")

# Load Dataset
st.header("1. Load Dataset")
path = 'https://raw.githubusercontent.com/klamsal/Fall2024Exam/refs/heads/main/CleanedAutomobile.csv'

@st.cache_data
def load_data():
    with st.spinner("Loading Data..."):
        return pd.read_csv(path)

df = load_data()
st.success("Data Loaded Successfully!")

# Dataset Overview
st.markdown("---")
if st.checkbox("Show Dataset Overview"):
    st.subheader("Preview of Dataset")
    st.dataframe(df.head())

    st.subheader("Basic Information")
    st.write(f"Number of Rows: {df.shape[0]}")
    st.write(f"Number of Columns: {df.shape[1]}")
    st.write("Column Data Types:")
    st.write(df.dtypes)

    if st.checkbox("Show Data Statistics"):
        st.write(df.describe())

# Filtering Dataset
st.markdown("---")
st.header("2. Filter Dataset")
columns = df.columns.tolist()

# Sliding option for selecting the number of columns
num_columns = st.slider("Select the number of columns to view", min_value=1, max_value=len(columns), value=5)
selected_columns = st.multiselect("Select Columns to View", columns[:num_columns], default=columns[:num_columns])
filtered_df = df[selected_columns]
st.write("Filtered Data Preview:")
st.dataframe(filtered_df)

# Download Filtered Data
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name='filtered_data.csv',
    mime='text/csv'
)

# Interactive Visualizations
st.markdown("---")
st.header("3. Interactive Visualizations")

# Scatterplot Generator
st.subheader("Scatterplot Generator")
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
x_feature = st.selectbox("Select X-axis Feature", numeric_columns)
y_feature = st.selectbox("Select Y-axis Feature", numeric_columns)
scatter_color = st.sidebar.color_picker("Choose Scatterplot Color", "#FF5733")

if st.button("Generate Scatterplot"):
    fig, ax = plt.subplots()
    sns.scatterplot(x=x_feature, y=y_feature, data=df, color=scatter_color, ax=ax)
    st.pyplot(fig)

# Histogram
st.subheader("Histogram")
if st.checkbox("Show Histogram"):
    feature_histogram = st.selectbox("Select Feature for Histogram", numeric_columns)
    hist_color = st.sidebar.color_picker("Choose Histogram Color", "#3498db")
    fig, ax = plt.subplots()
    sns.histplot(df[feature_histogram], bins=30, kde=True, color=hist_color, ax=ax)
    st.pyplot(fig)

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
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

# Boxplot
st.subheader("Boxplot")
feature_to_analyze = st.selectbox("Select Feature for Boxplot Analysis", columns)
box_color = st.sidebar.color_picker("Choose Boxplot Color", "#2ecc71")

if st.checkbox("Generate Boxplot"):
    fig, ax = plt.subplots()
    sns.boxplot(x=feature_to_analyze, y='price', data=df, color=box_color, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Grouping and Aggregation
st.markdown("---")
st.header("4. Grouping and Aggregation")
group_column = st.selectbox("Select Categorical Column for Grouping", df.select_dtypes(include=['object']).columns)
agg_column = st.selectbox("Select Numeric Column for Aggregation", numeric_columns)

if st.button("Show Grouped Data"):
    grouped_data = df.groupby(group_column)[agg_column].mean().reset_index()
    st.write(grouped_data)

    st.subheader(f"Bar Chart of {agg_column} Grouped by {group_column}")
    fig, ax = plt.subplots()
    sns.barplot(x=group_column, y=agg_column, data=grouped_data, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Statistical Analysis
st.markdown("---")
st.header("5. Statistical Analysis")
analysis_feature = st.selectbox("Select a Feature for Correlation with Price", numeric_columns)

if st.button("Calculate Pearson Correlation"):
    pearson_coef, p_value = stats.pearsonr(df[analysis_feature], df['price'])
    st.write(f"**Selected Feature:** {analysis_feature}")
    st.write(f"**Pearson Correlation Coefficient:** {pearson_coef:.3f}")
    st.write(f"**P-value:** {p_value:.3e}")
    if p_value < 0.05:
        st.success("The correlation is statistically significant.")
    else:
        st.warning("The correlation is not statistically significant.")

# Footer
st.write("This app was created to explore the Automobile dataset interactively.")
