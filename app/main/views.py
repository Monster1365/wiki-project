from flask import render_template, request, session, redirect, url_for
from functools import wraps
from firebase_admin import firestore
import random
from . import main

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return render_template("loginrequire.html", guest = True), 401
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
@login_required
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

@main.route('/randomArticle')
def randomArticle():
    db = firestore.client()
    title = request.args.get('title')
    docs_ref = db.collection('articles').get()
    doc = random.choice(docs_ref)
    return redirect(url_for("main.article", title=doc.id))