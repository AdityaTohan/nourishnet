import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to load data from CSV files
@st.cache_data
def load_data(file_path1, file_path2):
    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)
    return df1, df2

# Main function to create UI and plot graph
def main():
    st.title("Correlation Analysis")

    # Update the file paths below
    file_path1 = "data1.csv"  # Update with the file path for Table 1
    file_path2 = "data2.csv"  # Update with the file path for Table 2

    # Load data from CSV files
    df1, df2 = load_data(file_path1, file_path2)

    # Sidebar for user input
    st.sidebar.title("Filter Options")
    selected_countries = st.sidebar.multiselect("Select Countries", df1['Country Name'].unique())
    selected_gender = st.sidebar.selectbox("Select Gender", df1['Sex'].unique())
    selected_nutrition = st.sidebar.multiselect("Select Nutrition", df2['Nutrition'].unique())
    selected_y_axis = st.sidebar.selectbox("Select Y-axis from Table 1", df1.columns, index=5)  # Default to 'Mean' for y-axis from Table 1

    # Filter data based on user selection
    filtered_df1 = df1[(df1['Country Name'].isin(selected_countries)) & (df1['Sex'] == selected_gender)]
    filtered_df2 = df2[(df2['Country Name'].isin(selected_countries)) & (df2['Sex'] == selected_gender)]

    # Plot graph
    if not filtered_df1.empty:
        fig = go.Figure()

        # Add lines for Table 1
        for country in selected_countries:
            temp_df1 = filtered_df1[filtered_df1['Country Name'] == country]
            fig.add_trace(go.Scatter(x=temp_df1['Year'], y=temp_df1[selected_y_axis], mode='lines', name=f"{country} - Table 1"))

        # Add lines for Table 2 (mean)
        for nutrition in selected_nutrition:
            for country in selected_countries:
                temp_df2_country = filtered_df2[(filtered_df2['Country Name'] == country) & (filtered_df2['Nutrition'] == nutrition)]
                if not temp_df2_country.empty:
                    fig.add_trace(go.Scatter(x=temp_df2_country['Year'], y=temp_df2_country['Mean'], mode='lines', name=f"{country} - {nutrition} - Mean - Table 2", line=dict(dash='dot')))

        # Update layout for three-sided axis
        fig.update_layout(
            title=f"Malnutrition Trend for {selected_gender}s in Selected Countries",
            xaxis=dict(title="Year"),
            yaxis=dict(title=selected_y_axis, side='left'),
            yaxis2=dict(title='Mean - Table 2', side='right', overlaying='y'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig)
    else:
        st.warning(f"No data available for the selected {selected_gender}s in the selected countries.")

if __name__ == "__main__":
    main()
