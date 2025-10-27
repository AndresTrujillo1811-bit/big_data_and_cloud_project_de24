import streamlit as st
import plotly.express as px
import pandas as pd
from conn_warehouse import get_job_list


# ---------- Helper function ----------
def find_matching_column(df, keyword):
    """Return first column name containing keyword (case-insensitive)."""
    for col in df.columns:
        if keyword in col.upper():
            return col
    return None


# ---------- Get and aggregate employer data ----------
def get_top_employers(table):
    df_jobs = get_job_list(query=f"SELECT * FROM {table}")

    if df_jobs is None or df_jobs.empty:
        st.warning(f"⚠️ No data found in table {table}.")
        return pd.DataFrame()

    # Normalize columns
    df_jobs.columns = [c.upper() for c in df_jobs.columns]

    # Detect correct column names
    employer_col = find_matching_column(df_jobs, "EMPLOYER")
    vacancy_col = find_matching_column(df_jobs, "VACANC")

    if not employer_col or not vacancy_col:
        st.warning(f"⚠️ Could not find employer/vacancy columns. Found: {df_jobs.columns.tolist()}")
        return pd.DataFrame()

    # Aggregate data
    df_top = (
        df_jobs.groupby(employer_col, as_index=False)[vacancy_col]
        .sum()
        .sort_values(vacancy_col, ascending=False)
        .head(10)
    )

    df_top.columns = ["EMPLOYER_NAME", "VACANCIES"]
    return df_top


# ---------- Display chart ----------
def show_top_employers(table='mart_main'):
    df_top = get_top_employers(table)

    if df_top.empty:
        st.warning("⚠️ No employer data to visualize.")
        return

    fig = px.bar(
        df_top,
        x='VACANCIES',
        y='EMPLOYER_NAME',
        text='VACANCIES',
        orientation='h',
        color='VACANCIES',
        color_continuous_scale="Purples"
    )

    fig.update_traces(
        textposition='outside',
        textfont=dict(size=10, color='black')
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending', 'showgrid': False},
        xaxis={'showgrid': False},
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        bargap=0.4,
        bargroupgap=0.05,
        xaxis_title={"text": "Number of Vacancies", 'font': {'size': 14, 'color': 'black'}},
        yaxis_title={"text": "Employer Name", 'font': {'size': 14, 'color': 'black'}},
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=40),
    )

    st.plotly_chart(fig, use_container_width=True)
