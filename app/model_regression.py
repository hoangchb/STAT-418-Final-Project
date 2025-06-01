import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

model_data = pd.read_csv('model_data.csv')
columns_to_include = ['brand_encoded', 'min_freq', 'max_freq', 'is_wireless', 'form_factor']

y = model_data['price_usd']
X = model_data[columns_to_include]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

def predict_price(dict_values, model=rf_model):
  input = pd.DataFrame([dict_values], columns=columns_to_include)
  y_pred = model.predict(input)
  return y_pred[0]