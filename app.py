import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load the cleaned dataset
df = pd.read_excel("Global Superstore lite.xlsx")

# Title
st.title('Minger Analysis Dashboard')
st.markdown("---")
st.markdown("")  # Add some space

# Filter for selecting years (affecting only total profit)
selected_year = st.sidebar.selectbox("Select Year", ['All'] + sorted(df['Order Date'].dt.year.unique()))

# Filter data by selected year
if selected_year == 'All':
    filtered_df = df
else:
    filtered_df = df[df['Order Date'].dt.year == selected_year]

# Main Metrics Section (Total Sales and Profit)
st.header('Total Sales and Profit')
st.markdown("")  # Add some space

# Calculate total sales and profit for the selected year
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()

# Display total sales and profit side by side
col1, col2 = st.columns(2)
with col1:
    st.write("Total Sales")
    st.write(f"${total_sales:,.2f}", font_size=20)

with col2:
    st.write("Total Profit")
    st.write(f"${total_profit:,.2f}", font_size=20)

st.markdown("---")

# Sales vs. Discount Analysis
st.header('Sales vs. Discount Analysis')
selected_category_sales_discount = st.selectbox("Select Category for Sales vs. Discount", ['All'] + list(filtered_df["Category"].unique()))
filtered_data_sales_discount = filtered_df.copy()
if selected_category_sales_discount != 'All':
    filtered_data_sales_discount = filtered_data_sales_discount[filtered_data_sales_discount["Category"] == selected_category_sales_discount]

fig_sales_discount = px.scatter(filtered_data_sales_discount, x='Discount', y='Profit', color='Category', title='Sales vs. Discount Analysis',
                 labels={'Discount': 'Discount (%)', 'Profit': 'Profit ($)'},
                 width=800, height=500)  # Adjusted plot size
fig_sales_discount.update_layout(showlegend=True)  # Show legend
st.plotly_chart(fig_sales_discount)

# Total Sales by Category (Pie Chart)
total_sales_category = filtered_df.groupby('Category')['Profit'].sum().reset_index()
fig_total_sales_category = px.pie(total_sales_category, values='Profit', names='Category', title='Total Sales by Category', width=600, height=400)  # Adjusted plot size
st.plotly_chart(fig_total_sales_category)

# Top Products by Sales or Profit (Bar Graph)
st.header('Top Products')

# Product Selector
top_products_metric = st.selectbox("Select Top Products by", ('Sales', 'Profit'))

# Filter Data
top_products_data = filtered_df.groupby('Product Name')[top_products_metric].sum().nlargest(10).reset_index()
# Truncate long product names even further
top_products_data['Product Name'] = top_products_data['Product Name'].apply(lambda x: x[:15] + '...' if len(x) > 15 else x)

fig_top_products = go.Figure()

fig_top_products.add_trace(go.Bar(
    x=top_products_data['Product Name'],  # Set product names on x-axis
    y=top_products_data[top_products_metric],
    marker=dict(color='#636EFA'),  # Set color
))

fig_top_products.update_layout(
    title=f'Top 10 Products by {top_products_metric}',
    xaxis=dict(title='Product Name', automargin=True),  # Adjust margin automatically
    yaxis=dict(title=f'Total {top_products_metric} ($)'),
    margin=dict(l=50, r=50, t=100, b=50),  # Adjust margins
    width=800,  # Set figure width
    showlegend=False,  # Hide legend
    xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    xaxis_showgrid=True,  # Show grid lines
    yaxis_showgrid=True,
)

st.plotly_chart(fig_top_products)

# Region-wise Analysis by Sales or Profit (Bar Graph)
st.header('Region-wise Analysis')

# Region Selector
region_metric = st.selectbox("Select Region by", ('Sales', 'Profit'))

# Filter Data
region_data = filtered_df.groupby('Region')[region_metric].sum().nlargest(10).reset_index()

fig_region = go.Figure()

fig_region.add_trace(go.Bar(
    x=region_data['Region'],  # Set region names on x-axis
    y=region_data[region_metric],
    marker=dict(color='#FFA07A'),  # Set color
))

fig_region.update_layout(
    title=f'Top 10 Regions by {region_metric}',
    xaxis=dict(title='Region', automargin=True),  # Adjust margin automatically
    yaxis=dict(title=f'Total {region_metric} ($)'),
    margin=dict(l=50, r=50, t=100, b=50),  # Adjust margins
    width=800,  # Set figure width
    showlegend=False,  # Hide legend
    xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    xaxis_showgrid=True,  # Show grid lines
    yaxis_showgrid=True,
)

st.plotly_chart(fig_region)

# Geographic Distribution of Orders and Sales
st.header('Geographic Distribution')

# Choose between Sales and Orders
geo_metric = st.selectbox("Select Metric", ('Sales', 'Orders'))

# Group data by Country
geographic_data = filtered_df.groupby("Country").agg({'Sales': 'sum', 'Row ID': 'count'}).reset_index()
geographic_data.columns = ['Country', 'Sales', 'Orders']

# Plot geographic map
fig_geo_map = px.choropleth(geographic_data, locations="Country", locationmode='country names', 
                             color=geo_metric, hover_name="Country", 
                             color_continuous_scale='Blues', title=f"{geo_metric} by Country", width=900, height=500)  # Adjusted plot size
fig_geo_map.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))  # Transparent background
st.plotly_chart(fig_geo_map)

# Time Series Analysis of Sales
st.header('Time Series Analysis of Sales')
time_series_data = filtered_df.groupby(pd.Grouper(key='Order Date', freq='M')).agg({'Profit': 'sum'}).reset_index()

min_date = time_series_data['Order Date'].min()
max_date = time_series_data['Order Date'].max()

date_range = st.slider("Select Date Range", min_value=min_date.to_pydatetime(), 
                       max_value=max_date.to_pydatetime(), value=(min_date.to_pydatetime(), max_date.to_pydatetime()))

filtered_time_series_data = time_series_data[(time_series_data['Order Date'] >= pd.to_datetime(date_range[0])) & 
                                             (time_series_data['Order Date'] <= pd.to_datetime(date_range[1]))]

fig_time_series = px.line(filtered_time_series_data, x='Order Date', y='Profit', title='Time Series Analysis of Sales',
                          labels={'Order Date': 'Date', 'Profit': 'Profit ($)'},
                          width=900, height=500)  # Adjusted plot size
fig_time_series.update_layout(xaxis_showgrid=True, yaxis_showgrid=True)  # Show grid lines
st.plotly_chart(fig_time_series)

# Shipping Mode Distribution
st.header('Shipping Mode Distribution')

# Count the number of orders for each shipping mode
shipping_mode_counts = filtered_df['Ship Mode'].value_counts()

# Plot pie chart
fig_shipping_mode = px.pie(names=shipping_mode_counts.index, values=shipping_mode_counts.values, 
                           title='Shipping Mode Distribution', width=600, height=400)
fig_shipping_mode.update_traces(marker=dict(colors=['#FFA07A', '#98FB98', '#87CEEB', '#FFD700']))  # Set marker colors
st.plotly_chart(fig_shipping_mode)