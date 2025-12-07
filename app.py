import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

# ==============================
# DB CONNECTION HELPERS
# ==============================

@st.cache_resource
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="phonepe_data",
        port=3306
    )

@st.cache_data
def run_query(sql, params=None):
    conn = get_connection()
    return pd.read_sql(sql, conn, params=params)


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="PhonePe Pulse",
    layout="wide"
)

st.title("📊 PhonePe Pulse Dashboard")


# ==============================
# TAB LAYOUT
# ==============================

tab_overview, tab_txn, tab_device, tab_ins, tab_market, tab_engagement = st.tabs([
    "🏠 Overview",
    "💸 Transaction Dynamics",
    "📱 Device & Engagement",
    "🛡 Insurance Insights",
    "🌍 Market Expansion",
    "👥 User Engagement"
])


# ==============================
# 🏠 OVERVIEW TAB
# ==============================

with tab_overview:
    st.subheader("Project Overview")

    st.markdown(
        """
        This dashboard is built using PhonePe Pulse data to analyze:

        - **Transaction Dynamics:** How transaction volume and value evolve across years, quarters, payment types, and states.  
        - **Device Dominance & Engagement:** How different mobile brands and devices contribute to PhonePe usage and app engagement.  
        - **Insurance Penetration:** How digital insurance products are adopted across states and districts.  
        - **Market Expansion:** Which states offer the highest growth potential in terms of transaction count and value.  
        - **User Engagement & Growth Strategy:** How registered users and app opens behave across regions and pincodes.  

        Use the tabs above to explore each scenario.
        """
    )

    st.markdown("---")

    # Quick high-level metrics from aggregated_transaction and aggregated_user
    col1, col2, col3 = st.columns(3)

    # Total transaction value & count
    df_txn_summary = run_query("""
        SELECT 
            SUM(txn_amount) AS total_amount,
            SUM(txn_count)  AS total_count
        FROM aggregated_transaction;
    """)
    total_amount = df_txn_summary["total_amount"].iloc[0] if not df_txn_summary.empty else 0
    total_count = df_txn_summary["total_count"].iloc[0] if not df_txn_summary.empty else 0

    # Total registered users (from aggregated_user)
    df_users_summary = run_query("""
        SELECT 
            SUM(total_registered_users) AS total_users
        FROM aggregated_user
        WHERE total_registered_users IS NOT NULL;
    """)
    total_users = df_users_summary["total_users"].iloc[0] if not df_users_summary.empty else 0

    with col1:
        st.metric("Total Transaction Amount", f"₹ {total_amount:,.0f}")
    with col2:
        st.metric("Total Transaction Count", f"{total_count:,.0f}")
    with col3:
        st.metric("Total Registered Users", f"{total_users:,.0f}")


# ==============================
# 💸 TRANSACTION DYNAMICS TAB (SCENARIO 1)
# ==============================

with tab_txn:
    st.subheader("Scenario 1 – Decoding Transaction Dynamics")

    # --- Yearly Trend (All India) ---
    st.markdown("### 🔹 Yearly Transaction Trend (All India)")

    df_yearly_txn = run_query("""
        SELECT 
            year,
            SUM(txn_count)  AS total_txn_count,
            SUM(txn_amount) AS total_txn_amount
        FROM aggregated_transaction
        GROUP BY year
        ORDER BY year;
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.line(
            df_yearly_txn, x="year", y="total_txn_amount", markers=True,
            title="Total Transaction Amount by Year (All India)",
            labels={"total_txn_amount": "Total Transaction Amount"}
        )
        fig_amount.update_layout(xaxis=dict(dtick=1))
        st.plotly_chart(fig_amount, use_container_width=True, key="txn_year_amount")

    with col2:
        fig_count = px.line(
            df_yearly_txn, x="year", y="total_txn_count", markers=True,
            title="Total Transaction Count by Year (All India)",
            labels={"total_txn_count": "Total Transaction Count"}
        )
        fig_count.update_layout(xaxis=dict(dtick=1))
        st.plotly_chart(fig_count, use_container_width=True, key="txn_year_count")

    st.markdown("---")

    # --- Transaction Type Trend ---
    st.markdown("### 🔹 Transaction Type Trend Across Years")

    df_txn_type_trend = run_query("""
        SELECT 
            year,
            txn_type,
            SUM(txn_count)  AS total_txn_count,
            SUM(txn_amount) AS total_txn_amount
        FROM aggregated_transaction
        GROUP BY year, txn_type
        ORDER BY year, total_txn_amount DESC;
    """)

    fig_type_line = px.line(
        df_txn_type_trend,
        x="year",
        y="total_txn_amount",
        color="txn_type",
        markers=True,
        title="Transaction Amount Trend by Payment Type",
        labels={"total_txn_amount": "Total Transaction Amount", "txn_type": "Payment Type"}
    )
    fig_type_line.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_type_line, use_container_width=True, key="txn_type_line")

    st.markdown("---")

    # --- State-wise View for Selected Year ---
    st.markdown("### 🔹 State-wise Transaction Value for a Selected Year")

    df_state_year = run_query("""
        SELECT 
            state,
            year,
            SUM(txn_count)  AS total_txn_count,
            SUM(txn_amount) AS total_txn_amount
        FROM aggregated_transaction
        GROUP BY state, year
        ORDER BY year, total_txn_amount DESC;
    """)

    years_available = sorted(df_state_year["year"].unique().tolist())
    sel_year_txn = st.selectbox("Select Year", years_available, index=len(years_available)-1, key="txn_state_year")

    df_year_filter = df_state_year[df_state_year["year"] == sel_year_txn]

    fig_state_bar = px.bar(
        df_year_filter.sort_values("total_txn_amount", ascending=False).head(15),
        x="state",
        y="total_txn_amount",
        title=f"Top 15 States by Transaction Amount – {sel_year_txn}",
        labels={"total_txn_amount": "Total Transaction Amount"}
    )
    fig_state_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_state_bar, use_container_width=True, key="txn_state_bar")


# ==============================
# 📱 DEVICE & ENGAGEMENT TAB (SCENARIO 2)
# ==============================

with tab_device:
    st.subheader("Scenario 2 – Device Dominance & User Engagement")

    # --- Brand Trend Across Years ---
    st.markdown("### 🔹 Mobile Brand Usage Trend Across Years")

    df_brand_trend = run_query("""
        SELECT
            year,
            device_brand AS brand,
            SUM(device_user_count) AS total_registered_users
        FROM aggregated_user
        GROUP BY year, device_brand
        ORDER BY year, total_registered_users DESC;
    """)

    fig_brand_line = px.line(
        df_brand_trend,
        x="year",
        y="total_registered_users",
        color="brand",
        markers=True,
        title="Mobile Brand Usage Trend Across Years",
        labels={"total_registered_users": "Registered Users", "brand": "Device Brand"}
    )
    fig_brand_line.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_brand_line, use_container_width=True, key="device_brand_trend")

    st.markdown("---")

    # --- State-wise Brand Preference for a Selected Year & State ---
    st.markdown("### 🔹 State-wise Device Preference")

    df_state_brand = run_query("""
        SELECT
            state,
            year,
            device_brand AS brand,
            SUM(device_user_count) AS total_users
        FROM aggregated_user
        GROUP BY state, year, device_brand;
    """)

    years_device = sorted(df_state_brand["year"].unique().tolist())
    sel_year_dev = st.selectbox("Select Year", years_device, index=len(years_device)-1, key="device_year")

    states_device = sorted(df_state_brand["state"].unique().tolist())
    sel_state_dev = st.selectbox("Select State", states_device, key="device_state")

    df_year_state = df_state_brand[
        (df_state_brand["year"] == sel_year_dev) &
        (df_state_brand["state"] == sel_state_dev)
    ]

    if df_year_state.empty:
        st.info("No data for this state/year combination.")
    else:
        fig_state_brand = px.bar(
            df_year_state.sort_values("total_users", ascending=False),
            x="brand",
            y="total_users",
            title=f"Device Brand Usage in {sel_state_dev} – {sel_year_dev}",
            labels={"brand": "Device Brand", "total_users": "Registered Users"}
        )
        fig_state_brand.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_state_brand, use_container_width=True, key="device_state_brand")

    st.markdown("---")

    # --- Engagement Ratio (AppOpens / RegisteredUsers) ---
    st.markdown("### 🔹 Engagement – App Opens vs Registered Users (State-wise)")

    df_engagement = run_query("""
        SELECT
            state,
            year,
            SUM(total_registered_users) AS total_registered_users,
            SUM(total_app_opens)       AS total_app_opens
        FROM aggregated_user
        WHERE total_registered_users IS NOT NULL
          AND total_app_opens IS NOT NULL
        GROUP BY state, year
        HAVING SUM(total_registered_users) > 0;
    """)
    df_engagement["engagement_ratio"] = df_engagement["total_app_opens"] / df_engagement["total_registered_users"]

    years_eng = sorted(df_engagement["year"].unique().tolist())
    sel_year_eng = st.selectbox("Select Year (Engagement)", years_eng, index=len(years_eng)-1, key="eng_year")

    df_eng_y = df_engagement[df_engagement["year"] == sel_year_eng]

    col1, col2 = st.columns(2)

    with col1:
        top_eng = df_eng_y.sort_values("engagement_ratio", ascending=False).head(10)
        fig_top_eng = px.bar(
            top_eng,
            x="state",
            y="engagement_ratio",
            title=f"Top 10 States by Engagement Ratio – {sel_year_eng}",
            labels={"engagement_ratio": "AppOpens / RegisteredUser"}
        )
        fig_top_eng.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_top_eng, use_container_width=True, key="eng_top")

    with col2:
        low_eng = df_eng_y.sort_values("engagement_ratio", ascending=True).head(10)
        fig_low_eng = px.bar(
            low_eng,
            x="state",
            y="engagement_ratio",
            title=f"Bottom 10 States by Engagement Ratio – {sel_year_eng}",
            labels={"engagement_ratio": "AppOpens / RegisteredUser"}
        )
        fig_low_eng.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_low_eng, use_container_width=True, key="eng_low")


# ==============================
# 🛡 INSURANCE INSIGHTS TAB (SCENARIO 3)
# ==============================

with tab_ins:
    st.subheader("Scenario 3 – Insurance Penetration & Growth Potential")

    # --- Yearly Insurance Trend ---
    st.markdown("### 🔹 Yearly Insurance Growth (All India)")

    df_ins_year = run_query("""
        SELECT
            year,
            SUM(ins_count)  AS total_insurance_policies,
            SUM(ins_amount) AS total_insurance_value
        FROM aggregated_insurance
        GROUP BY year
        ORDER BY year;
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig_ins_val = px.line(
            df_ins_year,
            x="year",
            y="total_insurance_value",
            markers=True,
            title="Yearly Insurance Transaction Value (India)",
            labels={"total_insurance_value": "Insurance Value"}
        )
        fig_ins_val.update_layout(xaxis=dict(dtick=1))
        st.plotly_chart(fig_ins_val, use_container_width=True, key="ins_val")

    with col2:
        fig_ins_cnt = px.line(
            df_ins_year,
            x="year",
            y="total_insurance_policies",
            markers=True,
            title="Yearly Insurance Policy Count (India)",
            labels={"total_insurance_policies": "Number of Policies"}
        )
        fig_ins_cnt.update_layout(xaxis=dict(dtick=1))
        st.plotly_chart(fig_ins_cnt, use_container_width=True, key="ins_cnt")

    st.markdown("---")

    # --- State-wise Insurance Value for Selected Year ---
    st.markdown("### 🔹 State-wise Insurance Value")

    df_ins_state = run_query("""
        SELECT
            state,
            year,
            SUM(ins_count)  AS total_insurance_policies,
            SUM(ins_amount) AS total_insurance_value
        FROM aggregated_insurance
        GROUP BY state, year
        ORDER BY total_insurance_value DESC;
    """)

    years_ins = sorted(df_ins_state["year"].unique().tolist())
    sel_year_ins = st.selectbox("Select Year", years_ins, index=len(years_ins)-1, key="ins_state_year")

    df_ins_year_sel = df_ins_state[df_ins_state["year"] == sel_year_ins]

    col3, col4 = st.columns(2)

    with col3:
        fig_ins_top_states = px.bar(
            df_ins_year_sel.nlargest(10, "total_insurance_value"),
            x="state",
            y="total_insurance_value",
            title=f"Top 10 States by Insurance Value – {sel_year_ins}"
        )
        fig_ins_top_states.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_ins_top_states, use_container_width=True, key="ins_top_states")

    with col4:
        fig_ins_bottom_states = px.bar(
            df_ins_year_sel.nsmallest(10, "total_insurance_value"),
            x="state",
            y="total_insurance_value",
            title=f"Bottom 10 States by Insurance Value – {sel_year_ins}"
        )
        fig_ins_bottom_states.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_ins_bottom_states, use_container_width=True, key="ins_bottom_states")

    st.markdown("---")

    # --- District-level Insurance (map_insurance) ---
    st.markdown("### 🔹 District-level Insurance (map_insurance)")

    df_ins_dist = run_query("""
        SELECT
            state,
            district,
            year,
            SUM(ins_count)  AS total_insurance_policies,
            SUM(ins_amount) AS total_insurance_value
        FROM map_insurance
        GROUP BY state, district, year;
    """)

    years_ins_dist = sorted(df_ins_dist["year"].unique().tolist())
    sel_year_ins_dist = st.selectbox("Select Year (District View)", years_ins_dist,
                                     index=len(years_ins_dist)-1, key="ins_dist_year")

    df_ins_dist_year = df_ins_dist[df_ins_dist["year"] == sel_year_ins_dist]

    col5, col6 = st.columns(2)

    with col5:
        fig_top_districts = px.bar(
            df_ins_dist_year.nlargest(10, "total_insurance_value"),
            x="district",
            y="total_insurance_value",
            color="state",
            title=f"Top 10 Districts by Insurance Value – {sel_year_ins_dist}"
        )
        fig_top_districts.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_top_districts, use_container_width=True, key="ins_top_dist")

    with col6:
        fig_bottom_districts = px.bar(
            df_ins_dist_year.nsmallest(10, "total_insurance_value"),
            x="district",
            y="total_insurance_value",
            color="state",
            title=f"Bottom 10 Districts by Insurance Value – {sel_year_ins_dist}"
        )
        fig_bottom_districts.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bottom_districts, use_container_width=True, key="ins_bottom_dist")


# ==============================
# 🌍 MARKET EXPANSION TAB (SCENARIO 4)
# ==============================

with tab_market:
    st.subheader("Scenario 4 – Market Expansion Analysis")

    # --- State-Year Summary ---
    df_state_year = run_query("""
        SELECT 
            state,
            year,
            SUM(txn_count)  AS total_txn_count,
            SUM(txn_amount) AS total_txn_amount
        FROM aggregated_transaction
        GROUP BY state, year
        ORDER BY state, year;
    """)

    # Compute YoY growth %
    df_state_year["txn_growth_pct"] = df_state_year.groupby("state")["total_txn_count"].pct_change() * 100
    df_state_year["amount_growth_pct"] = df_state_year.groupby("state")["total_txn_amount"].pct_change() * 100

    latest_year = df_state_year["year"].max()
    st.markdown(f"### 🔹 Fastest Growing States (Transaction Count YoY Growth – {latest_year})")

    df_growth_latest = df_state_year[df_state_year["year"] == latest_year].dropna(subset=["txn_growth_pct"])
    fig_growth = px.bar(
        df_growth_latest.sort_values("txn_growth_pct", ascending=False).head(10),
        x="state",
        y="txn_growth_pct",
        title=f"Top 10 Fastest Growing States – {latest_year}",
        labels={"txn_growth_pct": "Growth %"}
    )
    fig_growth.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_growth, use_container_width=True, key="market_growth")

    st.markdown("---")

    # --- Market Size (Total Count & Amount) ---
    st.markdown("### 🔹 Market Size by State (Total Transaction Value)")

    df_market = run_query("""
        SELECT
            state,
            SUM(txn_count)  AS total_txn_count,
            SUM(txn_amount) AS total_txn_amount
        FROM aggregated_transaction
        GROUP BY state
        ORDER BY total_txn_amount DESC;
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig_market_top = px.bar(
            df_market.head(10),
            x="state",
            y="total_txn_amount",
            title="Top 10 States by Transaction Value",
            labels={"total_txn_amount": "Total Transaction Amount"}
        )
        fig_market_top.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_market_top, use_container_width=True, key="market_top")

    with col2:
        fig_market_bottom = px.bar(
            df_market.tail(10).sort_values("total_txn_amount"),
            x="state",
            y="total_txn_amount",
            title="Bottom 10 States by Transaction Value (Expansion Opportunities)",
            labels={"total_txn_amount": "Total Transaction Amount"}
        )
        fig_market_bottom.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_market_bottom, use_container_width=True, key="market_bottom")

    st.markdown("---")

    # --- Growth–Potential Matrix ---
    st.markdown("### 🔹 Growth–Potential Matrix (Count vs Value)")

    # Normalize
    df_market["count_norm"] = (df_market["total_txn_count"] - df_market["total_txn_count"].min()) / \
                              (df_market["total_txn_count"].max() - df_market["total_txn_count"].min())

    df_market["amount_norm"] = (df_market["total_txn_amount"] - df_market["total_txn_amount"].min()) / \
                               (df_market["total_txn_amount"].max() - df_market["total_txn_amount"].min())

    df_market["category"] = df_market.apply(
        lambda row:
            "High Count – High Value" if row["count_norm"] >= 0.5 and row["amount_norm"] >= 0.5 else
            "High Count – Low Value"  if row["count_norm"] >= 0.5 and row["amount_norm"] < 0.5 else
            "Low Count – High Value"  if row["count_norm"] < 0.5 and row["amount_norm"] >= 0.5 else
            "Low Count – Low Value",
        axis=1
    )

    fig_matrix = px.scatter(
        df_market,
        x="total_txn_count",
        y="total_txn_amount",
        color="category",
        hover_data=["state"],
        title="State Market Segmentation – Growth Potential Matrix",
        labels={
            "total_txn_count": "Total Transaction Count",
            "total_txn_amount": "Total Transaction Amount"
        }
    )
    st.plotly_chart(fig_matrix, use_container_width=True, key="market_matrix")


# ==============================
# 👥 USER ENGAGEMENT TAB (SCENARIO 5)
# ==============================

with tab_engagement:
    st.subheader("Scenario 5 – User Engagement & Growth Strategy")

    # --- State-level Registered Users & App Opens ---
    st.markdown("### 🔹 State-wise User Base & Engagement")

    df_user_state = run_query("""
        SELECT
            state,
            SUM(registered_users) AS total_registered_users,
            SUM(app_opens)        AS total_app_opens
        FROM map_user
        GROUP BY state
        ORDER BY total_registered_users DESC;
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig_reg_state = px.bar(
            df_user_state.head(10),
            x="state",
            y="total_registered_users",
            title="Top 10 States by Registered Users",
            labels={"total_registered_users": "Registered Users"}
        )
        fig_reg_state.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_reg_state, use_container_width=True, key="eng_reg_state")

    with col2:
        fig_app_state = px.bar(
            df_user_state.sort_values("total_app_opens", ascending=False).head(10),
            x="state",
            y="total_app_opens",
            title="Top 10 States by App Opens",
            labels={"total_app_opens": "App Opens"}
        )
        fig_app_state.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_app_state, use_container_width=True, key="eng_app_state")

    st.markdown("---")

    # --- District-level Engagement ---
    st.markdown("### 🔹 District-wise Engagement (Registered Users & App Opens)")

    df_user_dist = run_query("""
        SELECT
            state,
            district,
            SUM(registered_users) AS total_registered_users,
            SUM(app_opens)        AS total_app_opens
        FROM map_user
        GROUP BY state, district
        ORDER BY total_registered_users DESC;
    """)

    fig_reg_dist = px.bar(
        df_user_dist.head(10),
        x="district",
        y="total_registered_users",
        color="state",
        title="Top 10 Districts by Registered Users"
    )
    fig_reg_dist.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_reg_dist, use_container_width=True, key="eng_reg_dist")

    fig_app_dist = px.bar(
        df_user_dist.sort_values("total_app_opens", ascending=False).head(10),
        x="district",
        y="total_app_opens",
        color="state",
        title="Top 10 Districts by App Opens"
    )
    fig_app_dist.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_app_dist, use_container_width=True, key="eng_app_dist")

    st.markdown("---")

    # --- Top Registration Pincodes (top_user) ---
    st.markdown("### 🔹 Top Registration Hotspots (Pincodes)")

    df_top_reg = run_query("""
        SELECT
            parent_state AS state,
            entity_name  AS pincode,
            SUM(registered_users) AS total_registrations
        FROM top_user
        WHERE entity_type = 'pincode'
        GROUP BY parent_state, entity_name
        ORDER BY total_registrations DESC;
    """)

    fig_top_pins = px.bar(
        df_top_reg.head(10),
        x="pincode",
        y="total_registrations",
        color="state",
        title="Top 10 Pincodes by User Registrations"
    )
    st.plotly_chart(fig_top_pins, use_container_width=True, key="eng_top_pins")