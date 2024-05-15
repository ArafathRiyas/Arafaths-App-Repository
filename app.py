import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned dataset
df = pd.read_excel("Global Superstore lite.xlsx")

# Sidebar for filtering
st.sidebar.title('Filter Data')
selected_category = st.sidebar.selectbox("Select Category", ['All'] + list(df["Category"].unique()))
selected_segment = st.sidebar.selectbox("Select Segment", ['All'] + list(df["Segment"].unique()))
selected_country = st.sidebar.selectbox("Select Country", ['All'] + list(df["Country"].unique()))

# Filter the data based on the selections
filtered_data = df.copy()
if selected_category != 'All':
    filtered_data = filtered_data[filtered_data["Category"] == selected_category]
if selected_segment != 'All':
    filtered_data = filtered_data[filtered_data["Segment"] == selected_segment]
if selected_country != 'All':
    filtered_data = filtered_data[filtered_data["Country"] == selected_country]

# Organize the visualizations
st.title('Sales and Profit Analysis')

# Visualization 01 & 02- Sum of sales and profit
selected_year = st.selectbox("Select Year", ['All'] + list(df["Order Date"].dt.year.unique()))

# setting up filter so you could see sales and profit for each year
if selected_year != 'All':
    filtered_df = df[df["Order Date"].dt.year == selected_year]
else:
    filtered_df = df

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
col1, col2 = st.columns(2)

with col1:
    st.subheader('Total Sales')
    st.metric(label="Sales", value=f"${total_sales:,.0f}", delta=None)

with col2:
    st.subheader('Total Profit')
    st.metric(label="Profit", value=f"${total_profit:,.0f}", delta=None)

# Sales vs. Discount Scatter Plot
st.header('Sales vs. Discount Analysis')
fig = px.scatter(filtered_data, x='Discount', y='Sales', color='Category', title=f'Sales vs. Discount for {selected_category}',
                 labels={'Discount': 'Discount (%)', 'Sales': 'Sales ($)'},
                 template='plotly_dark')  # Change the template for a dark theme
st.plotly_chart(fig)

# Total Sales by Category (Bar Chart)
st.header('Total Sales by Category')
total_sales_category = filtered_data.groupby('Category')['Sales'].sum().reset_index()
fig = px.bar(total_sales_category, x='Category', y='Sales', title='Total Sales by Category',
             labels={'Category': 'Product Category', 'Sales': 'Total Sales ($)'},
             color='Sales',  # Color by Sales for differentiation
             color_continuous_scale='Blues')  # Change the color scale
st.plotly_chart(fig)

# Top 5 Products by Sales
st.header('Top 5 Products by Sales')
top_products = filtered_data.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
fig = px.bar(top_products, x='Sales', y='Product Name', orientation='h', title='Top 5 Products by Sales',
             labels={'Product Name': 'Product', 'Sales': 'Total Sales ($)'},
             color='Sales',  # Color by Sales for differentiation
             color_continuous_scale='Blues')  # Change the color scale
st.plotly_chart(fig)

# Sales Trends Over Time (Line Chart)
st.header('Sales Trends Over Time')
filtered_data['Order Date'] = pd.to_datetime(filtered_data['Order Date'])
sales_trends = filtered_data.groupby(filtered_data['Order Date'].dt.to_period("M"))['Sales'].sum().reset_index()
sales_trends['Order Date'] = sales_trends['Order Date'].astype(str)  # Convert period index to string
fig = px.line(sales_trends, x='Order Date', y='Sales', title='Sales Trends Over Time',
              labels={'Order Date': 'Date', 'Sales': 'Total Sales ($)'},
              template='plotly_dark')  # Change the template for a dark theme
st.plotly_chart(fig)

# Profit by Market and Segment (Bar Chart)
st.header('Profit by Market and Segment')
profit_market_segment = filtered_data.groupby(['Market', 'Segment'])['Profit'].sum().reset_index()
fig = px.bar(profit_market_segment, x='Market', y='Profit', color='Segment', title='Profit by Market and Segment',
             labels={'Profit': 'Total Profit ($)'},
             barmode='group', template='plotly_dark')  # Change the template for a dark theme
st.plotly_chart(fig)

# Distribution of Sales by Ship Mode (Pie Chart)
st.header('Distribution of Sales by Ship Mode')
sales_by_ship_mode = filtered_data.groupby('Ship Mode')['Sales'].sum().reset_index()
fig = px.pie(sales_by_ship_mode, values='Sales', names='Ship Mode', title='Sales Distribution by Ship Mode')
st.plotly_chart(fig)

# Distribution of Sales by Region (Bar Chart)
st.header('Distribution of Sales by Region')
sales_by_region = filtered_data.groupby('Region')['Sales'].sum().reset_index()
fig = px.bar(sales_by_region, x='Region', y='Sales', title='Sales Distribution by Region',
             labels={'Region': 'Region', 'Sales': 'Total Sales ($)'},
             color='Sales',  # Color by Sales for differentiation
             color_continuous_scale='Blues')  # Change the color scale
st.plotly_chart(fig)

# Distribution of Profit by Category (Pie Chart)
st.header('Distribution of Profit by Category')
profit_by_category = filtered_data.groupby('Category')['Profit'].sum().reset_index()
fig = px.pie(profit_by_category, values='Profit', names='Category', title='Profit Distribution by Category')
st.plotly_chart(fig)
