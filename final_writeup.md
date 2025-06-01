# Headset Recommendations App 🎧

## Background
This project invovles web scraping headset data from [PCPartPicker](https://pcpartpicker.com) using an API, building a regression model to predict headset prices, deploying the model through a Flask API on Google Cloud to run the model, and creating an interactive web application using Streamlit. 

The goal is to allow users to input headset features and receive a predicted prince along with a list of similar headset recommendations. This tool can help users better understand headset pricing and make more informed purchasing decisions. 

## Exploratory Data Analysis
The initial dataset contains 2417 headsets with the following columns: `brand`, `model`, `form_factor`, `frequency_response`, `has_microphone`, `is_wireless`, `type`, `color`, `price`. `frequency_response`, `color`, and `price` have missing values. 

![price_distribution_outliers](https://github.com/user-attachments/assets/8e8d2efe-0ee5-4910-b170-c5ae2175d659)
![price_distribution_outliers_removed](https://github.com/user-attachments/assets/45fd8a19-db4b-4d5f-a4cd-45b427863aed)
![price_distribution](https://github.com/user-attachments/assets/dc3b8a5c-d62a-4e75-85cd-40199258fb96)
![price_distribution_brand](https://github.com/user-attachments/assets/c09a5915-97d4-4071-b577-d1a60ce818cb)

## Methodology

### Data Cleaning/Feature Engineering for Model
![correlation](https://github.com/user-attachments/assets/74e2dcf3-00dd-482d-9bf6-c77e67162805)
--
### Model
A Random Forest regression model ([model_regression.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_regression.py)) is trained on [model_data.csv](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_data.csv) to predict `price_usd`. The model uses the following features: 
- `brand_encoded`
- `min_freq`
- `max_freq`
- `is_wireless`
- `form_factor`

These predictors were selected based on eploratory analysis and their relevance to pricing. The Random Forest model was chosen for its ability to handle non-linear relationships and better performance compared to an XGBoost Regressor model. 

### Deployment Pipeline
1. Flask API\
   [📁 app/server.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/server.py)
2. Docker Container\
   [📁 app/Dockerfile](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/Dockerfile)\
   [📁 app/docker-compose-yml](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/docker-compose.yml)\
   [📁 app/requirements.txt](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/requirements.txt)
4. Google Cloud Deployment
5. Streamlit App\
   [📁 app/app.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/app.py)

We created a Flask API to serve model predictions, which communicates with Streamlit frontend for user interaction. The Flask API is deployed on Google Cloud and the app is deployed on Streamlit. 

#### Flask API
#### Docker Image/Container
#### Google Cloud Deplyment
#### Streamlit App

## Results and Discussion
The Random Forest model achieved an RMSE of $60.51, MAE of $45.98,k and R^2 of 0.4983, indicating moderate predictive performance. On average, the model is about $46 off from the true price, which suggests it captures general pricing trends. However, there is still significant room for improvement. An example would be to add more features to increase model complexity.

For future work, a more complete dataset could be obtained by using BeautifulSoup to scrape data directly from PCPartPicker, rather than relying on the API. This would allow gathering additional important features, such as product ratings, which could be valuable for improving price prediction.
