from flask import Flask, render_template, jsonify
import json, os, requests

from api_handler import fetch_data, calculate_asset_count

DEPLOYED = False
app = Flask(__name__, static_folder="static", template_folder="templates")

# temporarily reading from json file
# data_file = os.path.join(os.path.dirname(__file__), "alt_assets.json")

@app.route("/")
def index():
    return render_template("dashboard.html")
@app.route("/api/data")
def api_data():
    if DEPLOYED:
        data = fetch_data()
    else:
        with open("webdashboard/new_assets.json") as f:
            data = json.load(f)
    
    data = calculate_asset_count(data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)


