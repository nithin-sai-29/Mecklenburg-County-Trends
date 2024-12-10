import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

# Load Datasets
education_data = pd.read_csv("Education.csv")
environment_data = pd.read_csv('Environment.csv')
geo_data = pd.read_csv('Geo.csv')
housing_data = pd.read_csv('Housing.csv')

# Merge datasets
combined_data = pd.merge(housing_data, education_data, on=["NPA", "data_year"], how="outer")
combined_data = pd.merge(combined_data, environment_data, on=["NPA", "data_year"], how="outer")

# Sidebar Navigation
st.sidebar.title("📊 Mecklenburg County Trends")
page = st.sidebar.radio(
    "Select a Section:",
    ["🏠 Home", "🏞 Environment Trends", "🎓 Education Trends", "🏠 Housing Trends"]
)

# Home Page
if page == "🏠 Home":
    st.title("📊 Mecklenburg County at a Glance: Trends in Environment, Education, and Housing")
    st.write("""
    Welcome to the Mecklenburg County Trends. This interactive application provides insights into 
    the key trends shaping the region, including environmental factors, education outcomes, 
    and housing developments.

    ### About This Dashboard:
    - Environment Trends: Explore how urbanization impacts water consumption, impervious surfaces, and community participation.
    - Education Trends: Discover the relationship between student absenteeism, academic proficiency, and high school graduation rates.
    - Housing Trends: Analyze housing density, foreclosure rates, and patterns in residential development.

    Use the navigation bar on the left to explore each section in detail. Each page includes interactive visualizations, 
    key metrics, and summaries of insights to help you better understand Mecklenburg County's evolving trends.
    """)

    st.subheader("🌿 Environment Trends")
    st.write("""
    Learn about the impact of urbanization and environmental programs, including water consumption patterns and community engagement.
    """)

    st.subheader("🎓 Education Trends")
    st.write("""
    Analyze trends in absenteeism, student performance, and graduation rates, which are key indicators of educational success.
    """)

    st.subheader("🏠 Housing Trends")
    st.write("""
    Explore housing density, foreclosure trends, and development patterns that reflect urban growth and economic conditions.
    """)

    # Footer
    st.write("""
    Navigate through the sections to uncover insights and visualize how *environment, education, and housing* trends are shaping Mecklenburg County.
    """)

# 1. Environment Trends
elif page == "🏞 Environment Trends":
    st.title("🌿 Environment Trends in Mecklenburg")
    st.write("""
    Explore environmental metrics such as community participation, water consumption, and impervious surfaces. 
    These trends help assess the sustainability and environmental challenges in Mecklenburg County.
    """)

    # Metrics Highlight
    avg_stream = combined_data['Adopt_a_Stream'].mean(skipna=True)
    avg_water = combined_data['Water_Consumption'].mean(skipna=True)
    st.write("### Key Environmental Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Avg 'Adopt a Stream'", f"{avg_stream:.2f}")
    col2.metric("Avg Water Consumption", f"{avg_water:.2f}")

    # Participation Bar Plot
    st.subheader("📈 Adopt a Stream Participation")
    df_stream = combined_data.dropna(subset=["Adopt_a_Stream"])
    avg_adopt_stream = df_stream.groupby("data_year")["Adopt_a_Stream"].mean().reset_index()
    plt.figure(figsize=(8, 4))
    sns.barplot(data=avg_adopt_stream, x="data_year", y="Adopt_a_Stream", color="skyblue")
    plt.title("Adopt a Stream Participation Over Years")
    plt.xlabel("Year")
    plt.ylabel("Average Participation")
    st.pyplot(plt)

    # Scatter Plot: Impervious Surface vs Water Consumption
    st.subheader("💧 Impervious Surface vs Water Consumption")
    scatter_data = combined_data.dropna(subset=["Impervious_Surface", "Water_Consumption"])
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=scatter_data, x="Impervious_Surface", y="Water_Consumption", alpha=0.6, color="green")
    plt.title("Water Consumption vs Impervious Surfaces")
    plt.xlabel("Impervious Surface")
    plt.ylabel("Water Consumption")
    st.pyplot(plt)

    # Insights Summary
    st.subheader("🔍 Summary of Insights")
    st.write("""
    - Adopt a Stream Participation: Fluctuating trends in community participation indicate opportunities for increased engagement.
    - Water Consumption: Impervious surfaces show a direct relationship with water consumption, emphasizing urban planning needs.
    """)

# 2. Education Trends
elif page == "🎓 Education Trends":
    st.title("🎓 Education Trends in Mecklenburg")
    st.write("""
    Analyze trends in absenteeism, elementary school proficiency, and high school graduation rates 
    to understand the education outcomes and challenges in the region.
    """)

    # Metrics Highlight
    avg_absenteeism = combined_data['Student_Absenteeism'].mean(skipna=True)
    avg_proficiency = combined_data['Proficiency_Elementary_School'].mean(skipna=True)
    st.write("### Key Education Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Avg Absenteeism", f"{avg_absenteeism:.2f}")
    col2.metric("Avg Proficiency", f"{avg_proficiency:.2f}")

    # Scatter Plot: Absenteeism vs Elementary Proficiency
    st.subheader("📉 Absenteeism vs Elementary Proficiency")
    edu_data = combined_data.dropna(subset=["Student_Absenteeism", "Proficiency_Elementary_School"])
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=edu_data, x="Student_Absenteeism", y="Proficiency_Elementary_School", color="orange")
    plt.title("Absenteeism Impact on Proficiency")
    plt.xlabel("Student Absenteeism (%)")
    plt.ylabel("Proficiency (%)")
    st.pyplot(plt)

    # High School Graduation Rate Trend
    st.subheader("🎓 High School Graduation Rate Over Time")
    df_graduation = combined_data.dropna(subset=["Highschool_Graduation_Rate"])
    avg_grad_rate = df_graduation.groupby("data_year")["Highschool_Graduation_Rate"].mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=avg_grad_rate, x="data_year", y="Highschool_Graduation_Rate", marker="o", color="green")
    plt.title("High School Graduation Rate Over Years")
    plt.xlabel("Year")
    plt.ylabel("Graduation Rate (%)")
    st.pyplot(plt)

    # Insights Summary
    st.subheader("🔍 Summary of Insights")
    st.write("""
    - Absenteeism Impact: High absenteeism rates correlate with lower academic performance.
    - Graduation Rates: Graduation rates show steady improvement, indicating positive education interventions.
    """)

# 3. Housing Trends
elif page == "🏠 Housing Trends":
    st.title("🏠 Housing Trends in Mecklenburg")
    st.write("""
    Understand housing density, foreclosure rates, and trends affecting residential stability and urban development in Mecklenburg County.
    """)

    # Metrics Highlight
    avg_density = combined_data['Housing_Density'].mean(skipna=True)
    avg_foreclosures = combined_data['Foreclosures'].mean(skipna=True)
    st.write("### Key Housing Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Avg Housing Density", f"{avg_density:.2f}")
    col2.metric("Avg Foreclosures", f"{avg_foreclosures:.2f}")

    # Housing Density Line Plot
    st.subheader("🏢 Housing Density Over Time")
    density_data = combined_data.dropna(subset=["data_year", "Housing_Density"]).groupby("data_year")["Housing_Density"].mean().reset_index()
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=density_data, x="data_year", y="Housing_Density", marker="o", color="purple")
    plt.title("Average Housing Density Over Years")
    plt.xlabel("Year")
    plt.ylabel("Housing Density")
    st.pyplot(plt)

    # Foreclosures Bar Plot
    st.subheader("📉 Foreclosure Trends")
    foreclosure_data = combined_data.dropna(subset=["data_year", "Foreclosures"]).groupby("data_year")["Foreclosures"].mean().reset_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=foreclosure_data, x="data_year", y="Foreclosures", color="red")
    plt.title("Average Foreclosures Over Years")
    plt.xlabel("Year")
    plt.ylabel("Foreclosures")
    st.pyplot(plt)

    # Insights Summary
    st.subheader("🔍 Summary of Insights")
    st.write("""
    - Housing Density: Density trends reflect growing urbanization.
    - Foreclosures: Foreclosure trends highlight economic pressures impacting housing stability.
    """)