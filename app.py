"""
Superstore Sales Dashboard
----------------------------
An interactive Streamlit dashboard for exploring retail sales data (2015-2018).
Allows filtering by region and visualizes sales trends, category performance,
regional performance, top products, customer segments, and shipping preferences.
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# =========================================================
# DATA LOADING & CLEANING
# =========================================================

# Load the raw dataset
df = pd.read_csv('Super store sales.csv')

# Convert date columns to datetime format (dates are in DD/MM/YYYY format)
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

# Extract year and month for time-based analysis
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month_name()

# =========================================================
# PAGE CONFIG & TITLE
# =========================================================

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")
st.title("Superstore Sales Dashboard")

# =========================================================
# SIDEBAR FILTER
# =========================================================

# Let the user filter the entire dashboard by region
region_list = ['All'] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox('Select Region', region_list)

# Apply the filter to a working copy of the data
filtered_df = df if selected_region == 'All' else df[df['Region'] == selected_region]

# =========================================================
# KPI CARDS (Top-level summary metrics)
# =========================================================

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")
col3.metric("Avg Order Value", f"${filtered_df['Sales'].mean():,.2f}")

st.divider()

# =========================================================
# HELPER FUNCTION: Applies consistent dark styling to every chart
# =========================================================

def style_dark(fig, ax):
    """Applies the dashboard's dark navy/teal theme to a matplotlib chart."""
    fig.patch.set_facecolor('#0A1420')
    ax.set_facecolor('#0A1420')
    ax.tick_params(colors='#8FA3B8')
    ax.xaxis.label.set_color('#8FA3B8')
    ax.yaxis.label.set_color('#8FA3B8')
    ax.title.set_color('#EEF2F5')
    for spine in ax.spines.values():
        spine.set_color('#3A4656')

# =========================================================
# ROW 1: Monthly Sales Trend | Sales by Category
# =========================================================

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Monthly Sales Trend")
    # Group total sales by month to see how sales change over time
    monthly_sales = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum()
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    monthly_sales.plot(kind='line', marker='o', color='#4DD6C4', ax=ax1)
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Total Sales')
    ax1.grid(True, alpha=0.2, color='#3A4656')
    style_dark(fig1, ax1)
    st.pyplot(fig1)

with row1_col2:
    st.subheader("Sales by Category")
    # Group total sales by category, sorted highest to lowest
    category_sales = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    category_sales.plot(kind='bar', color='#4DD6C4', ax=ax2)
    ax2.set_xlabel('Category')
    ax2.set_ylabel('Total Sales')
    plt.xticks(rotation=0)
    style_dark(fig2, ax2)
    st.pyplot(fig2)

# =========================================================
# ROW 2: Sales by Region | Top 10 Best-Selling Products
# =========================================================

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Sales by Region")
    # Group total sales by region, sorted highest to lowest
    region_sales = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    region_sales.plot(kind='bar', color='#8FA3B8', ax=ax3)
    ax3.set_xlabel('Region')
    ax3.set_ylabel('Total Sales')
    plt.xticks(rotation=0)
    style_dark(fig3, ax3)
    st.pyplot(fig3)

with row2_col2:
    st.subheader("Top 10 Best-Selling Products")
    # Group total sales by product, take the top 10
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    top_products.plot(kind='barh', color='#4DD6C4', ax=ax4)
    ax4.invert_yaxis()  # highest value on top
    ax4.set_xlabel('Total Sales')
    style_dark(fig4, ax4)
    st.pyplot(fig4)

# =========================================================
# ROW 3: Sales by Segment | Order Count by Ship Mode
# =========================================================

row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.subheader("Sales Share by Segment")
    # Group total sales by customer segment
    segment_sales = filtered_df.groupby('Segment')['Sales'].sum()
    fig5, ax5 = plt.subplots(figsize=(5, 5))
    fig5.patch.set_facecolor('#0A1420')
    wedges, texts, autotexts = ax5.pie(
        segment_sales,
        labels=segment_sales.index,
        autopct='%1.1f%%',
        colors=['#4DD6C4', '#8FA3B8', '#1A2C3D']
    )
    # Pie chart labels need their text color set separately
    for text in texts + autotexts:
        text.set_color('#EEF2F5')
    st.pyplot(fig5)

with row3_col2:
    st.subheader("Order Count by Ship Mode")
    # Count how many orders used each shipping mode
    ship_mode_counts = filtered_df['Ship Mode'].value_counts()
    fig6, ax6 = plt.subplots(figsize=(6, 4))
    ship_mode_counts.plot(kind='bar', color='#8FA3B8', ax=ax6)
    ax6.set_xlabel('Ship Mode')
    ax6.set_ylabel('Number of Orders')
    plt.xticks(rotation=15)
    style_dark(fig6, ax6)
    st.pyplot(fig6)
