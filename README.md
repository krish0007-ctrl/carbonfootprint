# Carbon Footprint Calculator

A comprehensive Carbon Footprint Calculator built with Streamlit that allows users to estimate their environmental impact across multiple categories including Household, Transport, Car, and Food. The app provides interactive visualizations and tracks footprint data during the user session.

## Features

- Calculate carbon footprint for:
  - Household energy consumption
  - Transport modes (bus, train, taxi, flights)
  - Car emissions based on fuel type and distance
  - Food consumption based on diet type and meals per week
- User profile management (name, email, location)
- Interactive charts and visualizations using Plotly
- Impact level indicators with intuitive emojis
- Background image customization
- Data stored only during the current session for privacy

## Installation

1. Clone the repository or download the project files.
2. Ensure you have Python 3.7+ installed.
3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app with the following command:

```bash
streamlit run merged_carbon_calculator.py
```

This will open the app in your default web browser. Use the sidebar to enter your profile information and navigate through the tabs to calculate your carbon footprint in different categories.

## Categories Explained

- **Household:** Calculates emissions based on electricity, natural gas, heating oil, and coal consumption per household member.
- **Transport:** Estimates emissions from bus, train, taxi, and flights based on kilometers traveled.
- **Car:** Calculates emissions based on distance driven, fuel type (Petrol, Diesel, Hybrid, Electric), and fuel efficiency.
- **Food:** Estimates yearly carbon footprint based on diet type (Meat lover, Average, Vegetarian, Vegan) and number of meals per week.

## Data Storage

All footprint data is stored only during the current session and is not saved permanently. Closing the app or refreshing the page will clear the data.

## About

This calculator uses standard emissions factors from environmental research to provide an estimate of your carbon footprint. It is designed for educational and awareness purposes.
