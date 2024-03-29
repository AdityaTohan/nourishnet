import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt  # Importing matplotlib for plotting

# Function to load data from CSV file
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Main function to create UI and plot graphs
def main():
    st.title("Malnutrition Analysis")

    # Update the file path below
    file_path = "data1.csv"  # Update with the file path for Table 1

    # Load data from CSV file
    df = load_data(file_path)

    # Sidebar for user input
    st.sidebar.title("Filter Options")
    selected_countries = st.sidebar.multiselect("Select Countries", df['Country Name'].unique())
    selected_gender = st.sidebar.selectbox("Select Gender", df['Sex'].unique())
    selected_y_axis = st.sidebar.selectbox("Select Y-axis", ['Overweight', 'Stunting', 'Wasting', 'Mean'], index=3)  # Default to 'Mean' for y-axis

    # Filter data based on user selection
    filtered_df = df[(df['Country Name'].isin(selected_countries)) & (df['Sex'] == selected_gender)]

    # Plot dynamic graph
    st.header("Dynamic Analysis Graph")
    if not filtered_df.empty:
        fig = go.Figure()

        # Add lines for Table 1
        for country in selected_countries:
            temp_df = filtered_df[filtered_df['Country Name'] == country]
            fig.add_trace(go.Scatter(x=temp_df['Year'], y=temp_df[selected_y_axis], mode='lines', name=f"{country}"))

        # Update layout
        fig.update_layout(
            title=f"Malnutrition Trend for {selected_gender}s in Selected Countries",
            xaxis=dict(title="Year"),
            yaxis=dict(title=selected_y_axis),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig)
    else:
        st.warning(f"No data available for the selected {selected_gender}s in the selected countries.")
    
    st.empty()
    # Plot static bar graphs
    st.header("Global Malnutrition Analysis")
    st.subheader("Histograms of Malnutrition Indicators")

    with plt.style.context("dark_background"):  # Use dark background style for static graphs
        fig, axis = plt.subplots(2,2)
        fig.suptitle("World's Children Malnutrition Histogram", fontsize=20)

        axis[0,0].hist(df['Mean'], bins=50, color='lightblue', alpha=0.7, edgecolor='black')
        axis[0,0].set_xlabel('Mean Malnutrition Percentage', fontsize=14)
        axis[0,0].set_ylabel('Number of Countries')

        axis[0,1].hist(df['Overweight'], bins=50, color='lightgreen', alpha=0.7, edgecolor='black')
        axis[0,1].set_xlabel('Overweight Percentage', fontsize=14)
        axis[0,1].set_ylabel('Number of Countries')

        axis[1,0].hist(df['Wasting'], bins=50, color='lightcoral', alpha=0.7, edgecolor='black')
        axis[1,0].set_xlabel('Wasting Percentage', fontsize=14)
        axis[1,0].set_ylabel('Number of Countries')

        axis[1,1].hist(df['Stunting'], bins=50, color='lightskyblue', alpha=0.7, edgecolor='black')
        axis[1,1].set_xlabel('Stunting Percentage', fontsize=14)
        axis[1,1].set_ylabel('Number of Countries')

        fig.set_size_inches(15, 10)
        st.pyplot(fig)

    # Plot the fifth static graph in a separate component
    st.empty()
    st.empty()
    
    st.subheader("Combined Global Malnutrition Analysis Histogram")

    with plt.style.context("dark_background"):  # Use darkroyalblue style for static graphs
        fig, ax = plt.subplots()
        ax.hist(df['Overweight'], bins=30, color='lightblue', alpha=0.5, label='Overweight', edgecolor='black')
        ax.hist(df['Stunting'], bins=30, color='royalblue', alpha=0.5, label='Stunting', edgecolor='black')
        ax.hist(df['Wasting'], bins=30, color='orange', alpha=0.5, label='Wasting', edgecolor='black')
        ax.hist(df['Mean'], bins=30, color='forestgreen', alpha=0.5, label='Mean', edgecolor='black')
        ax.set_xlabel('Percentage', fontsize=14)
        ax.set_ylabel('Number of Countries', fontsize=16)

        ax.legend()
        fig.set_size_inches(15, 10)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
