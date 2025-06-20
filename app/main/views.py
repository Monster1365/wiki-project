from flask import render_template, current_app, request
from firebase_admin import firestore
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/article')
def article():
    db = firestore.client()
    title = request.args.get('title')
    doc_ref = db.collection('articles').document(title)
    doc = doc_ref.get()
    if not doc.exists:
        return "ARTICLE NOT EXISTS!"
    return render_template('index.html',article_content=doc.to_dict()["content"])