# ==============================================================================
# PROJECT DOCUMENTATION & ANALYTICAL OVERVIEW
# ==============================================================================

# --- Domain Introduction ---
# The socio-economic domain analyzes how human capital development, specifically education,
# serves as a primary driver for national economic prosperity.
# It uses data to identify regional gaps in literacy and gender parity that impact global development.

# --- Project Introduction ---
# This project is an interactive analytical dashboard designed to visualize the historical
# correlation between global literacy rates and economic growth.
# It transforms raw data into actionable insights using a Python-based visualization engine.

# --- Objective of the Project ---
# The objective is to establish a clear statistical link between a nation's educational investment
# and its subsequent economic output.
# It provides a user-friendly platform to identify regional success stories through complex data querying.

# --- ELT Approach ---
# I followed an ELT (Extract, Load, Transform) workflow, loading raw CSV data into SQLite
# before performing cleaning and standardizations using SQL and Pandas.
# This ensures the "Gold" dataset is fully rectified for accurate trend analysis.

# --- Data Migration ---
# Data migration involves extracting JSON-like documents from MongoDB and flattening
# them into a tabular relational format for SQL.
# This transfer ensures ACID compliance and significantly faster join operations for time-series visualizations.

# --- EDA (Exploratory Data Analysis) ---
# My analysis revealed a strong positive correlation between schooling years and wealth,
# though some nations show education levels outstripping GDP growth.
# I also found that global gender literacy gaps have narrowed significantly, but regional pockets of inequality still exist.

# --- Feature Engineering ---
# I engineered an Education Index to evaluate school system efficiency and used
# Forward-Fill (Time-Series Imputation) to rectify missing GDP records.
# This ensures continuous, reliable trend lines for every country in the dashboard.

# --- Statistical Technique ---
# I used Ordinary Least Squares (OLS) Regression to calculate linear trends and
# Lowess Smoothing to identify non-linear growth patterns.
# These were chosen to provide both a mathematical baseline and a localized understanding of complex country-specific trends.

# --- Conclusion ---
# The project proves that sustained increases in adult literacy are a consistent precursor
# to national economic stability and GDP growth.
# Equitable education across genders remains the most reliable predictor for long-term regional development.

# --- Business Suggestion/Solution ---
# Policymakers should focus on "Secondary Education" as the data shows the sharpest wealth
# increases occur after crossing a 7-year schooling threshold.
# I implemented a Dual-Axis Visualization to allow stakeholders to instantly see this correlation despite different data scales.

# ==============================================================================
# END OF DOCUMENTATION
# ==============================================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. DATABASE & CONFIG ---
st.set_page_config(page_title="Global Education & GDP Analytics", layout="wide", page_icon="📈")


def get_connection():
    return sqlite3.connect("guvi_project.db", check_same_thread=False)


conn = get_connection()

# --- 2. SMART COLUMN DETECTION (Fixes KeyError) ---
# Automatically detects if table uses 'entity' or 'country'
df_schema = pd.read_sql("SELECT * FROM gdp_schooling LIMIT 1", conn)
c_col = 'entity' if 'entity' in df_schema.columns else 'country'

# --- 3. NAVIGATION ---
st.sidebar.title("📊 Project Dashboard")
page = st.sidebar.radio("Navigate to:", ["🏠 Home", "🌍 Country Explorer", "📈 EDA Visuals", "💾 SQL Lab"])

# ==========================================
# PAGE: HOME
# ==========================================
if page == "🏠 Home":
    st.title("Global Literacy & Economic Analysis")
    st.image(
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
        use_container_width=True)
    st.markdown("---")
    st.subheader("Project Overview")
    st.write(
        "An analytical study on the correlation between global literacy rates and national economic productivity (GDP).")

    c1, c2, c3 = st.columns(3)
    c1.metric("Engine", "Python & SQLite")
    c2.metric("Data Status", "Verified & Cleaned")
    c3.metric("Visuals", "Interactive Plotly")

# ==========================================
# PAGE: COUNTRY EXPLORER (Dual-Axis Fixed)
# ==========================================
elif page == "🌍 Country Explorer":
    st.title("National Growth Trends")
    entities = sorted(pd.read_sql(f"SELECT DISTINCT {c_col} FROM gdp_schooling", conn)[c_col].tolist())
    sel_entity = st.selectbox("Select Country:", entities, index=entities.index("India") if "India" in entities else 0)

    # Pulling directly from main DB to ensure data is found
    df = pd.read_sql(f"SELECT year, adult_literacy, gdp_per_capita FROM gdp_schooling WHERE {c_col}='{sel_entity}'",
                     conn).dropna()

    if not df.empty:
        # Scale fix: Dual Y-Axes so Literacy (0-100) and GDP both look good
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df['year'], y=df['adult_literacy'], name="Literacy (%)", line=dict(color="#00CC96")),
                      secondary_y=False)
        fig.add_trace(go.Scatter(x=df['year'], y=df['gdp_per_capita'], name="GDP ($)", line=dict(color="#636EFA")),
                      secondary_y=True)
        fig.update_yaxes(title_text="Literacy Rate (%)", secondary_y=False)
        fig.update_yaxes(title_text="GDP Per Capita ($)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)

# ==========================================
# PAGE: EDA VISUALS (All 10 Graphs)
# ==========================================
elif page == "📈 EDA Visuals":
    st.title("Exploratory Data Analysis")
    u_tab, b_tab = st.tabs(["Univariate Analysis", "Bivariate Analysis"])
    df_eda = pd.read_sql("SELECT * FROM gdp_schooling", conn).dropna()

    with u_tab:
        st.plotly_chart(px.histogram(df_eda, x="adult_literacy", title="1. Literacy Distribution"))
        st.plotly_chart(px.box(df_eda, y="gdp_per_capita", title="2. GDP Spread"))
        st.plotly_chart(px.violin(df_eda, y="youth_female", title="3. Female Youth Density", box=True))
        df_reg = df_eda.groupby(c_col).size().reset_index(name='count').head(15)
        st.plotly_chart(px.pie(df_reg, values='count', names=c_col, title="4. Data Contribution", hole=0.5))
        st.plotly_chart(px.histogram(df_eda, x="avg_schooling_years", title="5. Schooling Years Distribution"))

    with b_tab:
        st.plotly_chart(px.scatter(df_eda, x="avg_schooling_years", y="gdp_per_capita", trendline="ols",
                                   title="6. Schooling vs GDP"))

        # India Correlation Fail-Safe
        df_ind = df_eda[df_eda[c_col] == 'India']
        if not df_ind.empty:
            st.plotly_chart(px.scatter(df_ind, x="adult_literacy", y="gdp_per_capita", title="7. India Correlation"))

        st.plotly_chart(
            px.scatter(df_eda, x="youth_male", y="youth_female", color="year", title="8. Gender Correlation"))
        df_time = df_eda.groupby('year')['adult_literacy'].mean().reset_index()
        st.plotly_chart(px.line(df_time, x='year', y='adult_literacy', title="9. Global Progress", markers=True))

        x_heat = "education_index" if "education_index" in df_eda.columns else "adult_literacy"
        st.plotly_chart(
            px.density_heatmap(df_eda, x=x_heat, y="gdp_per_capita", title="10. Education vs Wealth Heatmap"))

# ==========================================
# PAGE: SQL LAB (13 Queries + Visuals)
# ==========================================
elif page == "💾 SQL Lab":
    st.title("SQL Analytical Engine")
    queries = {
        "Q1: Top 5 Literacy (2020)": (
            f"SELECT {c_col} as Label, adult_literacy as Value FROM literacy_rates WHERE year=2020 ORDER BY Value DESC LIMIT 5",
            "bar"),
        "Q2: Female Youth < 80%": (
            f"SELECT {c_col} as Label, youth_female as Value FROM literacy_rates WHERE youth_female < 80 LIMIT 10",
            "bar"),
        "Q3: Avg Literacy per Entity": (
            f"SELECT {c_col} as Label, AVG(adult_literacy) as Value FROM literacy_rates GROUP BY {c_col} LIMIT 10",
            "bar"),
        "Q4: Illiteracy > 20% (2000)": (
            f"SELECT {c_col} as Label, illiteracy_pct as Value FROM illiteracy_population WHERE year=2000 AND Value > 20",
            "bar"),
        "Q5: India Illiteracy Trend": (
            f"SELECT year as Label, (100-adult_literacy) as Value FROM gdp_schooling WHERE {c_col}='India'", "line"),
        "Q6: Top 10 Illiterate 2015": (
            f"SELECT {c_col} as Label, illiteracy_pct as Value FROM illiteracy_population WHERE year=2015 ORDER BY Value DESC LIMIT 10",
            "bar"),
        "Q7: High School/Low GDP": (
            f"SELECT {c_col} as Label, gdp_per_capita as Value FROM gdp_schooling WHERE avg_schooling_years > 7 AND Value < 5000",
            "bar"),
        "Q8: GDP/Schooling Rank": (
            f"SELECT {c_col} as Label, gdp_per_schooling as Value FROM gdp_schooling WHERE year=2020 ORDER BY Value DESC LIMIT 10",
            "bar"),
        "Q9: Global Schooling Trend": (
            "SELECT year as Label, AVG(avg_schooling_years) as Value FROM gdp_schooling GROUP BY Label", "line"),
        "Q10: High GDP/Low School": (
            f"SELECT {c_col} as Label, gdp_per_capita as Value FROM gdp_schooling WHERE Value > 10000 AND avg_schooling_years < 8",
            "bar"),
        "Q11: Education Index View": (f"SELECT {c_col} as Label, education_index as Value FROM gdp_schooling LIMIT 10",
                                      "bar"),
        "Q12: India Final View": (
            f"SELECT year as Label, adult_literacy as Value FROM gdp_schooling WHERE {c_col}='India'", "line"),
        "Q13: Rich Country Gender Gap": (
            f"SELECT {c_col} as Label, (youth_male-youth_female) as Value FROM literacy_rates WHERE year=2020 LIMIT 10",
            "bar")
    }

    q_sel = st.selectbox("Select Question:", list(queries.keys()))
    sql, c_type = queries[q_sel]
    if st.button("Run Analytics"):
        res = pd.read_sql(sql, conn).dropna()
        if not res.empty:
            if c_type == "bar":
                st.plotly_chart(px.bar(res, x='Label', y='Value', color='Value'))
            elif c_type == "line":
                st.plotly_chart(px.line(res, x='Label', y='Value', markers=True))
            elif c_type == "pie":
                st.plotly_chart(px.pie(res, names='Label', values='Value', hole=0.3))
            st.dataframe(res, use_container_width=True)

conn.close()