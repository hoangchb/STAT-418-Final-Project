# Headset Recommendations App 🎧

## Background
This project invovles web scraping headset data from [PCPartPicker](https://pcpartpicker.com) using an [API](https://github.com/JonathanVusich/pcpartpicker/blob/master/README.md), building a regression model to predict headset prices, deploying the model through a Flask API on Google Cloud to run the model, and creating an interactive web application using Streamlit. 

The goal is to allow users to input headset features and receive a predicted prince along with a list of similar headset recommendations. This tool can help users better understand headset pricing and make more informed purchasing decisions. 

## Exploratory Data Analysis
The initial dataset contained 2,417 headsets entries with the following columns: `brand`, `model`, `form_factor`, `frequency_response`, `has_microphone`, `is_wireless`, `type`, `color`, `price`. 

The `price` column initially had 1,673 rows with a value of zero. Since these likely represent missing or placeholder values rather than true prices, they were removed for the purpose of the price prediction model. After removing these rows, the dataset contained 744 entries. Among these, the average headset price was $135.62, with 75th percentile price was $158.90, and the maximum price was $3799.00. 

![price_distribution_outliers](https://github.com/user-attachments/assets/8e8d2efe-0ee5-4910-b170-c5ae2175d659)\
The price distribution is skewed to the right due to the few expensive headsets, which are outliers. The outliers are not representative of the overall dataset and can affect model performance. To avoid this, the top 5% of prices were removed and only the entries with a price at or below the 95th percentile were kept. This helps reduce the influence of extreme values and provides a more balanced distribution for model training. 

![price_distribution_outliers_removed](https://github.com/user-attachments/assets/45fd8a19-db4b-4d5f-a4cd-45b427863aed)\
After removing the outliers, the distribution remains right-skewed, but it's less extreme than before. To further trim and balance the dataset, the IQR method was applied to detect and remove outliers. This approach excludes both extremely low and high price values based on the distribution spread. 

![price_distribution](https://github.com/user-attachments/assets/dc3b8a5c-d62a-4e75-85cd-40199258fb96)\
Looking at the price distribution plot after these high and low extreme values were removed, it is apparent that the distribution is slightly better balanced. 

![price_distribution_brand](https://github.com/user-attachments/assets/c09a5915-97d4-4071-b577-d1a60ce818cb)
This boxplot compares the price distribution across the top 10 most common headset brands. Brands such as Final Audio Design and Sennheiser have a much wider price range and many high-value outliers compared to Koss and Skullcandy. 

## Methodology

### Data Cleaning/Feature Engineering for Model
To prepare the data for modeling, null values and data types were examined. Rows containing null values were removed from the dataset.

The binary features `has_microphone` and `is_wireless` were converted to integers (0 and 1).  The `frequency_response` feature was originally a string and was parsed to extract numeric features: `min_freq` and `max_freq`. The original `frequency_response` column was then dropped. 

The categorical variables `form_factor` and `type` were label encoded. The `color` feature, which can contain multiple values, was split and transformed into separate binary columns using one-hot encoding. Brands in `brand` with fewer than 5 counts were grouped into an 'Other' category before encoding. The encoded values were saved in a new column titled `brand_encoded` for further analysis and model fitting. 

The correlation heatmap showed all predictors had correlations below 0.5, indicating no strong linear relationships among the features.

![removing_null](https://github.com/user-attachments/assets/ce3873a7-e284-45ab-a684-b60ff459a6a7)\

![headset_dtypes](https://github.com/user-attachments/assets/bfd2a3e5-7305-4c43-b4ef-eee2f5f36e67)

![correlation](https://github.com/user-attachments/assets/74e2dcf3-00dd-482d-9bf6-c77e67162805)

--
### Model
A Random Forest regression model ([model_regression.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_regression.py)) is trained on [model_data.csv](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_data.csv) to predict `price_usd`. The model uses the following features: 
- `brand_encoded`
- `min_freq`
- `max_freq`
- `is_wireless`
- `form_factor`

These predictors were selected based on exploratory analysis and their relevance to pricing. The Random Forest model was chosen for its ability to handle non-linear relationships and better performance compared to an XGBoost Regressor model. 

### Deployment Pipeline
1. Dataset\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📁 app/model_data.csv](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_data.csv)  
2. Model Script\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📁 app/model_regression.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_regression.py)
3. Flask API\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📁 app/server.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/server.py)
4. Docker Container\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📁 app/Dockerfile](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/Dockerfile)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📁 app/docker-compose.yml](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/docker-compose.yml)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📁 app/requirements.txt](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/requirements.txt)
5. Google Cloud Deployment
6. Streamlit App\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📁 app/app.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/app.py)

#### Flask API
The trained Random Forest model is served through a FlaskAPI defined in [`server.py`]((https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/server.py)). The API receives feature input from the frontend (Streamlit App), passes it to the model, and returns the predicted price. The command used to push the Flask API is listed under the Docker Image/Container section below.

#### Docker Image/Container
The API and its dependencies are packed into a Docker container using the `Dockerfile` and [`docker-compose.yml`](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/docker-compose.yml). This allows for consistent deployment and easy replication across environments. 

Commands used: 
1. `docker compose up -d`
2. `docker tag headset-price-prediction-api-app:latest chauhbui/headset-prediction-app:latest`
3. `docker buildx build --platform linux/amd64,linux/arm64 -t chauhbui/headset-prediction-app:latest --push .`

This builds a Docker image of the FlaskAPI and pushes it to Docker Hub, making it accessible for deployment on Google Cloud. 

#### Google Cloud Deployment
The Dockerized API was deployed on Google Cloud Run and ensures the model can handle API request from users interacting with the app. 

Steps followed:
1. Selected 'Deploy container' on Google Cloud Run 
2. Created a service
3. Selected 'Deploy one revision from an existining container image'
4. Entered the container image URL (`chauhbui/headset-prediction-app:latest`)
5. Selected Use Cloud IAM to authenticate learning requests --> Allow unauthenticated invocations
6. Changed the 'Container port' to `5001`
7. Deployed the Cloud Run and the resulting url was: https://headset-prediction-app-378985735322.us-central1.run.app
8. Tested the deployed API with the following commands
      - `curl -X POST https://headset-prediction-app-378985735322.us-central1.run.app/predict_price \ -H "Content-Type: application/json" \ -d '{"brand_encoded": 15, "min_freq": 20, "max_freq": 20000, "is_wireless": 1, "form_factor": 0}' `

#### Streamlit App
This website/interface was built using `app.py` to collect user inputs, send them to the Flask API, and display predicted headset prices. 
![streamlit](https://github.com/user-attachments/assets/151b6527-6c01-4d67-9bbf-1971c341557e)


## Results and Discussion
The Random Forest model achieved an **RMSE of $60.51**, **MAE of $45.98** and **R^2 of 0.4983**, indicating moderate predictive performance. On average, the model is about $46 off from the true price, which suggests it captures general pricing trends. However, there is still significant room for improvement. An example would be to add more features to increase model complexity.

For future work, a more complete dataset could be obtained by using BeautifulSoup to scrape data directly from PCPartPicker, rather than relying on the API. This would allow gathering additional important features, such as product ratings, which could be valuable for improving price prediction.
