from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from optimizer import Optimizer
import numpy

app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=['POST', 'OPTIONS'])
@cross_origin()
def generate():
    max_risk = float(request.json['max_risk'])
    opt = Optimizer(max_risk)
    portfolio = opt.generate_genetic_algorithm_portfolio()
    if portfolio == None:
        resp = jsonify(None)
        resp.status_code = 500
        return resp
    message = { 'weights': portfolio.weights.tolist(), 'expected_return': portfolio.expected_return * 100, 'std': portfolio.std * 100 }
    resp = jsonify(message)
    resp.status_code = 200
    return resp
if __name__ == "__main__":
    app.run(debug=True)
