import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ---- Load raw data and clean it ----
df = pd.read_csv('Super store sales.csv')

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month_name()

# ---- Dashboard title ----
st.title("Superstore Sales Dashboard")

# ---- Sidebar filter ----
region_list = ['All'] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox('Select Region', region_list)

filtered_df = df if selected_region == 'All' else df[df['Region'] == selected_region]

# ---- KPI cards ----
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")
col3.metric("Avg Order Value", f"${filtered_df['Sales'].mean():,.2f}")

st.divider()

# ---- Q1: Monthly sales trend ----
st.subheader("Q1: Monthly Sales Trend")
monthly_sales = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum()
fig1, ax1 = plt.subplots(figsize=(10, 4))
monthly_sales.plot(kind='line', marker='o', color='teal', ax=ax1)
ax1.set_xlabel('Month')
ax1.set_ylabel('Total Sales')
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

# ---- Q2: Category-wise sales ----
st.subheader("Q2: Sales by Category")
category_sales = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(8, 4))
category_sales.plot(kind='bar', color='#4dd6c4', ax=ax2)
ax2.set_xlabel('Category')
ax2.set_ylabel('Total Sales')
plt.xticks(rotation=0)
st.pyplot(fig2)

# ---- Q3: Region-wise sales ----
st.subheader("Q3: Sales by Region")
region_sales = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
fig3, ax3 = plt.subplots(figsize=(7, 4))
region_sales.plot(kind='bar', color='#3a4656', ax=ax3)
ax3.set_xlabel('Region')
ax3.set_ylabel('Total Sales')
plt.xticks(rotation=0)
st.pyplot(fig3)

# ---- Q4: Top 10 best-selling products ----
st.subheader("Q4: Top 10 Best-Selling Products")
top_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
fig4, ax4 = plt.subplots(figsize=(8, 5))
top_products.plot(kind='barh', color='#4dd6c4', ax=ax4)
ax4.invert_yaxis()
ax4.set_xlabel('Total Sales')
st.pyplot(fig4)

# ---- Q5: Segment-wise sales ----
st.subheader("Q5: Sales Share by Customer Segment")
segment_sales = filtered_df.groupby('Segment')['Sales'].sum()
fig5, ax5 = plt.subplots(figsize=(6, 6))
ax5.pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%',
        colors=['#4dd6c4', '#8fa3b8', '#0a1420'])
st.pyplot(fig5)

# ---- Q6: Ship mode usage ----
st.subheader("Q6: Order Count by Ship Mode")
ship_mode_counts = filtered_df['Ship Mode'].value_counts()
fig6, ax6 = plt.subplots(figsize=(7, 4))
ship_mode_counts.plot(kind='bar', color='#8fa3b8', ax=ax6)
ax6.set_xlabel('Ship Mode')
ax6.set_ylabel('Number of Orders')
plt.xticks(rotation=15)
st.pyplot(fig6)