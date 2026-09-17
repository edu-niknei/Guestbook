from flask import Flask, request, render_template
import json
import os
import datetime

app = Flask(__name__)
JSON_FILE = 'data.json'

def load_posts():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def spara_posts(posts):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=json.dumps(posts, indent=4, ensure_ascii=False))

@app.route('/submit', methods=['POST'])
def submit():
    posts = load_posts()
    posts.append({
        'name': request.form.get('name', ''),
        'message': request.form.get('message', ''),
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    spara_posts(posts)
    posts = load_posts()
    return render_template('index.html', posts=json.dumps(posts, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    app.run(debug=True)