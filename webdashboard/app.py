from flask import Flask, render_template, jsonify
import json, os, requests

from api_handler import fetch_data

app = Flask(__name__, static_folder="static", template_folder="templates")

# temporarily reading from json file
# data_file = os.path.join(os.path.dirname(__file__), "alt_assets.json")

@app.route("/")
def index():
    return render_template("dashboard.html")



@app.route("/api/data")
def api_data():
    data = fetch_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)


