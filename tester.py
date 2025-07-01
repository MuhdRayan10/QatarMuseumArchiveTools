from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)


with open('assets_data.json') as f:
    asset_data = json.load(f)


@app.route('/')
def dashboard():
    months = list(asset_data.keys())

    return render_template("index.html", content = 'user!')

@app.route('/get_data')
def get_data():
    selected_month = request.json['month']
    





if __name__ == "__main__":
    app.run(debug=True)

