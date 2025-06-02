# Data Retrieval and Cleaning
This folder contains the following files:
- [Dockerfile](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/Dockerfile) - Contains script to build the Docker Image for the Flask API
- [app.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/app.py) - Contains the code for the Streamlit app to call the Flask API and any frontend features
- [docker-compose.yml](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/docker-compose.yml) - Defines how the containers should be configured 
- [model_data.csv](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_data.csv) - Contains the cleaned and processed dataset used to train the Random Forest regression model to predict headset prices
- [model_regression.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/model_regression.py) - Contains the script for the Rnadom Forest regression model
- [requirements.txt](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/requirements.txt) - Lists all the Python packages and dependencies required for the app and API to run 
- [server.py](https://github.com/hoangchb/STAT-418-Final-Project/blob/main/app/server.py) - Contains the Flask API server script that loads the trained model, accepts input features, makes price predictions, and returns the results to the Streamlit app
