from transformers import AutoTokenizer, AutoModel
import json
import csv
import os
from pymongo import MongoClient
import config.config as cfg
from utils.image_utils import ImageUtils

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(cfg.SENTENCE_TRANSFORMERS_MODEL)
model = AutoModel.from_pretrained(cfg.SENTENCE_TRANSFORMERS_MODEL)


def get_embedding(text):
    """
    Generate an embedding for the given text using the transformer model.
    """
    inputs = tokenizer(text, return_tensors="pt",
                       truncation=True, padding=True)
    outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1)
    return embedding.detach().numpy().tolist()[0]


# MongoDB client setup
client = MongoClient(cfg.MONGO_URI)
db = client[cfg.DB_NAME]
stories_collection = db[cfg.STORIES_COLLECTION_NAME]
images_collection = db[cfg.IMAGES_COLLECTION_NAME]
stories_corpus_file = cfg.STORIES_CORPUS
images_corpus_file = cfg.IMAGES_CORPUS

# --- Ingest Stories ---
json_path = os.path.join("corpus", stories_corpus_file)
with open(json_path, "r") as f:
    stories = json.load(f)

for story in stories:
    text = story['story']
    story["embedding"] = get_embedding(text)

stories_collection.insert_many(stories)
print("Stories Data inserted successfully!")

# --- Ingest Images ---
public_images = []
csv_path = os.path.join("corpus", images_corpus_file)
with open(csv_path, "r", encoding="utf-8") as f:
    images = csv.DictReader(f)
    for image in images:
        if (
            image['Is Highlight'] == "True"
            and image['Is Timeline Work'] == "True"
            and image['Is Public Domain'] == "True"
        ):
            public_image = {
                'id': image['Object ID'],
                'description': ImageUtils.image_attribute(image),
            }
            public_image["embedding"] = get_embedding(public_image['description'])
            public_images.append(public_image)

images_collection.insert_many(public_images)
print("Images Data inserted successfully!")
