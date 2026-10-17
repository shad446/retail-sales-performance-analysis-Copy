import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# RETAIL SALES PERFORMANCE | EXECUTIVE ANALYTICS DASHBOARD
# ---------------------------------------------------------
st.set_page_config(
    page_title="Retail Intelligence | Sales Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Luxury, readable palette — intentionally no red
NAVY = "#101A2B"
NAVY_2 = "#17263D"
GOLD = "#D6B56D"
IVORY = "#F4F0E6"
MUTED = "#AAB5C5"
TEAL = "#65C3B0"
BLUE = "#7FA6E8"
PURPLE = "#B6A0E8"
PANEL = "#172338"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    .stApp {{
        background: linear-gradient(135deg, {NAVY} 0%, #0B1220 100%);
        color: {IVORY};
        font-family: 'DM Sans', sans-serif;
    }}
    [data-testid="stSidebar"] {{
        background: #0C1422;
        border-right: 1px solid rgba(214,181,109,.22);
    }}
    [data-testid="stSidebar"] * {{ color: {IVORY}; }}
    h1, h2, h3 {{ font-family: 'Manrope', sans-serif !important; color: {IVORY} !important; }}
    h1 {{ letter-spacing: -1.2px; font-weight: 800 !important; }}
    p, label, .stCaption {{ color: {MUTED}; }}
    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, #1A2940, #131F32);
        border: 1px solid rgba(214,181,109,.24);
        border-radius: 15px;
        padding: 17px 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,.12);
    }}
    [data-testid="stMetricLabel"] {{ color: {MUTED} !important; font-size: .82rem; }}
    [data-testid="stMetricValue"] {{ color: {IVORY} !important; font-family: 'Manrope', sans-serif; }}
    div[data-testid="stDataFrame"] {{ border: 1px solid rgba(214,181,109,.22); border-radius: 12px; }}
    .hero {{
        padding: 25px 28px;
        border-radius: 18px;
        border: 1px solid rgba(214,181,109,.32);
        background: linear-gradient(110deg, #1B2A41 0%, #111C2D 70%, #202B3C 100%);
        margin-bottom: 20px;
    }}
    .eyebrow {{
        color: {GOLD}; text-transform: uppercase; letter-spacing: 2px;
        font-size: .72rem; font-weight: 700; margin-bottom: 8px;
    }}
    .hero-sub {{ color: {MUTED}; margin: 5px 0 0 0; font-size: .98rem; }}
    .section-note {{ color: {MUTED}; font-size: .84rem; margin-top: -8px; }}
    .insight {{
        background: #17263A; border-left: 3px solid {GOLD};
        padding: 13px 16px; border-radius: 8px; margin-bottom: 10px;
        color: {IVORY}; line-height: 1.5;
    }}
    .small-label {{ color: {GOLD}; font-size: .72rem; font-weight: 700; letter-spacing: 1.4px; }}
    hr {{ border-color: rgba(214,181,109,.2) !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Plotly chart defaults
CHART_TEMPLATE = "plotly_dark"
BASE_LAYOUT = dict(
    template=CHART_TEMPLATE,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color=IVORY),
    margin=dict(l=12, r=12, t=50, b=12),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
)

@st.cache_data
def load_data(file_path="Retail_Sales.csv", uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, encoding="latin1")
    else:
        data = pd.read_csv(file_path, encoding="latin1")

    # Normalize common date columns
    for col in ("Order Date", "Ship Date"):
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], errors="coerce")

    required = ["Sales", "Profit", "Quantity", "Order ID", "Customer ID",
                "Region", "Category", "Segment", "Product Name", "Order Date"]
    missing = [col for col in required if col not in data.columns]
    if missing:
        raise ValueError(
            "The dataset is missing these expected columns: "
            + ", ".join(missing)
            + ". Please check that you selected the Superstore retail sales CSV."
        )

    for col in ("Sales", "Profit", "Quantity", "Discount"):
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=["Order Date", "Sales", "Profit"])
    data["Year"] = data["Order Date"].dt.year
    data["Month Start"] = data["Order Date"].dt.to_period("M").dt.to_timestamp()
    return data

# Sidebar
st.sidebar.markdown(f"<div class='small-label'>RETAIL INTELLIGENCE</div>", unsafe_allow_html=True)
st.sidebar.title("Control Center")
st.sidebar.caption("Choose filters to explore the business.")
uploaded = st.sidebar.file_uploader("Optional: upload your retail CSV", type=["csv"])

try:
    df = load_data(uploaded_file=uploaded)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.info("Keep `Retail_Sales.csv` in the same folder as `dashboard.py`, or upload the CSV using the sidebar.")
    st.stop()

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

regions = sorted(df["Region"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())
segments = sorted(df["Segment"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Product category", categories, default=categories)
selected_segments = st.sidebar.multiselect("Customer segment", segments, default=segments)

if "Sub-Category" in df.columns:
    subcategories = sorted(df["Sub-Category"].dropna().unique().tolist())
    selected_subcategories = st.sidebar.multiselect("Sub-category", subcategories, default=subcategories)
else:
    selected_subcategories = None

if "State" in df.columns:
    states = sorted(df["State"].dropna().unique().tolist())
    selected_states = st.sidebar.multiselect("State", states, default=states)
else:
    selected_states = None

filtered = df[
    df["Order Date"].dt.date.between(start_date, end_date)
    & df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
    & df["Segment"].isin(selected_segments)
].copy()

if selected_subcategories is not None:
    filtered = filtered[filtered["Sub-Category"].isin(selected_subcategories)]
if selected_states is not None:
    filtered = filtered[filtered["State"].isin(selected_states)]

# Header
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Executive analytics · Project 01</div>
      <h1 style="margin:0;">Retail Sales Performance</h1>
      <p class="hero-sub">A decision-ready view of revenue, profitability, customer segments and product performance.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(
    f"Reporting window: {start_date:%d %b %Y} – {end_date:%d %b %Y}  ·  "
    f"{len(filtered):,} transaction rows in current selection"
)

if filtered.empty:
    st.warning("No records match these filters. Widen the date range or select more regions, categories or segments.")
    st.stop()

# KPI calculations
sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
quantity = filtered["Quantity"].sum()
orders = filtered["Order ID"].nunique()
customers = filtered["Customer ID"].nunique()
aov = sales / orders if orders else 0
margin = (profit / sales * 100) if sales else 0
profit_per_order = profit / orders if orders else 0

st.markdown("### Executive snapshot")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total sales", f"${sales:,.0f}")
k2.metric("Total profit", f"${profit:,.0f}")
k3.metric("Profit margin", f"{margin:.1f}%")
k4.metric("Unique orders", f"{orders:,}")

k5, k6, k7, k8 = st.columns(4)
k5.metric("Customers", f"{customers:,}")
k6.metric("Units sold", f"{quantity:,.0f}")
k7.metric("Average order value", f"${aov:,.2f}")
k8.metric("Profit per order", f"${profit_per_order:,.2f}")

st.divider()

# Trends
st.markdown("### 01 · Revenue & profitability trend")
st.markdown("<p class='section-note'>Track monthly performance across the selected period.</p>", unsafe_allow_html=True)
monthly = (
    filtered.groupby("Month Start", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
    .sort_values("Month Start")
)
trend_left, trend_right = st.columns([1.65, 1])
with trend_left:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month Start"], y=monthly["Sales"], name="Sales",
        mode="lines+markers", line=dict(color=GOLD, width=3),
        marker=dict(size=6), hovertemplate="%{x|%b %Y}<br>Sales: $%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=monthly["Month Start"], y=monthly["Profit"], name="Profit",
        mode="lines+markers", line=dict(color=TEAL, width=2.5),
        marker=dict(size=5), hovertemplate="%{x|%b %Y}<br>Profit: $%{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(**BASE_LAYOUT, height=360, yaxis_title="Amount ($)", xaxis_title="", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
with trend_right:
    fig = px.bar(
        monthly, x="Month Start", y="Orders", title="Monthly order volume",
        text_auto=".2s", color_discrete_sequence=[BLUE]
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(**BASE_LAYOUT, height=360, xaxis_title="", yaxis_title="Unique orders")
    st.plotly_chart(fig, use_container_width=True)

# Mix and geography
st.markdown("### 02 · Where performance comes from")
mix_left, mix_right = st.columns(2)
with mix_left:
    region_perf = filtered.groupby("Region", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    region_perf = region_perf.sort_values("Sales", ascending=True)
    fig = px.bar(
        region_perf, x="Sales", y="Region", orientation="h", title="Sales by region",
        text=region_perf["Sales"].map(lambda x: f"${x:,.0f}"),
        color="Sales", color_continuous_scale=[[0, "#49617D"], [1, GOLD]]
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(**BASE_LAYOUT, height=330, xaxis_title="Sales ($)", yaxis_title="", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
with mix_right:
    cat_perf = filtered.groupby("Category", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Sales", x=cat_perf["Category"], y=cat_perf["Sales"], marker_color=GOLD,
                         hovertemplate="%{x}<br>Sales: $%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Bar(name="Profit", x=cat_perf["Category"], y=cat_perf["Profit"], marker_color=TEAL,
                         hovertemplate="%{x}<br>Profit: $%{y:,.0f}<extra></extra>"))
    fig.update_layout(**BASE_LAYOUT, barmode="group", height=330, title="Sales vs profit by category",
                      xaxis_title="", yaxis_title="Amount ($)")
    st.plotly_chart(fig, use_container_width=True)

# Product and customer analysis
st.markdown("### 03 · Product & customer performance")
prod_left, prod_right = st.columns(2)
with prod_left:
    products = filtered.groupby("Product Name", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    top_products = products.nlargest(10, "Sales").sort_values("Sales", ascending=True)
    fig = px.bar(
        top_products, x="Sales", y="Product Name", orientation="h", title="Top 10 products by sales",
        text=top_products["Sales"].map(lambda x: f"${x:,.0f}"),
        color_discrete_sequence=[GOLD]
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(**BASE_LAYOUT, height=430, xaxis_title="Sales ($)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with prod_right:
    seg_perf = filtered.groupby("Segment", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"), Customers=("Customer ID", "nunique")
    )
    fig = px.pie(
        seg_perf, names="Segment", values="Sales", hole=.62, title="Sales mix by customer segment",
        color_discrete_sequence=[GOLD, TEAL, BLUE]
    )
    fig.update_traces(textposition="inside", textinfo="label+percent", marker=dict(line=dict(color=NAVY, width=2)))
    fig.update_layout(**BASE_LAYOUT, height=430, legend_title_text="Segment")
    st.plotly_chart(fig, use_container_width=True)

# Discount analysis and underperformers
st.markdown("### 04 · Profitability diagnostics")
diag_left, diag_right = st.columns(2)
with diag_left:
    if "Discount" in filtered.columns:
        disc = filtered.groupby("Discount", as_index=False).agg(
            Average_Profit=("Profit", "mean"), Sales=("Sales", "sum"), Rows=("Profit", "size")
        ).sort_values("Discount")
        disc["Discount label"] = disc["Discount"].map(lambda x: f"{x:.0%}")
        fig = px.bar(
            disc, x="Discount label", y="Average_Profit", title="Average profit at each discount level",
            text=disc["Average_Profit"].map(lambda x: f"${x:,.2f}"),
            color="Average_Profit", color_continuous_scale=[[0, "#60748C"], [1, TEAL]]
        )
        fig.add_hline(y=0, line_dash="dot", line_color=MUTED, opacity=.7)
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(**BASE_LAYOUT, height=350, xaxis_title="Discount", yaxis_title="Average profit ($)", coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("This dataset has no Discount column, so discount analysis is unavailable.")
with diag_right:
    loss_products = products[products["Profit"] < 0].nsmallest(10, "Profit").sort_values("Profit")
    if loss_products.empty:
        st.success("No loss-making products appear in the current selection.")
    else:
        fig = px.bar(
            loss_products, x="Profit", y="Product Name", orientation="h",
            title="Products with the largest total losses",
            text=loss_products["Profit"].map(lambda x: f"-${abs(x):,.0f}"),
            color_discrete_sequence=[PURPLE]
        )
        fig.add_vline(x=0, line_dash="dot", line_color=MUTED, opacity=.7)
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(**BASE_LAYOUT, height=350, xaxis_title="Profit ($)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

# Automatically generated insights
st.markdown("### 05 · Business insights")
insights = []
best_region = region_perf.sort_values("Sales", ascending=False).iloc[0]
best_cat = cat_perf.sort_values("Sales", ascending=False).iloc[0]
best_profit_cat = cat_perf.sort_values("Profit", ascending=False).iloc[0]
insights.append(f"**Leading region:** {best_region['Region']} generates the most sales in this selection (${best_region['Sales']:,.0f}).")
insights.append(f"**Sales leader:** {best_cat['Category']} is the highest-revenue category (${best_cat['Sales']:,.0f}).")
insights.append(f"**Profit leader:** {best_profit_cat['Category']} contributes the highest total profit (${best_profit_cat['Profit']:,.0f}).")
if not loss_products.empty:
    worst = loss_products.iloc[0]
    insights.append(f"**Priority review:** {worst['Product Name']} has the largest product-level loss (${abs(worst['Profit']):,.0f}); investigate discounting, cost and pricing.")
if "Discount" in filtered.columns and filtered["Discount"].nunique() > 1:
    low_disc = filtered.groupby("Discount")["Profit"].mean()
    low_disc_level = low_disc.idxmin()
    insights.append(f"**Discount watch:** the lowest average profit occurs at a {low_disc_level:.0%} discount level. Review margin impact before expanding promotions.")
for insight in insights:
    st.markdown(f"<div class='insight'>{insight}</div>", unsafe_allow_html=True)

# Data table and export
with st.expander("Explore transaction-level data", expanded=False):
    search = st.text_input("Search within visible rows (product, customer, order, region)", "")
    display_df = filtered.copy()
    if search.strip():
        mask = display_df.astype(str).apply(lambda col: col.str.contains(search.strip(), case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    st.caption(f"{len(display_df):,} matching rows")
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=360)
    st.download_button(
        "Download filtered data (CSV)",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="retail_sales_filtered.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown("---")
st.markdown(
    f"<p style='text-align:center;color:{MUTED};font-size:.78rem;'>RETAIL INTELLIGENCE · Executive dashboard · Built with Streamlit & Plotly</p>",
    unsafe_allow_html=True,
)
