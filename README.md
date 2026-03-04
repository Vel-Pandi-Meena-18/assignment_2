# assignment_2
A comprehensive Data Science capstone project that investigates the correlation between educational attainment and national wealth. This interactive dashboard, built with Python, Streamlit, and SQLite3, analyzes historical trends to demonstrate how literacy rates influence GDP growth across different global entities.


Global Literacy & Economic Potential Analysis
📌 Project Overview
This repository contains a comprehensive data science application that investigates the correlation between educational attainment and national wealth. By leveraging Python, Streamlit, and SQLite3, the dashboard provides an interactive platform to analyze how literacy rates have historically influenced GDP growth across different global regions.

🚀 Key Features
Dual-Axis Trend Analysis: A specialized "Country Explorer" module that utilizes dual Y-axes to compare Literacy (%) and GDP ($) on independent scales, ensuring clear trend visibility for both metrics regardless of their numerical range.

SQL Analytical Engine: An integrated "SQL Lab" featuring 13 pre-defined analytical queries. The engine dynamically renders Bar, Line, or Pie charts based on the database results.

Interactive EDA Suite: A collection of 10 distinct visualizations categorized into:

Univariate Analysis: Histograms, Box Plots, and Violin plots to understand data distribution and spread.

Bivariate Analysis: Scatter plots with OLS/Lowess trendlines and Heatmaps to identify correlations.

Smart Schema Detection: A robust backend logic that automatically identifies database column variations (e.g., "Entity" vs. "Country") to ensure seamless cross-platform execution.

Data Integrity & Cleaning: All modules are powered by a strictly rectified dataset, featuring automated null-value handling and data type synchronization.

🛠️ Technology Stack
Frontend: Streamlit

Database: SQLite3

Visualization: Plotly Express & Plotly Graph Objects

Data Processing: Pandas & NumPy

📂 File Structure
stmapp.py: The core Streamlit application script containing the UI and visualization logic.

guvi_project.db: The rectified SQLite database with cleaned global data tables.
