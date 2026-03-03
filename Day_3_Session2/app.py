from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def home():
    return "home"
@app.route("/show/<name>")
def show(name):
    return render_template("index.html",name=name)
@app.route("/about/<int:age>")
def about(age):
    return render_template("agecheck.html",age = age)
@app.route("/auth/<role>")
def page(role):
    return render_template("admin.html",role=role)
@app.route("/courses")
def courses():
    course_names = ["Btech","B.Pharma","BCA","BCom","BBA","MBA","MCom","M.Tech","Diploma"]
    return render_template("course.html",names = course_names)
@app.route("/dict")
def my_dict():
    emp = [
        {"name":"ajay","role":"admin","email":"ajay@gmail.com"},
        {"name":"vasant","role":"manager","email":"vasant@gmail.com"},
        {"name":"kumar","role":"play","email":"kumar@gmail.com"}
    ]
    return render_template("dictionary.html",mydict = emp)
if __name__=="__main__":
    app.run(debug = True)