from pymongo import MongoClient
from datetime import datetime

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['product_reviews']
collection = db['reviews']

def save_to_mongodb(reviews, website):
    try:
        # Add timestamp and website info to each review
        for review in reviews:
            review['scraped_at'] = datetime.now()
            review['website'] = website.lower()
        
        # Insert into MongoDB
        if reviews:
            result = collection.insert_many(reviews)
            return len(result.inserted_ids)
        return 0
    except Exception as e:
        print(f"Error saving to MongoDB: {str(e)}")
        return 0

def get_reviews_from_mongodb(website=None):
    try:
        query = {'website': website.lower()} if website else {}
        reviews = list(collection.find(query, {'_id': 0}))
        return reviews
    except Exception as e:
        print(f"Error fetching from MongoDB: {str(e)}")
        return []