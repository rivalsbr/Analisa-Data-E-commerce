import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# --- HELPER FUNCTIONS ---

def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%B %Y')
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return monthly_orders_df

def create_category_revenue_df(df):
    category_revenue_df = df.groupby("product_category").price.sum().sort_values(ascending=False).reset_index()
    return category_revenue_df

def create_delivery_rating_df(df):
    delivery_rating_df = df.groupby("delivery_status").review_score.mean().sort_values(ascending=False).reset_index()
    return delivery_rating_df

def create_rfm_df(df):
    recent_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": lambda x: (recent_date - x.max()).days,
        "order_id": "nunique",
        "price": "sum"
    })
    rfm_df.columns = ["customer_id", "recency", "frequency", "monetary"]
    return rfm_df

# --- LOAD DATA ---

main_df = pd.read_csv("product_sales.csv")
reviews_df = pd.read_csv("delivery_reviews.csv")

# Konversi datetime
main_df["order_purchase_timestamp"] = pd.to_datetime(main_df["order_purchase_timestamp"])
reviews_df["order_delivered_customer_date"] = pd.to_datetime(reviews_df["order_delivered_customer_date"])

# --- FILTER SIDEBAR ---
min_date = main_df["order_purchase_timestamp"].min()
max_date = main_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.header("E-Commerce Dashboard Filter")
    # Date Input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan pilihan tanggal
main_filtered_df = main_df[(main_df["order_purchase_timestamp"] >= str(start_date)) & 
                           (main_df["order_purchase_timestamp"] <= str(end_date))]

# Menyiapkan berbagai dataframe melalui helper functions
monthly_orders_df = create_monthly_orders_df(main_filtered_df)
category_revenue_df = create_category_revenue_df(main_filtered_df)
delivery_rating_df = create_delivery_rating_df(reviews_df) # Biasanya statis atau menyesuaikan dataset review
rfm_df = create_rfm_df(main_filtered_df)

# --- DASHBOARD UI ---
st.header('E-Commerce Performance Dashboard :sparkles:')

# Section 1: Monthly Revenue Trend
st.subheader('Monthly Revenue Trend')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df["order_purchase_timestamp"],
    monthly_orders_df["revenue"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Section 2: Product Performance
st.subheader('Top Categories by Revenue')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x="price", 
    y="product_category", 
    data=category_revenue_df.head(5), 
    palette="Blues_r",
    ax=ax
)
st.pyplot(fig)

# Section 3: Delivery Impact
st.subheader('Delivery Status vs Review Score')
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="delivery_status", 
    y="review_score", 
    data=delivery_rating_df, 
    palette="coolwarm",
    ax=ax
)
ax.set_ylim(0, 5)
st.pyplot(fig)

# Section 4: RFM Analysis (Top 5 Customers)
st.subheader('Best Customers Based on RFM Parameters')
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**By Recency (days)**")
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), color="#72BCD4", ax=ax)
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

with col2:
    st.write("**By Frequency**")
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), color="#72BCD4", ax=ax)
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

with col3:
    st.write("**By Monetary**")
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), color="#72BCD4", ax=ax)
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

st.caption('Copyright (c) Muhammad Rivaldi 2025')