import os
from flask import Flask, request,jsonify # type: ignore
from dotenv import load_dotenv # type: ignore
import pymongo # type: ignore

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')

if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is not set")

try:
    client = pymongo.MongoClient(MONGO_URL)
    client.admin.command('ping')  # Test the connection
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

    
db = client.test

collection = db['flask-tutorial']

app = Flask(__name__)

@app.route('/')
def index():
    return "backend is running!"

@app.route('/submit', methods=['POST'])
def submit():
    try:
        from_data = request.json
        if not from_data:
            return jsonify({"error": "No data provided"}), 400

        # Log the data being inserted
        print("Inserting data:", from_data)

        collection.insert_one(from_data)
        return "Data stored in MongoDB"
    except Exception as e:
        print(f"Error inserting data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/view')
def view():
    try:
        data = collection.find()
        data = list(data)

        for d in data:
            print(d)
            del d['_id']  # Remove MongoDB's `_id` field

        return jsonify({'data': data})
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=9000,debug=True)