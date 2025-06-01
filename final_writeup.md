# Headset Recommendations App 🎧

## Background
This project invovles web scraping headset data from [PCPartPicker](https://pcpartpicker.com) using an API, building a regression model to predict headset prices, deploying the model through a Flask API on Google Cloud to run the model, and creating an interactive web application using Streamlit. 

The goal is to allow users to input headset features and receive a predicted prince along with a list of similar headset recommendations. This tool can help users better understand headset pricing and make more informed purchasing decisions. 

## Exploratory Data Analysis
The initial dataset contains 2417 headsets with the following columns: `brand`, `model`, `form_factor`, `frequency_response`, `has_microphone`, `is_wireless`, `type`, `color`, `price`. `frequency_response`, `color`, and `price` have missing values. 

![price_distribution_outliers](https://github.com/user-attachments/assets/8e8d2efe-0ee5-4910-b170-c5ae2175d659)
![price_distribution_outliers_removed](https://github.com/user-attachments/assets/45fd8a19-db4b-4d5f-a4cd-45b427863aed)
![price_distribution](https://github.com/user-attachments/assets/dc3b8a5c-d62a-4e75-85cd-40199258fb96)
![top_brands](https://github.com/user-attachments/assets/c212e599-f8fc-4a20-8a56-d3ecffa028d5)
![price_distribution_brand](https://github.com/user-attachments/assets/c09a5915-97d4-4071-b577-d1a60ce818cb)

## Methodology

### Data Cleaning/Feature Engineering for Model
![correlation](https://github.com/user-attachments/assets/74e2dcf3-00dd-482d-9bf6-c77e67162805)
--
### Model

### Deployment Pipeline
1. Flask API
2. Docker Container
3. Google Cloud Deployment
4. Streamlit App

#### Flask API
#### Docker Image/Container
#### Google Cloud Deplyment
#### Streamlit App

## Results

## Discussion
