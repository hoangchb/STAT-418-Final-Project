import os
import json

from flask import Flask, jsonify, request
from model_regression import predict_price

HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def flask_app():
    app = Flask(__name__)


    @app.route('/', methods=['GET'])
    def server_is_up():
        # print("success")
        return 'server is up - nice job! \n \n'

    @app.route('/predict_price', methods=['POST'])
    def predict_price_route():
        to_predict = request.json
        print(to_predict)
        pred = predict_price(to_predict)
        return jsonify({"Predicted Price": f"${pred:.2f}"})

    return app

if __name__ == '__main__':
    app = flask_app()
    app.run(debug=True, host='0.0.0.0', port=5001)