from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from optimizer import Optimizer
import assets
import numpy
import time

app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=['POST', 'OPTIONS'])
@cross_origin()
def generate():
    t0 = time.time()
    max_risk = float(request.json['max_risk'])
    assets = request.json['assets']
    opt = Optimizer(max_risk, assets)
    portfolio = opt.generate_genetic_algorithm_portfolio()
    if portfolio == None:
        resp = jsonify(None)
        resp.status_code = 500
        return resp
    t1 = time.time()
    print("Total Optimization in: " + str(int(t1 - t0)) + " seconds")
    message = { 'weights': portfolio.weights.tolist(), 'expected_return': portfolio.expected_return * 100, 'std': portfolio.std * 100 }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route("/stocks", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_stocks():
    stocks = assets.get_assets()
    return { 'data': [e.serialize() for e in stocks] }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
