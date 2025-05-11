import base64
import json
import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Answer, Community

load_dotenv()

url = "https://api.perplexity.ai/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv('PPLX_API_KEY')}",
    "accept": "application/json",
    "content-type": "application/json",
}


app = Flask(__name__)
CORS(app)


@app.route("/answer", methods=["POST"])
def answer():
    data = request.get_json()
    print(data)

    image = data["image"]
    lat, lng, alt = data["location"]

    print(image)
    print(lat, lng, alt)

    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Analyze this image and return short description of the place with respect to suitability of plant growth "
                        "and suggest plants that can grow in this place having coordinates [{lat}, {lng}] and altitude {alt} and average weather condition of this place",
                    },
                    {"type": "image_url", "image_url": {"url": image}},
                ],
            },
        ],
        "stream": False,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": Answer.model_json_schema()},
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return jsonify(json.loads(response.json()["choices"][0]["message"]["content"]))

    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")


@app.route("/community", methods=["POST"])
def community():
    data = request.get_json()
    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": "You are a community builder of people who want to plant trees to nearby places."
                "They have been suggested some plants according to their place and weather. Your job is to analyze the plants of the corresponding users "
                "and create a group of those users and return group of those users whose plants are of similar type and how they can collaborate with themselves",
            },
            {"role": "user", "content": json.dumps(data["users"])},
        ],
        "stream": False,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": Community.model_json_schema()},
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return jsonify(json.loads(response.json()["choices"][0]["message"]["content"]))

    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")


@app.route("/users")
def users():
    # Other app users details
    users = [
        {
            "name": "Raj",
            "plants": [
                "Spider Plant",
                "Peace Lily",
                "Snake Plant",
                "Pothos",
                "Rubber Plant",
            ],
        },
        {"name": "Aisha", "plants": ["Guava", "Lemon", "Papaya"]},
        {"name": "John", "plants": ["Oak", "Maple", "Pine", "Cedar"]},
        {"name": "Maria", "plants": ["Rose", "Jasmine", "Hibiscus", "Marigold"]},
        {"name": "Liam", "plants": ["Apple", "Cherry", "Peach"]},
        {"name": "Sophia", "plants": ["Coconut", "Banana", "Areca Palm"]},
        {"name": "Ethan", "plants": ["Teak", "Mahogany", "Sandalwood"]},
        {"name": "Olivia", "plants": ["Lavender", "Thyme", "Basil", "Mint"]},
        {"name": "Noah", "plants": ["Bamboo", "Fern", "Aloe Vera", "Cactus"]},
    ]
    return jsonify(users)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
