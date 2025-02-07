from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Blog Post Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts])

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = BlogPost(
        title=data['title'],
        content=data['content']
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify(post.to_dict())

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
