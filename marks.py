from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask import session
import csv
import uuid

marks_bp = Blueprint('marks', __name__)

@marks_bp.route('/create', methods=['POST'])
def create_mark():
    if "user" not in session:
        return jsonify({
            "error": "mf ion even know you 😭😭",
            "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/who-is-he.gif"
        }), 401
    data = request.get_json()
    mark_url = data.get('url')
    mark_tags = data.get('tags')
    if not mark_url:
        return jsonify({
            "error": "fuh you even bookmarking without a url brah",
            "file": "illaddthislater"
        }), 400
    if type(mark_tags) != list:
        return jsonify({
            "error": "make ts a list brah",
            "file": "illaddthislater"
        }), 400
    
    with open(f'marks_db/{session["user"]}.csv', 'a', newline='') as markfile:
        writer = csv.DictWriter(markfile, fieldnames=['id','url', 'tags'])
        writer.writerow({'id': str(uuid.uuid4()), 'url': mark_url, 'tags': ",".join(mark_tags)})
    
    return jsonify({
        "message": "mark created successfully",
        "file": "illaddthislater"
    })

@marks_bp.route('/view', methods=['GET'])
def view_marks():
    if "user" not in session:
        return jsonify({
            "error": "mf ion even know you 😭😭",
            "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/who-is-he.gif"
        })
    marks = []
    with open(f'marks_db/{session["user"]}.csv', 'r') as markfile:
        reader = csv.DictReader(markfile)
        for row in reader:
            marks.append({
                "url": row['url'],
                "tags": row['tags'].split(",") if row['tags'] else []
            })
    return jsonify(marks)

@marks_bp.route('/delete', methods=['DELETE'])
def delete_mark():
    if "user" not in session:
        return jsonify({
            "error": "mf ion even know you 😭😭",
            "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/who-is-he.gif"
        })
    data = request.get_json()
    mark_id = data.get('id')
    if not mark_id:
        return jsonify({
            "error": "what mark brah",
            "file": "illaddthislater"
        })
    
    marks = []
    with open(f'marks_db/{session["user"]}.csv', 'r') as markfile:
        reader = csv.DictReader(markfile)
        for row in reader:
            if row['id'] != mark_id:
                marks.append(row)
    with open(f'marks_db/{session["user"]}.csv', 'w', newline='') as markfile:
        writer = csv.DictWriter(markfile, fieldnames=['id','url','tags'])
        writer.writeheader()
        for mark in marks:
            writer.writerow(mark)
    return jsonify({
        "message": "dat mf gone",
        "file": "illaddthislater"
    })

@marks_bp.route('/search', methods=['GET'])
def search_marks():
    if "user" not in session:
        return jsonify({
            "error": "mf ion even know you 😭😭",
            "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/who-is-he.gif"
        })
    query = request.args.get('query')
    if not query:
        return jsonify({
            "error": "how you gonna find nothing brah",
            "file": "illaddthislater"
        })
    results = []
    with open(f'marks_db/{session["user"]}.csv', 'r') as markfile:
        reader = csv.DictReader(markfile)
        for row in reader:
            if query in row['url'] or query in row['tags']:
                results.append({
                    "url": row["url"],
                    "tags": row["tags"].split(",") if row["tags"] else []
                })
    return jsonify(results)

@marks_bp.route('/edit_tags', methods=['PUT'])
def edit_mark():
    if "user" not in session:
        return jsonify({
            "error": "mf ion even know you 😭😭",
            "file": "https://raw.githubusercontent.com/tanmayrajk/slushies/refs/heads/main/memes/who-is-he.gif"
        })
    data = request.get_json()
    mark_id = data.get('id')
    new_tags = data.get('tags')
    if not mark_id:
        return jsonify({
            "error": "what mark brah",
            "file": "illaddthislater"
        })
    if type(new_tags) != list:
        return jsonify({
            "error": "make ts a list brah",
            "file": "illaddthislater"
        })
    marks = []
    with open(f'marks_db/{session["user"]}.csv', 'r') as markfile:
        reader = csv.DictReader(markfile)
        for row in reader:
            if row['id'] == mark_id:
                row['tags'] = ",".join(new_tags)
            marks.append(row)
    with open(f'marks_db/{session["user"]}.csv', 'w', newline='') as markfile:
        writer = csv.DictWriter(markfile, fieldnames=['id', 'url', 'tags'])
        writer.writeheader()
        for mark in marks:
            writer.writerow(mark)
    return jsonify({
        "message": "bet",
        "file": "illaddthislater"
    })