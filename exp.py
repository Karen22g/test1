#Example 1
import streamlit as st
import plotly.express as px
import pandas as pd

# Title of the app
st.title("Streamlit Dashboard with Plotly")

# Sample data
data = {
    "Category": ["A", "B", "C", "D"],
    "Values": [10, 20, 15, 25]
}
df = pd.DataFrame(data)

# Create a bar chart
fig = px.bar(df, x="Category", y="Values", title="Sample Bar Chart")

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)

# Load Sample Data
df = px.data.gapminder()

# Title
st.title("Interactive Dashboard with Streamlit & Plotly")

# Select Year with Slider
year = st.slider("Select Year:", int(df["year"].min()), int(df["year"].max()), int(df["year"].min()), step =5)

# Filter Data
filtered_df = df[df.year == year]

# Create Plotly Scatter Plot
fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=60)

# Display Plot
st.plotly_chart(fig)
