from flask import render_template, redirect, url_for, request
from firebase_admin import firestore
from . import main

@main.route('/edit')
def edit():
    if "title" in request.args:
        db = firestore.client()
        article_title = request.args["title"]
        doc_ref = db.collection('articles').document(article_title)
        doc = doc_ref.get()
        if not doc.exists:
            return "ARTICLE NOT EXISTS!"
        return render_template('edit.html',article_content=doc.to_dict()["content"],article_title=article_title)
    return "NOT A VAILD PARAMETER!"

@main.route('/api/edit', methods=['POST'])
def apiEdit():
    if "article_content" in request.form and "article_title" in request.form:
        db = firestore.client()
        doc_ref = db.collection('articles').document(request.form["article_title"])
        doc = doc_ref.get()
        if not doc.exists:
            return "ARTICLE NOT EXISTS!"
        doc_ref.update({"content": request.form["article_content"]})
        return redirect(url_for('main.index'))
    return "NOT A VAILD PARAMETER!"