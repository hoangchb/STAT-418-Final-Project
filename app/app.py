import streamlit as st
import pandas as pd
import requests

st.title('Headsets Price Predictor :headphones:')

brand_mapping = {
    'AKG': 0, 
    'Adesso': 1, 
    'Astro': 2, 
    'Asus': 3, 
    'Audio-Technica': 4, 
    'Beyerdynamic': 5,
    'Cooler Master': 6, 
    'Corsair': 7, 
    'Creative Labs': 8, 
    'Cyber Acoustics': 9,
    'Ergoguys': 10, 
    'Harman Kardon': 11, 
    'JBL': 12, 
    'Kingston': 13, 
    'Koss': 14,
    'Logitech': 15, 
    'Mad Catz': 16, 
    'Other': 17, 
    'Panasonic': 18, 
    'Philips': 19,
    'Pioneer': 20, 
    'ROCCAT': 21, 
    'Razer': 22, 
    'Sennheiser': 23, 
    'Skullcandy': 24,
    'Sony': 25, 
    'SteelSeries': 26, 
    'Syba': 27, 
    'Thermaltake': 28, 
    'Turtle Beach': 29
}

form_factor_mapping = {
    "Circumaural": 0,
    "Supra-aural": 1
}

# ------ User inputs for features -----
brand = st.selectbox("Select Brand", list(brand_mapping.keys()))
brand_encoded = brand_mapping[brand]

min_freq = st.slider("Minimum Frequency (Hz)", min_value=3, max_value=300, value=20, step=1)
max_freq = st.slider("Maximum Frequency (Hz)", min_value=2000, max_value=55000, value=20000, step=1000)

connectivity = st.selectbox("Connectivity", ["Wireless", "Wired"])
is_wireless = 1 if connectivity == "Wireless" else 0

form_factor = st.radio(
    "Select Form Factor:",
    ("Circumaural", "Supra-aural")
)
form_factor_encoded = form_factor_mapping[form_factor]


# Categorize price into labels
def categorize_price(price):
    if price < 50:
        return "Affordable"
    elif price < 150:
        return "Mid-range"
    else:
        return "Premium"

# Predict
if st.button("Predict Price"):
    input_data = {
        "brand": brand_encoded,
        "min_freq": min_freq,
        "max_freq": max_freq,
        "is_wireless": is_wireless,
        "form_factor": form_factor_encoded
    }

    try:
        response = requests.post("http://localhost:5001/predict_price", json=input_data)
        response.raise_for_status()  

        result = response.json()
        predicted_price = float(result["Predicted Price"].replace("$", ""))
        price_category = categorize_price(predicted_price)

        st.success(f"Predicted Price: ${predicted_price:.2f}")
        st.info(f"Category: {price_category}")

        model_data = pd.read_csv("model_data.csv") 
        recommendations = model_data[
            (model_data['price_usd'] >= predicted_price - 20) &
            (model_data['price_usd'] <= predicted_price + 20) &
            (model_data['form_factor'] == form_factor_encoded)
        ].sample(n=3, random_state=1)

        st.write("Here are some similar headsets:")
        st.dataframe(recommendations[['brand', 'model', 'price_usd']].reset_index(drop=True))

    except Exception as e:
        st.error(f"Error: {e}")
