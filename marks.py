from flask import Blueprint, request, jsonify
from flask import session
import csv
import uuid
import time
import re

marks_bp = Blueprint('marks', __name__)

@marks_bp.route('/create', methods=['POST'])
def create_mark():
    marks = marks_bp.marks
    if "user" not in session:
        return "mf ion even know you 😭😭", 401
    data = request.get_json()
    mark_body = data.get('body')
    mark_id = str(uuid.uuid4())
    mark_timestamp = int(time.time())
    if not mark_body:
        return "no body", 400
    
    marks.insert_one({
        "id": mark_id,
        "timestamp": mark_timestamp,
        "body": mark_body,
        "user": session["user"]
    })
    
    return jsonify({
        "body": mark_body,
        "id": mark_id,
        "timestamp": mark_timestamp,
    })

@marks_bp.route('/view', methods=['GET'])
def view_marks():
    if "user" not in session:
        return "mf ion even know you 😭😭", 401
    user_marks = []
    for mark in marks_bp.marks.find({"user": session["user"]}, sort=[("timestamp", -1)]):
        user_marks.append({
            "id": mark['id'],
            "timestamp": mark['timestamp'],
            "body": mark['body'],
        })
    return jsonify(user_marks)

@marks_bp.route('/delete', methods=['DELETE'])
def delete_mark():
    if "user" not in session:
        return "mf ion even know you 😭😭", 401
    data = request.get_json()
    mark_id = data.get('id')
    if not mark_id:
        return "what mark brah", 400
    
    marks_bp.marks.delete_one({"id": mark_id, "user": session["user"]})
    return "dat mf gone", 200

@marks_bp.route('/search', methods=['GET'])
def search_marks():
    if "user" not in session:
        return "what mark brah", 400
    query = request.args.get('query')
    if not query:
        return "how you gonna find nothing brah", 400
    results = []
    safe_query = re.escape(query)
    for mark in marks_bp.marks.find({
        "user": session["user"],
        "body": {
            "$regex": safe_query,
            "$options": "i"
        }
    }).sort("timestamp", -1):
        results.append({
            "id": mark['id'],
            "timestamp": mark['timestamp'],
            "body": mark['body'],
        })

    print(results)

    results.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(results)

@marks_bp.route('/edit', methods=['PUT'])
def edit_mark():
    if "user" not in session:
        return "mf ion even know you 😭😭", 401
    data = request.get_json()
    mark_id = data.get('id')
    new_body = data.get('body')
    if not mark_id:
        return "what mark brah", 400
    marks_bp.marks.update_one({"id": mark_id, "user": session["user"]}, {"$set": {"body": new_body}})
    return "bet", 200