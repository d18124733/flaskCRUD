from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
app.app_context().push()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    students = Student.query.all()
    return render_template("home.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def create_student():
    if request.method == "GET":
        return render_template("add.html")
    else:
        name = request.form["name"]
        email = request.form["email"]
        student = Student(name=name, email=email)
        db.session.add(student)
        db.session.commit()
        return redirect("/add")

if __name__ == "__main__":
    app.run(debug=True)