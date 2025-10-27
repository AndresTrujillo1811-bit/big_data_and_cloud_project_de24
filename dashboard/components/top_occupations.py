import pandas as pd
import matplotlib.pyplot as plt
from conn_warehouse import get_job_list
import streamlit as st  # for dashboard-safe warnings

def occupation_chart(table="mart_main"):
    # Run query
    df = get_job_list(query=f"""
        SELECT 
            occupation,
            SUM(vacancies) AS total_vacancies
        FROM {table}
        GROUP BY occupation
        ORDER BY total_vacancies DESC
        LIMIT 10
    """)

    # Check if data returned
    if df is None or df.empty:
        st.warning(f"⚠️ No data found in table {table}.")
        return plt.figure()

    # Normalize column names to uppercase
    df.columns = [c.upper() for c in df.columns]

    # Safety check for expected columns
    if "OCCUPATION" not in df.columns or "TOTAL_VACANCIES" not in df.columns:
        st.warning(f"⚠️ Columns not found in table {table}. Got: {df.columns.tolist()}")
        return plt.figure()

    # --- Build chart ---
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(df["OCCUPATION"], df["TOTAL_VACANCIES"], color="#b07cf4")
    ax.invert_yaxis()

    ax.set_xlabel("Antal lediga jobb", fontsize=10)
    ax.set_ylabel("")
    ax.text(
        x=-0.25,
        y=1.02,
        s="Yrkesområde",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=10,
    )

    # Simplify look
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="x", which="both", length=0)
    ax.tick_params(axis="y", which="both", length=0)

    # Add value labels
    for i, v in enumerate(df["TOTAL_VACANCIES"]):
        ax.text(v + max(df["TOTAL_VACANCIES"]) * 0.01, i, str(v), va="center", fontsize=9)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    occupation_chart()
