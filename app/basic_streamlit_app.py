import pandas as pd
import streamlit as st

# Sample data generation (replace with your actual data source)
fake_data = {
    "Time": pd.date_range(start="2023-11-01", end="2023-11-13", freq="D"),
    "Passengers": [
        10,
        15,
        20,
        25,
        30,
        28,
        22,
        18,
        15,
        12,
        10,
        8,
        7,
    ],
}
fake_df = pd.DataFrame(fake_data)


# Display markdown text
st.markdown("# Bus Affluence Analysis")
st.markdown(
    "This app displays the average number of passengers on buses throughout November 2023."
)

# Generate and display the graph
st.line_chart(fake_df.set_index("Time")["Passengers"])

# Additional information (optional)
st.markdown(
    """**Note:** This is a sample application with generated data.
    Replace this with your actual data source.
    You may want to check databricks ('dbx') template to use functionalities
    about loading data from databricks.
    """
)
