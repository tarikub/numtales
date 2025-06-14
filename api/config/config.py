import os

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "numtales_db"
DATABASE_NAME = DB_NAME  # Alias for clarity

# Collection Names
STORIES_COLLECTION_NAME = "stories"
IMAGES_COLLECTION_NAME = "images"

# Model Configuration
SENTENCE_TRANSFORMERS_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Data Files
STORIES_CORPUS = "numtales.json"
IMAGES_CORPUS = "MetObjects.txt"