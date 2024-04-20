import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Semester 3 Dashboard",
                   layout="wide")

df = pd.read_excel(
    io='all.xlsx',
    engine='openpyxl',
    sheet_name='all'
)

# Custom header with logo and title
with st.container():
    st.markdown("# Sardar Patel Institute of Technology", unsafe_allow_html=True)

# ---- MAINPAGE ----
st.title("Results Dashboard")
st.markdown("##")


# Sidebar for general filtering
st.sidebar.image('logo.png', width=100)
st.sidebar.header("Filter Options")
division = st.sidebar.multiselect("Select the Class:", options=df['Class'].unique(), default=df['Class'].unique())
semester = st.sidebar.multiselect("Select the Semester:", options=df['Semester'].unique(), default=df['Semester'].unique())
status = st.sidebar.multiselect("Select Status:", options=df['Status'].unique(), default=df['Status'].unique())


# Apply initial filters
filtered_df = df[(df['Class'].isin(division)) & (df['Semester'].isin(semester)) & (df['Status'].isin(status))]

# Column selection for displaying specific "Total" columns
total_columns = [col for col in df.columns if 'Total' in col and 'Total Credits' not in col]
selected_columns = st.sidebar.multiselect(
    "Select columns to display:",
    options=total_columns,
    default=total_columns
)


# KPI Calculations
avg_cgpa = filtered_df['CGPA'].mean()
num_unsuccessful = filtered_df[filtered_df['Status'] == 'Unsuccessful'].shape[0]
mean_scores = filtered_df[selected_columns].mean()
most_scoring_subject = mean_scores.idxmax()
least_scoring_subject = mean_scores.idxmin()

# Display KPIs
st.header("Key Performance Indicators")
row1_col1, row1_col2 = st.columns(2)
row1_col1.metric("Average CGPA", f"{avg_cgpa:.2f}")
row1_col2.metric("Number of Unsuccessful Students", num_unsuccessful)

row2_col1, row2_col2 = st.columns(2)
row2_col1.metric("Least Scoring Subject", least_scoring_subject)
row2_col2.metric("Most Scoring Subject", most_scoring_subject)


# Ensure that 'Class' and 'Semester' are always included for context
display_columns = ['Class', 'Semester', 'Name', 'UID', 'Status', 'CGPA'] + selected_columns
display_df = filtered_df[display_columns]

# Display the filtered dataframe
st.dataframe(display_df)

# Visualization 1: Average Scores per Subject for selected columns
mean_scores = display_df[selected_columns].mean().sort_values(ascending=False)
fig1 = px.bar(x=mean_scores.index, y=mean_scores.values, labels={'x': 'Subjects', 'y': 'Average Score'}, title="Most Scoring Subjects")
st.plotly_chart(fig1)

# Visualization 2: Subjects where students are "Unsuccessful" for selected columns
unsuccessful_df = filtered_df[filtered_df['Status'] == "Unsuccessful"]
unsuccessful_counts = unsuccessful_df[selected_columns].apply(lambda x: (x < 50).sum())  
fig2 = px.bar(x=unsuccessful_counts.index, y=unsuccessful_counts.values, labels={'x': 'Subjects', 'y': 'Number of Unsuccessful Scores'}, title="Subjects with Unsuccessful Scores")
st.plotly_chart(fig2)

# Advanced Visualization: Distribution of Scores per Subject using Box Plots for selected columns
fig3 = px.box(filtered_df, y=selected_columns, labels={'variable': 'Subjects', 'value': 'Scores'}, title="Distribution of Scores per Subject")
st.plotly_chart(fig3)

# Advanced Visualization: Status Overview with a Pie Chart
status_distribution = filtered_df['Status'].value_counts()
fig4 = px.pie(names=status_distribution.index, values=status_distribution.values, title="Overview of Student Status")
st.plotly_chart(fig4)