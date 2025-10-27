# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from conn_warehouse import get_job_list

# def show_exp_data(table):
#     df = get_job_list(query=f"""SELECT * FROM {table}""")

#     exp = df['EXPERIENCE_REQUIRED'].value_counts()

#     fig_exp = px.pie(
#             values=exp.values, 
#             names=['Required' if x else 'Not required' for x in exp.index], 
#             title="",
#             hole=0.5,  # Donut style
#             color_discrete_sequence=["#F48720", "#b07cf4", '#45B7D1', '#96CEB4']
#         )
        
#     fig_exp.update_traces(
#         textposition='inside', 
#         textinfo='percent+label',
#         textfont_size=12,
#         marker=dict(line=dict(color='#FFFFFF', width=3))
#     )

#     fig_exp.update_layout(
#         height=280,
#         margin=dict(l=20, r=20, t=20, b=20),
#         showlegend=False,
#         font=dict(family="Arial", size=11),
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)'
#     )

#     st.plotly_chart(fig_exp, use_container_width=True)


# def show_license_data(table):
#     df = get_job_list(query=f"""SELECT * FROM {table}""")

#     exp = df['DRIVING_LICENSE_REQUIRED'].value_counts()

#     fig_exp = px.pie(
#             values=exp.values, 
#             names=['Required' if x else 'Not required' for x in exp.index], 
#             title="",
#             hole=0.5,  # Donut style
#             color_discrete_sequence=["#F48720", "#b07cf4", "#F6F6F8", '#96CEB4']
#         )
        
#     fig_exp.update_traces(
#         textposition='inside', 
#         textinfo='percent+label',
#         textfont_size=12,
#         marker=dict(line=dict(color='#FFFFFF', width=3))
#     )

#     fig_exp.update_layout(
#         height=280,
#         margin=dict(l=20, r=20, t=20, b=20),
#         showlegend=False,
#         font=dict(family="Arial", size=11),
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)'
#     )

#     st.plotly_chart(fig_exp, use_container_width=True)


# def show_pie_chart(table):
#     col1, col2 = st.columns(2)
#     with col1:
#         show_exp_data(table)
#     with col2:
#         show_license_data(table)

import streamlit as st
import pandas as pd
import plotly.express as px
from conn_warehouse import get_job_list


# ---------- Helper: detect best matching column ----------
def find_matching_column(df, keyword):
    """Return the first column name containing the keyword (case-insensitive)."""
    for col in df.columns:
        if keyword in col.upper():
            return col
    return None


# ---------- Pie Chart Creator ----------
def create_pie_chart(data, column_name, title):
    if column_name not in data.columns:
        st.warning(f"⚠️ Column '{column_name}' not found in data. Available columns: {data.columns.tolist()}")
        return px.pie(pd.DataFrame({'category': ['No data'], 'count': [1]}),
                      values='count', names='category', title=f"{title} (No Data)")

    # Count True/False or 1/0 values
    required_count = data[data[column_name].isin([True, 1])].shape[0]
    not_required_count = data[data[column_name].isin([False, 0])].shape[0]

    df_counts = pd.DataFrame({
        'category': ['Required', 'Not required'],
        'count': [required_count, not_required_count]
    })

    fig = px.pie(
        df_counts,
        values='count',
        names='category',
        title=title,
        hole=0.55,
        color='category',
        category_orders={'category': ['Required', 'Not required']},
        color_discrete_map={'Required': "#F48720", 'Not required': "#b07cf4"}
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        textfont_size=14,
        marker=dict(line=dict(color='#FFFFFF', width=3))
    )

    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=50, b=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.2,
            x=0.5,
            xanchor="center"
        ),
        font=dict(family="Arial", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=14, family="Arial Bold")
        )
    )

    return fig


# ---------- Experience Pie ----------
def show_exp_data(table):
    df = get_job_list(query=f"SELECT * FROM {table}")
    if df is None or df.empty:
        st.warning(f"⚠️ No data found in {table}.")
        return

    df.columns = [c.upper() for c in df.columns]
    exp_col = find_matching_column(df, "EXPERIENCE")
    if not exp_col:
        st.warning("⚠️ Could not find any column related to 'EXPERIENCE'.")
        return

    fig = create_pie_chart(df, exp_col, "Experience Required")
    st.plotly_chart(fig, use_container_width=True)


# ---------- License Pie ----------
def show_license_data(table):
    df = get_job_list(query=f"SELECT * FROM {table}")
    if df is None or df.empty:
        st.warning(f"⚠️ No data found in {table}.")
        return

    df.columns = [c.upper() for c in df.columns]
    lic_col = find_matching_column(df, "LICENSE")
    if not lic_col:
        st.warning("⚠️ Could not find any column related to 'LICENSE'.")
        return

    fig = create_pie_chart(df, lic_col, "Driving License Required")
    st.plotly_chart(fig, use_container_width=True)


# ---------- Combined Charts ----------
def show_pie_chart(table):
    col1, col2 = st.columns(2)
    with col1:
        show_exp_data(table)
    with col2:
        show_license_data(table)
