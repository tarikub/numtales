from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import os
import glob
from bson import ObjectId
import config.config as cfg

app = Flask(__name__)

# Enable CORS for all routes (or restrict to your frontend domain)
CORS(app, origins=["*"])

from pymongo import MongoClient
from transformers import AutoTokenizer, AutoModel

# Initialize MongoDB client and specify the database and collection
client = MongoClient(cfg.MONGO_URI)

db = client[cfg.DB_NAME]  # Replace with your database name
collection = db[cfg.STORIES_COLLECTION_NAME]  # Replace with your collection name

tokenizer = AutoTokenizer.from_pretrained(cfg.SENTENCE_TRANSFORMERS_MODEL)
model = AutoModel.from_pretrained(cfg.SENTENCE_TRANSFORMERS_MODEL)


def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt",
                       truncation=True, padding=True)
    outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1)
    return embedding.detach().numpy().tolist()[0]


def image_vector_search(query_embedding):
    pipelines_images = [
        {
            "$vectorSearch": {
                "index": "vector_index_images",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 150,
                "limit": 10
            }
        }
    ]

    # Search images
    images_collection = db["images"]
    results_images = list(images_collection.aggregate(pipelines_images))

    # Optionally, sort by score if available
    results_images.sort(key=lambda x: x.get('score', 0), reverse=True)

    return {
        "images": results_images
    }


def story_match_search(query_text):
    pipelines = [
        {
            "$match": {
                "number": int(query_text)
            }
        }
    ]

    # Search stories
    results_stories = list(collection.aggregate(pipelines))

    # Optionally, sort by score if available
    results_stories.sort(key=lambda x: x.get('score', 0), reverse=True)

    return {
        "stories": results_stories,
    }


def convert_objectid(obj):
    if isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

# Handle CORS preflight requests
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://numtales-frontend-758664829455.us-west1.run.app"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route('/searchstory', methods=['OPTIONS', 'GET'])
def search_story(): 
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 204
    
    query_text = request.args['query']
    result = story_match_search(query_text)
    result = convert_objectid(result)
    return jsonify(result)

@app.route('/searchimage', methods=['OPTIONS', 'GET'])
def search_image(): 
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 204
    
    query_text = request.args['query']
    query_embedding = get_embedding(query_text)
    result = image_vector_search(query_embedding)
    result = convert_objectid(result)
    return jsonify(result)

if __name__ == "__main__":
    port = 5000
    app.run(debug=True, host='0.0.0.0', port=port)
