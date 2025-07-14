from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "your_ibm_api_key_here"
DEPLOYMENT_URL = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/49781105-393e-49a1-a203-ab422fc27ef7/predictions?version=2021-05-01"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        # Step 1: Get IAM token
        token_res = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"apikey={API_KEY}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        )

        access_token = token_res.json()["access_token"]

        # Step 2: Prepare payload
        payload = {
            "input_data": [{
                "fields": ["age", "sleep", "screen"],
                "values": [[data["age"], data["sleep"], data["screen"]]]
            }]
        }

        # Step 3: Score with Watson
        scoring_res = requests.post(
            DEPLOYMENT_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json=payload
        )

        prediction = scoring_res.json()["predictions"][0]["values"][0][0]
        return jsonify(result=f"Predicted Stress Load: {prediction}%")

    except Exception as e:
        return jsonify(result="⚠️ Error occurred: " + str(e)), 500
