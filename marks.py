from flask import Blueprint, request, jsonify
from flask import session
import csv
import uuid
import time

marks_bp = Blueprint('marks', __name__)

@marks_bp.route('/create', methods=['POST'])
def create_mark():
    if "user" not in session:
        return "mf ion even know you 😭😭", 401
    data = request.get_json()
    mark_body = data.get('body')
    if not mark_body:
        return "no body", 400
    with open(f'marks_db/{session["user"]}.csv', 'a', newline='') as markfile:
        writer = csv.DictWriter(markfile, fieldnames=['id', 'timestamp','body'])
        writer.writerow({'id': str(uuid.uuid4()), 'timestamp': int(time.time()), 'body': mark_body})
    
    return "mark created", 201

@marks_bp.route('/view', methods=['GET'])
def view_marks():
    if "user" not in session:
        return "mf ion even know you 😭😭", 401
    marks = []
    with open(f'marks_db/{session["user"]}.csv', 'r') as markfile:
        reader = csv.DictReader(markfile)
        for row in reader:
            marks.append({
                "id": row['id'],
                "timestamp": int(row['timestamp']),
                "body": row['body'],
            })
    return jsonify(marks)

@marks_bp.route('/delete', methods=['DELETE'])
def delete_mark():
    if "user" not in session:
        return "mf ion even know you 😭😭", 401
    data = request.get_json()
    mark_id = data.get('id')
    if not mark_id:
        return "what mark brah", 400
    
    marks = []
    with open(f'marks_db/{session["user"]}.csv', 'r') as markfile:
        reader = csv.DictReader(markfile)
        for row in reader:
            if row['id'] != mark_id:
                marks.append(row)
    with open(f'marks_db/{session["user"]}.csv', 'w', newline='') as markfile:
        writer = csv.DictWriter(markfile, fieldnames=['id', 'timestamp','body'])
        writer.writeheader()
        for mark in marks:
            writer.writerow(mark)
    return "dat mf gone", 200

@marks_bp.route('/search', methods=['GET'])
def search_marks():
    if "user" not in session:
        return "what mark brah", 400
    query = request.args.get('query')
    if not query:
        return "how you gonna find nothing brah", 400
    results = []
    with open(f'marks_db/{session["user"]}.csv', 'r') as markfile:
        reader = csv.DictReader(markfile)
        for row in reader:
            if query in row['body']:
                results.append({
                    "id": row['id'],
                    "timestamp": int(row['timestamp']),
                    "body": row["body"],
                })
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
    marks = []
    with open(f'marks_db/{session["user"]}.csv', 'r') as markfile:
        reader = csv.DictReader(markfile)
        for row in reader:
            if row['id'] == mark_id:
                row['body'] = new_body
            marks.append(row)
    with open(f'marks_db/{session["user"]}.csv', 'w', newline='') as markfile:
        writer = csv.DictWriter(markfile, fieldnames=['id', 'timestamp','body'])
        writer.writeheader()
        for mark in marks:
            writer.writerow(mark)
    return "bet", 200