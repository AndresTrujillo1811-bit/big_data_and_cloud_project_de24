import pandas as pd
import json
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
from conn_warehouse import get_job_list
from difflib import get_close_matches
import streamlit as st


# ------------------- Load data and GeoJSON -------------------
def karta(table="mart_main", occupation=None):
    # Prepare SQL filter
    where_clause = f"WHERE occupation_field = '{occupation}'" if occupation else ""
    query = f"""
        SELECT
            SUM(vacancies) AS total_vacancies,
            workplace_region
        FROM {table}
        {where_clause}
        GROUP BY workplace_region
        ORDER BY total_vacancies DESC
    """
    df = get_job_list(query=query)

    if df is None or df.empty:
        st.warning(f"⚠️ No regional data found in {table}.")
        return pd.DataFrame(), {}, {}

    # Normalize column names
    df.columns = [c.upper() for c in df.columns]

    # Use absolute path for GeoJSON file
    geojson_path = Path(__file__).parent.parent / "assets" / "swedish_regions.geojson"

    if not geojson_path.exists():
        st.error(f"❌ GeoJSON file not found: {geojson_path}")
        return df, {}, {}

    with open(geojson_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Extract region name + ID mapping
    region_codes = {}
    for feature in json_data.get("features", []):
        props = feature.get("properties", {})
        name = props.get("name")
        code = str(props.get("l_id") or props.get("id") or props.get("nuts_code") or "")
        if name and code:
            region_codes[name] = code

    return df, json_data, region_codes


# ------------------- Create Map Figure -------------------
def create_map(table="mart_main", occupation=None):
    df, json_data, region_codes = karta(table, occupation)

    if df.empty or not json_data:
        st.warning("⚠️ Map data unavailable or empty.")
        return go.Figure()

    # Ensure data columns exist
    if "WORKPLACE_REGION" not in df.columns or "TOTAL_VACANCIES" not in df.columns:
        st.warning(f"⚠️ Expected columns not found. Got: {df.columns.tolist()}")
        return go.Figure()

    # Prepare z-values
    z_values = df["TOTAL_VACANCIES"].astype(float)

    # Match region names between DB and GeoJSON
    matched_names = []
    for region in df["WORKPLACE_REGION"]:
        if not region:
            matched_names.append("")
            continue
        match = get_close_matches(region, region_codes.keys(), n=1, cutoff=0.6)
        matched_names.append(match[0] if match else region)

    region_ids = [region_codes.get(name, "") for name in matched_names]

    total_vacancies = int(df["TOTAL_VACANCIES"].sum())

    # ------------------- Plotly Choropleth -------------------
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=json_data,
            locations=region_ids,
            z=z_values,
            featureidkey="properties.l_id",
            colorscale="Oranges",
            zmin=0,
            zmax=float(df["TOTAL_VACANCIES"].max()),
            showscale=True,
            customdata=df["TOTAL_VACANCIES"],
            text=df["WORKPLACE_REGION"],
            marker_line_width=0.3,
        )
    )

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            zoom=3.2,
            center=dict(lat=62.6952, lon=13.9149)
        ),
        margin=dict(r=0, t=50, l=0, b=0),
        title=dict(
            text=f"<b>Total Vacancies:</b> {total_vacancies:,}",
            x=0.05,
            y=0.97,
            font=dict(size=14, family="Arial"),
        ),
    )

    return fig

