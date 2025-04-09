"""
Carbon Footprint Calculator - Merged Version
Combines all features from various versions into one comprehensive calculator


"""

import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime

# Initialize session state for data storage
if 'footprint_data' not in st.session_state:
    st.session_state.footprint_data = pd.DataFrame(columns=[
        'Type', 'Value', 'Timestamp', 'Category'
    ])

def save_data(data):
    """Save footprint data to session state"""
    new_row = pd.DataFrame([data])
    st.session_state.footprint_data = pd.concat(
        [st.session_state.footprint_data, new_row],
        ignore_index=True
    )

# Background image setup from main.py
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Impact level display from enhanced_carbon_calculator.py
def show_impact(value, category):
    """Show impact level with appropriate styling"""
    thresholds = {
        'Household': ([2, 5, 10], ["🌱 Excellent!", "⚠️ Moderate", "❗ High", "🚨 Very High"]),
        'Transport': ([1, 3, 5], ["🚆 Great!", "⚠️ Average", "❗ High", "✈️ Very High"]),
        'Car': ([2, 4, 6], ["⚡ Efficient!", "⚠️ Average", "❗ High", "💨 Very High"]),
        'Food': ([1.5, 3, 4.5], ["🌱 Sustainable!", "⚠️ Average", "❗ High", "🍗 Very High"])
    }
    
    if value < thresholds[category][0][0]:
        st.success(thresholds[category][1][0])
    elif value < thresholds[category][0][1]:
        st.warning(thresholds[category][1][1])
    elif value < thresholds[category][0][2]:
        st.error(thresholds[category][1][2])
    else:
        st.error(thresholds[category][1][3], icon="🚨")

# Visualizations from enhanced_carbon_calculator.py
def show_visualizations():
    """Display interactive charts with error handling"""
    if st.session_state.footprint_data.empty:
        return
        
    try:
        st.subheader("📊 Your Footprint History")
        
        # Time series line chart with markers
        if not st.session_state.footprint_data.empty:
            fig = px.line(
                st.session_state.footprint_data,
                x='Timestamp',
                y='Value',
                color='Category',
                title='Carbon Footprint Over Time',
                markers=True,
                line_shape='spline'
            )
            fig.update_traces(line=dict(width=3))
            st.plotly_chart(fig, use_container_width=True)
        
        # Latest comparison as pie chart
        st.subheader("🔍 Footprint Composition")
        if not st.session_state.footprint_data.empty:
            latest = st.session_state.footprint_data.dropna().groupby('Category').last().reset_index()
            if not latest.empty:
                fig = px.pie(
                    latest,
                    names='Category',
                    values='Value',
                    title='Latest Footprint Composition',
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No complete data available for visualization")
    except Exception as e:
        st.error(f"Error displaying visualizations: {str(e)}")

# Calculation methods from equations.py with improved UI
def household_calculator():
    with st.expander("🏠 Household Emissions", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            members = st.number_input("Household members", 1, 20, 1)
            electricity = st.number_input("Electricity (kWh)", 0.0, 100000.0, 0.0)
            gas = st.number_input("Natural gas (kWh)", 0.0, 100000.0, 0.0)
        with cols[1]:
            oil = st.number_input("Heating oil (litres)", 0.0, 10000.0, 0.0)
            coal = st.number_input("Coal (kg)", 0.0, 10000.0, 0.0)
        
        if st.button("Calculate Household Footprint"):
            total = (
                (electricity * 0.000708) +
                (gas * 0.0002) +
                (oil * 0.0027) +
                (coal * 0.00288)
            ) / members
            
            st.metric("Total Footprint", f"{round(total, 2)} metric tons CO₂")
            show_impact(total, "Household")
            
            # Store results
            new_data = {
                'Type': 'Household',
                'Value': round(total, 2),
                'Timestamp': datetime.now(),
                'Category': 'Household'
            }
            save_data(new_data)
            
            show_visualizations()

def transport_calculator():
    with st.expander("🚌 Transport Emissions", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            bus = st.number_input("Bus (km)", 0.0, 50000.0, 0.0)
            train = st.number_input("Train (km)", 0.0, 50000.0, 0.0)
        with cols[1]:
            taxi = st.number_input("Taxi (km)", 0.0, 50000.0, 0.0)
            flights = st.number_input("Flights (km)", 0.0, 500000.0, 0.0)
        
        if st.button("Calculate Transport Footprint"):
            total = (
                (bus * 0.0001) +
                (train * 0.00004) +
                (taxi * 0.0001) +
                (flights * 0.0002)
            )
            
            st.metric("Total Footprint", f"{round(total, 2)} metric tons CO₂")
            show_impact(total, "Transport")
            
            # Store results
            new_data = {
                'Type': 'Transport',
                'Value': round(total, 2),
                'Timestamp': datetime.now(),
                'Category': 'Transport'
            }
            save_data(new_data)
            
            show_visualizations()

# Main app structure from carbon_footprint_calculator.py with enhancements
def main():
    st.set_page_config(
        page_title="Carbon Calculator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    set_background('background.png')
    
    st.title("🌍 Carbon Footprint Calculator")
    st.write("Calculate and track your environmental impact across different categories")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Household", 
        "🚌 Transport", 
        "🚗 Car", 
        "🍗 Food"
    ])
    
    with tab1:
        household_calculator()
    with tab2:
        transport_calculator()
    with tab3:
        with st.expander("🚗 Car Emissions", expanded=True):
            cols = st.columns(2)
            with cols[0]:
                distance = st.number_input("Distance driven (km)", 0.0, 100000.0, 0.0)
                fuel_type = st.selectbox("Fuel type", ["Petrol", "Diesel", "Hybrid", "Electric"])
            with cols[1]:
                fuel_efficiency = st.number_input("Fuel efficiency (L/100km)", 0.0, 20.0, 8.0)
                
            if st.button("Calculate Car Footprint"):
                # Emission factors (kg CO2 per liter or per km for electric)
                factors = {
                    "Petrol": 2.31,
                    "Diesel": 2.68, 
                    "Hybrid": 1.50,
                    "Electric": 0.05  # kg CO2 per km (depends on electricity source)
                }
                
                if fuel_type == "Electric":
                    total = distance * factors[fuel_type] / 1000  # Convert to metric tons
                else:
                    total = (distance * (fuel_efficiency/100) * factors[fuel_type]) / 1000
                
                st.metric("Total Footprint", f"{round(total, 2)} metric tons CO₂")
                show_impact(total, "Car")
                
                new_data = {
                    'Type': 'Car',
                    'Value': round(total, 2),
                    'Timestamp': datetime.now(),
                    'Category': 'Car'
                }
                save_data(new_data)
                
                show_visualizations()

    with tab4:
        with st.expander("🍗 Food Emissions", expanded=True):
            diet_type = st.selectbox("Diet type", [
                "Meat lover",
                "Average",
                "Vegetarian", 
                "Vegan"
            ])
            
            meals = st.number_input("Meals per week", 1, 21, 14)
            
            if st.button("Calculate Food Footprint"):
                # Average kg CO2 per meal by diet type
                factors = {
                    "Meat lover": 3.5,
                    "Average": 2.5,
                    "Vegetarian": 1.5,
                    "Vegan": 1.0
                }
                
                total = (meals * factors[diet_type] * 52 / 1000)  # Yearly total in metric tons
                
                st.metric("Yearly Footprint", f"{round(total, 2)} metric tons CO₂")
                show_impact(total, "Food")
                
                new_data = {
                    'Type': 'Food',
                    'Value': round(total, 2),
                    'Timestamp': datetime.now(),
                    'Category': 'Food'
                }
                save_data(new_data)
                
                show_visualizations()
    
    st.sidebar.header("About")
    st.sidebar.info("""
        This calculator estimates your carbon footprint using 
        standard emissions factors from environmental research.
        Data is stored only during your current session.
    """)

if __name__ == "__main__":
    main()
