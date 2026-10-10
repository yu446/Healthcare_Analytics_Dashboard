import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Healthcare Survey Dashboard",
    page_icon="🏥",
    layout="wide"
)

# App Title & Description
st.title("🏥 Healthcare & Public Health Analytics Dashboard")
st.markdown("An interactive platform for analyzing public health survey responses, tracking medical metrics, and visualizing field data.")

# 2. Sidebar File Uploader
st.sidebar.header("Data Configuration")
uploaded_file = st.sidebar.file_uploader("Upload your CSV dataset", type=["csv"])

# Load Data (User uploaded file or fallback sample data)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Custom dataset loaded successfully!")
else:
    # Default sample dataset representing public health survey results
    data = {
        "Age_Group": ["18-25", "26-35", "36-50", "50+", "18-25", "26-35", "36-50", "50+"],
        "Awareness_Level": ["High", "High", "Moderate", "Low", "Moderate", "High", "Low", "Low"],
        "Respondents": [120, 210, 150, 80, 95, 180, 130, 60],
        "Region": ["Urban", "Urban", "Urban", "Urban", "Rural", "Rural", "Rural", "Rural"]
    }
    df = pd.DataFrame(data)
    st.sidebar.info("Tip: Upload your own CSV file above to test custom data.")

# 3. Dynamic Sidebar Filters
if "Region" in df.columns:
    region_filter = st.sidebar.selectbox("Filter by Region", options=["All"] + list(df["Region"].unique()))
    if region_filter != "All":
        filtered_df = df[df["Region"] == region_filter]
    else:
        filtered_df = df
else:
    filtered_df = df

# 4. Top KPI Metric Cards
st.subheader("📊 Key Performance Metrics")
col1, col2, col3 = st.columns(3)

col1.metric(label="Total Records", value=len(filtered_df))

if "Respondents" in filtered_df.columns:
    col2.metric(label="Total Respondents", value=int(filtered_df["Respondents"].sum()))
else:
    col2.metric(label="Dataset Columns", value=len(filtered_df.columns))

col3.metric(label="Active Filters", value=region_filter if "Region" in df.columns else "None")

# Divider
st.markdown("---")

# 5. Interactive Visualizations
st.subheader("📈 Data Visualizations")

if "Age_Group" in filtered_df.columns and "Respondents" in filtered_df.columns:
    color_col = "Awareness_Level" if "Awareness_Level" in filtered_df.columns else None
    fig = px.bar(
        filtered_df, 
        x="Age_Group", 
        y="Respondents", 
        color=color_col, 
        barmode="group",
        title="Survey Response Distribution by Age Group"
    )
    st.plotly_chart(fig, width="stretch")
else:
    st.info("The uploaded dataset does not contain standard age/respondent columns for the bar chart, but you can view the raw data below.")

# 6. Raw Data Table View
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df, width="stretch")
