import requests, json
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/data', methods=["GET"])
def testpost():
    try:
         stock = request.args.get('ticker')
         return jsonify(getStockData(stock))
    except:
        return "Error finding stock data."
def remove_empty_elements(d):
    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}
def getStockData(t):
    response = requests.get(f'https://finance.yahoo.com/quote/{t}').text.split("root.App.main =")[1].split("(this))")[0].split("}}}};")[0] + "}}}}"
    j=json.loads(response)['context']['dispatcher']['stores']['QuoteSummaryStore']
    j = remove_empty_elements(j)
    return j
