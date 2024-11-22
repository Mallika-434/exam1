README: Automobile Data Explorer

Overview
The Automobile Data Explorer is an interactive Streamlit application designed to help users explore, analyze, and visualize an automobile dataset. With this tool, you can gain insights into automobile data through various features like filtering, statistical analysis, and interactive visualizations. Whether you're an automotive analyst or a data enthusiast, this app empowers you to draw meaningful insights quickly.

Features:
1. Data Overview:
   
    Dataset Preview: View the first few rows of the dataset.
  
    Basic Information: Check the dataset's structure, including the number of rows, columns, and column data types.
  
    Statistics: Explore descriptive statistics for numerical columns, such as mean, median, and standard deviation.

3. Custom Data Selection:
Select specific columns to view and analyze using a multiselect widget.
Limit the number of columns displayed with a slider.
Download filtered data as a CSV file.
4. Interactive Visualizations:

    Scatterplot Generator: Explore relationships between numerical features with customizable color options.

      Histogram Viewer: Visualize the distribution of numerical features with      KDE overlays.

   Pie Chart: Analyze the proportion of categories in a selected column.

   Correlation Heatmap: Visualize the correlation between selected numerical    columns.

   Boxplots: Compare a feature with price using visually appealing boxplots.
5. Grouping and Aggregation: 
Group data by a categorical column and compute the mean for a selected numerical column. Visualize grouped data with a bar chart.
6. Statistical Analysis: 
Calculate the Pearson Correlation Coefficient between a numerical feature and price. Determine the statistical significance of the correlation using the p-value.

Prerequisites: To run the application locally, you need the following:
1. Python 3.7+
2. Required Python libraries:

   *streamlit

    *pandas

    *matplotlib

    *seaborn

    *scipy

File Details:
1. examapp.py: The main application file containing all functionalities.
2. CleanedAutomobile.csv: Default dataset loaded from the repository.

Dataset Information:
The dataset, CleanedAutomobile.csv, contains cleaned automobile data with features such as price, fuel type, engine size, and body style.

Key Dependencies:
1. Streamlit: Framework for building interactive web applications.
2. Pandas: For data manipulation and analysis.
3. Matplotlib & Seaborn: For creating static and interactive visualizations.
4. SciPy: For performing statistical tests.
   
Troubleshooting:
1. If the dataset fails to load, ensure the URL in the path variable is accessible or replace it with a local file path.
2. If streamlit is not recognized, ensure the library is installed and your Python environment is properly set up.

Acknowledgments: 
  Streamlit for their user-friendly app framework.
