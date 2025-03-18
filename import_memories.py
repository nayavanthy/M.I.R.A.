import os
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["MIRA"]  # Database name
memory_collection = db["long_term_memory"]  # Collection for storing memories

# Complete set of stored memories
memories = [
    # Goals & Aspirations

    # Relationships & Social Life

    # Current Emotional & Personal Growth

    # Interests & Hobbies

    # Routine & Discipline

    # Identity & Transformation

    # Music & Personal Expression

    # Academic & Professional Goals

    # Personal Philosophies & Motivations
]

# Insert memories into MongoDB (avoiding duplicates)
for memory in memories:
    if not memory_collection.find_one(memory):  # Prevent duplicate entries
        memory_collection.insert_one(memory)

print("All memories successfully imported into MongoDB.")
