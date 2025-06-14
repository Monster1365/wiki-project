from flask import Flask, request, Response, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/edit")
def edit():
    return render_template("edit.html")

@app.route("/change")
def change():
    return render_template("change.html")

@app.route("/discussion")
def discussion():
    return render_template("discussion.html")

if __name__ == "__main__":
    app.run(debug=True)