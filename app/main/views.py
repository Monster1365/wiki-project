from flask import render_template, request, session
from firebase_admin import firestore
from . import main

@main.route('/')
def index():
    if "token" in session:
        return render_template('index.html')
    return "로그인 필요"

@main.route('/article')
def article():
    db = firestore.client()
    title = request.args.get('title')
    doc_ref = db.collection('articles').document(title)
    doc = doc_ref.get()
    if not doc.exists:
        return "ARTICLE NOT EXISTS!"
    return render_template('index.html',article_content=doc.to_dict()["content"])