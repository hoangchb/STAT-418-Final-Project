# Data Retrieval and Cleaning
This folder contains the following files:
- [Dockerfile](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/Dockerfile) - Script to build the Docker Image for the Flask API
- [app.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/app.py) - Code for the Streamlit app to call the Flask API and any frontend features
- [docker-compose.yml](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/docker-compose.yml) - Defines how the containers should be configured 
- [model_data.csv](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_data.csv) - Cleaned and processed dataset used to train the Random Forest regression model to predict headset prices
- [model_regression.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_regression.py) - Script for training the Random Forest regression model
- [requirements.txt](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/requirements.txt) - Lists all the Python packages and dependencies required for the app and API to run 
- [server.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/server.py) - Flask API server script that loads the trained model, accepts input features, makes price predictions, and returns the results to the Streamlit app
