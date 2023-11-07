from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Подключение к MongoDB
client = MongoClient(os.environ['DB_URI'])
db = client.mydatabase


@app.route('/<key>', methods=['GET', 'POST', 'PUT'])
def manage_item(key):
    collection = db.myappcollection
    if request.method == 'POST':
        value = request.json['value']
        collection.insert_one({'_id': key, 'value': value})
        return jsonify({'key': key, 'value': value}), 201
    elif request.method == 'PUT':
        new_value = request.json['value']
        collection.update_one({'_id': key}, {'$set': {'value': new_value}})
        return jsonify({'key': key, 'value': new_value}), 200
    elif request.method == 'GET':
        item = collection.find_one({'_id': key})
        if item:
            return jsonify({'key': key, 'value': item['value']}), 200
        else:
            return jsonify({'error': 'Key not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
