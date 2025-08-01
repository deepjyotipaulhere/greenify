import base64
import json
import os
import re
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Answer1, Answer2, Community
from typing import Any, Dict

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
                        "text": f"Analyze this image and return short description of the place with respect to suitability of plant growth ",
                    },
                    {"type": "image_url", "image_url": {"url": image}},
                ],
            },
        ],
        "stream": False,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": Answer1.model_json_schema()},
        },
    }

    answer1 = {}

    # try:
    #     response = requests.post(url, headers=headers, json=payload)
    #     response.raise_for_status()  # Raise an exception for bad status codes
    #     return jsonify(json.loads(response.json()["choices"][0]["message"]["content"]))

    # except requests.exceptions.RequestException as e:
    #     print(f"API Request failed: {e}")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(response.text)
        answer_text = response.text
        text_cleaned = re.sub(
            r"<think>.*?</think>\s*", "", answer_text, flags=re.DOTALL
        )
        json_match = re.search(r"{.*}", text_cleaned, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                # Parse the JSON string
                answer_data = json.loads(json_str)
                print(answer_data)
                answer1 = json.loads(answer_data["choices"][0]["message"]["content"])

            except json.JSONDecodeError as e:
                answer1 = json.loads(
                    response.json()["choices"][0]["message"]["content"]
                )

        # response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")

    payload_research = {
        "model": "sonar-deep-research",
        "messages": [
            {
                "role": "system",
                "content": "You are a plant growth expert. You are given a description of a place where an user want to grow some plants. You are also given latitude, longitude and altitude of the user. Your task is to suggest at most 5 plant that can be grown by the user in that particular place according to average weather.",
            },
            {
                "role": "user",
                "content": f"I am standing in a place having coordinates [{lat}, {lng}] and altitude {alt}]. The place can be described as follows: {answer1}"
                "Suggest at most five suitable plants that can be grown here.",
            },
        ],
        "stream": False,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": Answer2.model_json_schema()},
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload_research)
        print(response.text)
        answer_text = response.text
        text_cleaned = re.sub(
            r"<think>.*?</think>\s*", "", answer_text, flags=re.DOTALL
        )
        json_match = re.search(r"{.*}", text_cleaned, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                # Parse the JSON string
                answer_data = json.loads(json_str)
                print(answer_data)
                return jsonify(
                    json.loads(answer_data["choices"][0]["message"]["content"])
                    | answer1
                )

            except json.JSONDecodeError as e:
                return jsonify(
                    json.loads(response.json()["choices"][0]["message"]["content"])
                    | answer1
                )

        # response.raise_for_status()

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

    # try:
    #     response = requests.post(url, headers=headers, json=payload)

    #     answer_text = response.text
    #     text_cleaned = re.sub(
    #         r"<think>.*?</think>\s*", "", answer_text, flags=re.DOTALL
    #     )
    #     json_match = re.search(r"{.*}", text_cleaned, re.DOTALL)
    #     if json_match:
    #         json_str = json_match.group(0)
    #         try:
    #             # Parse the JSON string
    #             answer_data = json.loads(json_str)
    #             return jsonify(
    #                 json.loads(answer_data["choices"][0]["message"]["content"])
    #             )

    #         except json.JSONDecodeError as e:
    #             print("Error decoding JSON:", e)

    #     # response.raise_for_status()

    # except requests.exceptions.RequestException as e:
    #     print(f"API Request failed: {e}")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(response.text)
        answer_text = response.text
        text_cleaned = re.sub(
            r"<think>.*?</think>\s*", "", answer_text, flags=re.DOTALL
        )
        json_match = re.search(r"{.*}", text_cleaned, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                # Parse the JSON string
                answer_data = json.loads(json_str)
                print(answer_data)
                return jsonify(
                    json.loads(answer_data["choices"][0]["message"]["content"])
                )

            except json.JSONDecodeError as e:
                return jsonify(
                    json.loads(response.json()["choices"][0]["message"]["content"])
                )

        # response.raise_for_status()

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
