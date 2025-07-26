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
    db = firestore.client()
    doc_ref = db.collection('articles').document('메인콘텐츠')
    doc = doc_ref.get()
    if not doc.exists:
        article_content = "아직 콘텐츠가 없습니다."
    else:
        article_content = doc.to_dict().get('content', "내용이 없습니다.")
    return render_template('index.html', article_content=article_content)

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
