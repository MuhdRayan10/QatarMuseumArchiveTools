from flask import Flask, render_template, jsonify, request
import json

from api_handler import fetch_data, update_data
from database import get_counts, get_users

DEPLOYED = False
app = Flask(__name__, static_folder="static", template_folder="templates")

# temporarily reading from json file
# data_file = os.path.join(os.path.dirname(__file__), "alt_assets.json")

@app.route("/")
def index():
    return render_template("dashboard.html")
@app.route("/api/data")
def api_data():
    user = request.args.get("user", None)
    if DEPLOYED:
        data = fetch_data()
    else:
        with open("webdashboard/new_assets.json") as f:
            data = json.load(f)
    
    update_data(data)

    data = get_counts(user)
    return jsonify(data)

@app.route("/api/users")
def api_users():
    return jsonify(get_users())


if __name__ == "__main__":
    app.run(debug=True)


