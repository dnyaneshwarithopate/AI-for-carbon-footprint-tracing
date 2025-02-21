import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from carbon_calculator import calculate_footprint, EMISSION_FACTORS

# Configure Streamlit
st.set_page_config(page_title="Carbon Footprint Tracker", page_icon="🌍")
st.title("AI-Powered Carbon Footprint Tracker 🌱")

# Load or initialize sample data
@st.cache_data
def load_data():
    return pd.read_csv("src/data/sample_data.csv")

# Train clustering model (simple example)
def train_model(df):
    features = df[['electricity_kwh', 'miles_driven', 'diet_score', 'flights_hours']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(scaled_features)
    return scaler, kmeans

# User input form
with st.form("user_input"):
    st.header("Your Activity Details")
    electricity = st.number_input("Monthly electricity usage (kWh)", min_value=0, value=300)
    miles = st.number_input("Monthly miles driven (gasoline car)", min_value=0, value=800)
    diet = st.select_slider("Diet (1 = meat-heavy, 5 = vegan)", options=[1, 2, 3, 4, 5], value=3)
    flights = st.number_input("Yearly flight hours", min_value=0, value=4)
    submitted = st.form_submit_button("Calculate My Footprint")

if submitted:
    # Calculate emissions
    emissions = calculate_footprint({
        'electricity_kwh': electricity,
        'miles_driven': miles,
        'diet_score': diet,
        'flights_hours': flights
    })
    
    # Load data and train model
    df = load_data()
    scaler, model = train_model(df)
    
    # Predict cluster for recommendations
    user_data = pd.DataFrame([{
        'electricity_kwh': electricity,
        'miles_driven': miles,
        'diet_score': diet,
        'flights_hours': flights
    }])
    scaled_data = scaler.transform(user_data)
    cluster = model.predict(scaled_data)[0]
    
    # Display results
    st.success(f"*Your Monthly Carbon Footprint:* {emissions:.2f} kg CO2")
    
    # Recommendations
    st.subheader("Personalized Recommendations")
    recommendations = {
        0: ["Switch to renewable energy 🌞", "Use public transport 🚌", "Reduce meat consumption 🥦"],
        1: ["Optimize home insulation 🏠", "Carpool for long commutes 👥", "Offset flight emissions ✈"],
        2: ["Keep up the good work! 🌟", "Advocate for climate policies 📢", "Invest in solar panels 🔋"]
    }
    for action in recommendations[cluster]:
        st.write(f"- {action}")

    # Visualization
    st.subheader("How You Compare")
    st.bar_chart(df.groupby('cluster')['total_emissions'].mean())
