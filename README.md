# Headset Price Prediction 🎧 
💻 [Streamlit App](https://cb-headset-recommendations-app.streamlit.app/)\
🌐 [Flask API on Google Cloud Run](https://headset-prediction-app-378985735322.us-central1.run.app/)

## Project Overview
This interactive web application predicts headset prices based on product features using a Random Forest regression model. The data was collected from [PCPartPicker](https://pcpartpicker.com/) using this [PCPartPicker API](https://github.com/JonathanVusich/pcpartpicker/blob/master/README.md). The app connects to a deployed Flask API that contains the trained model.
- **Data Collection:** Web scraping headset data using from https://pcpartpicker.com/ using an API 
- **Modeling:** Built a Random Forest regression model (RMSE ≈ **60.51**) to predict headset price
    - Note: RMSE of 60.51 suggests room for model improvement. For demo purposes, the current model is used.
- **App:** Streamlit web interface for selecting headset features and viewing predicted prices + recommendations
- **Docker Image:** Containerized the Flask API and model for consistent deployment
- **Deployment:** Flask API and Streamlit app hosted on Google Cloud Run and Streamlit Cloud

### Folders
- **/Project Proposal** - Contains the initial project proposal slides and earlier attempts at data collection (these are no longer used in the final version)
- **/app** - Contains all the necessary files to deploy the streamlit app, including the Streamlit frontend and Flask API connection code
- **/data-retrieval-cleaning** - Includes notebooks for data retrieval and cleaning, exploratory data analysis, and the original headset data collected using the PCPartPicker API
---

### Streamlit App 
1. Go to https://cb-headset-recommendations-app.streamlit.app/
2. Select your headset preferences
    - Brand
    - Min Frequency (slider)
    - Max Frequency (slider)
    - Connectivity (Wireless/Wired)
    - Form Factor (Circumaural/Supra-aural)
7. Click **Predict Price**
8. Results:
    - Predicted Price
    - Category
    - Recommended similar headsets

---

### Flask API (Google Cloud Run)
1. Visit the url https://headset-prediction-app-378985735322.us-central1.run.app/
    - You should see the message: `server  is up - nice job!`
2.  Run the following curl command to see the results.\
    `curl -X POST https://headset-prediction-app-378985735322.us-central1.run.app/predict_price \
      -H "Content-Type: application/json" \
      -d '{"brand_encoded": 15, "min_freq": 20, "max_freq": 20000, "is_wireless": 1, "form_factor": 0}'
    `

    - This should print `Predicted Price: $179.93`

