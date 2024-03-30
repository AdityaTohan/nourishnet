import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import openai

# Function to load data from CSV files
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Main function to create UI and plot graph
def main():
    st.title("Malnutrition Analysis")

    # Update the file path below
    file_path = "data2.csv"  # Update with the file path for Table 2

    # Load data from CSV file
    df = load_data(file_path)

    # Sidebar for user input
    st.sidebar.title("Filter Options")
    selected_countries = st.sidebar.multiselect("Select Countries", df['Country Name'].unique())
    gender_mapping = {0: "Male", 1: "Female", 999: "Both"}
    selected_gender = st.sidebar.selectbox("Select Gender", [gender_mapping[gender_code] for gender_code in sorted(df['Sex'].unique())])
    selected_nutrition = st.sidebar.multiselect("Select Nutrition", df['Nutrition'].unique())

    # Filter data based on user selection
    filtered_df = df[(df['Country Name'].isin(selected_countries)) & (df['Sex'] == list(gender_mapping.keys())[list(gender_mapping.values()).index(selected_gender)])]

    # Plot graph
    if not filtered_df.empty:
        fig = go.Figure()

        # Add lines for Table 2 (mean)
        for nutrition in selected_nutrition:
            for country in selected_countries:
                temp_df_country = filtered_df[(filtered_df['Country Name'] == country) & (filtered_df['Nutrition'] == nutrition)]
                if not temp_df_country.empty:
                    fig.add_trace(go.Scatter(x=temp_df_country['Year'], y=temp_df_country['Mean'], mode='lines', name=f"{country} - {nutrition} - Mean - Table 2"))

        # Update layout
        fig.update_layout(
            title=f"Malnutrition Trend for {selected_gender}s in Selected Countries",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Mean - Table 2"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig)

        # Analyse button
        if st.button("Analyse"):
            # Get the graph as a string
            graph_str = fig.to_html(full_html=False, include_plotlyjs='cdn')

            # Send graph data to OpenAI API and receive analysis
            openai.api_key = ""
            response = openai.Completion.create(
                engine="davinci",
                prompt=graph_str,
                temperature=0.5,
                max_tokens=150
            )

            # Display analysis below the graph
            st.subheader("Analysis")
            st.write(response.choices[0].text)

    else:
        st.warning(f"No data available for the selected {selected_gender}s in the selected countries.")

if __name__ == "__main__":
    main()
