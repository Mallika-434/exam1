import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
#from st_aggrid import AgGrid, GridOptionsBuilder

# Configure Streamlit page layout
st.set_page_config(page_title="Automobile Data Explorer", layout="wide")

# Sidebar for configuration
st.sidebar.header("Controls")

# Title and App Info
st.title("Automobile Data Explorer")
st.write("This app allows you to explore and visualize the Automobile dataset interactively.")

# Load Dataset
st.header("Fueling Your Analysis: Data Upload")
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

    # Slider for setting the number of rows to display
    num_rows = st.slider("Number of rows to display", min_value=5, max_value=len(df), value=10)
    styled_df = df.head(num_rows).style.set_precision(2)  # Limit rows and format numbers

    # Display the table with dynamic container width
    st.dataframe(styled_df, use_container_width=True)

    if st.checkbox("Show Basic Information", value=True):  # Checkbox for Basic Info
        st.subheader("Basic Information")
        st.write(f"Number of Rows: {df.shape[0]}")
        st.write(f"Number of Columns: {df.shape[1]}")
        st.write("Column Data Types:")
        st.write(df.dtypes)

    if st.checkbox("Show Data Statistics"):
        st.subheader("Dataset Statistics")
        st.write(df.describe())

if st.checkbox("Show Enhanced Table"):
    st.subheader("Interactive Dataset View")
    st.dataframe(df, use_container_width=True)

# Filtering Dataset
st.markdown("---")
st.header("Custom Data Selection")
columns = df.columns.tolist()

# Sliding option to set the maximum number of columns to view
num_columns = st.slider("Set the maximum number of columns to view", min_value=1, max_value=len(columns), value=3)

# Multi-select with restriction
selected_columns = st.multiselect("Select Columns to View (Max: {} columns)".format(num_columns), columns)

# Logic to restrict column selection
if len(selected_columns) > num_columns:
    st.toast("You can only select up to {} columns. Extra columns will not be added.".format(num_columns), icon="⚠️")
    selected_columns = selected_columns[:num_columns]  # Truncate to allowed columns

# Display Filtered Data
st.write("Filtered Data Preview:")
st.dataframe(df[selected_columns])

# Download Filtered Data
st.download_button(
    label="Download Filtered Data as CSV",
    data=df[selected_columns].to_csv(index=False),
    file_name='filtered_data.csv',
    mime='text/csv'
)

# Interactive Visualizations
st.markdown("---")
st.header("Discover Patterns: Interactive Visualizations")

# Scatterplot Generator
st.subheader("Uncover Relationships: Scatterplot Generator")
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
x_feature = st.selectbox("Select X-axis Feature", numeric_columns)
y_feature = st.selectbox("Select Y-axis Feature", numeric_columns)
scatter_color = st.sidebar.color_picker("Choose Scatterplot Color", "#FF5733")

if st.button("Generate Scatterplot"):
    fig, ax = plt.subplots()
    sns.scatterplot(x=x_feature, y=y_feature, data=df, color=scatter_color, ax=ax)
    st.pyplot(fig)

# Histogram
st.subheader("Analyze Spread: Histogram Viewer")
feature_histogram = st.selectbox("Select Feature for Histogram", numeric_columns)
hist_color = st.sidebar.color_picker("Choose Histogram Color", "#3498db")

if st.button("Generate Histogram"):
    fig, ax = plt.subplots()
    sns.histplot(df[feature_histogram], bins=30, kde=True, color=hist_color, ax=ax)
    ax.set_title(f"Histogram of {feature_histogram}")
    st.pyplot(fig)

# Pie Chart
st.subheader("Visualize Distributions: Pie Chart")
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
selected_category = st.selectbox("Select Categorical Column for Pie Chart", categorical_columns)

if st.button("Generate Pie Chart"):
    category_counts = df[selected_category].value_counts()
    fig, ax = plt.subplots()
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.set_title(f"Distribution of {selected_category}")
    st.pyplot(fig)

# Correlation Heatmap
st.subheader("Understanding Relationships: Heatmap")
selected_corr_columns = st.multiselect(
    "Select Columns for Correlation Heatmap",
    numeric_columns,
    default=numeric_columns[:5]
)

if st.button("Generate Heatmap"):
    if selected_corr_columns:
        corr_matrix = df[selected_corr_columns].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title("Correlation Heatmap")
        st.pyplot(fig)
    else:
        st.warning("Please select at least one column for the heatmap.")

# Boxplot
st.subheader("Comparative Insights: Boxplots")
feature_to_analyze = st.selectbox("Select Feature for Boxplot Analysis", columns)
box_color = st.sidebar.color_picker("Choose Boxplot Color", "#2ecc71")

if st.button("Generate Boxplot"):
    fig, ax = plt.subplots()
    sns.boxplot(x=feature_to_analyze, y='price', data=df, color=box_color, ax=ax)
    plt.xticks(rotation=90)
    ax.set_title(f"Boxplot of {feature_to_analyze} vs Price")
    st.pyplot(fig)

# Grouping and Aggregation
st.markdown("---")
st.header("Summarizing Key Metrics")
group_column = st.selectbox("Select Categorical Column for Grouping", df.select_dtypes(include=['object']).columns)
agg_column = st.selectbox("Select Numeric Column for Aggregation", numeric_columns)

if st.button("Show Grouped Data"):
    grouped_data = df.groupby(group_column)[agg_column].mean().reset_index()
    st.write(grouped_data)

    st.subheader(f"Bar Chart of {agg_column} Grouped by {group_column}")
    fig, ax = plt.subplots()
    sns.barplot(x=group_column, y=agg_column, data=grouped_data, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

# Statistical Analysis
st.markdown("---")
st.header("Quantify Relationships: Statistical Analysis")
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
st.write("Your Automobile Data Analysis Journey Ends Here.")
