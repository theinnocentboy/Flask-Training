from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///project.db"

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    role = db.Column(db.String(20))
    email = db.Column(db.String(50))

@app.route("/")
def home():
    return "<h1>Home</h1>"
@app.route("/add/<name>/<role>/<email>")
def add(name,role,email):
    admin = User(name=name,role=role,email=email)
    db.session.add(admin)
    db.session.commit()
    return "Database Created!"

@app.route("/show")
def show():
    user = User.query.all()
    for items in user:
        print(items.id,":",items.name,":",items.role)
    print(user)
    return f"Data is in console"
@app.route("/part/<identity1>/<identity2>")
def particular(identity1,identity2):
    usr = User.query.filter_by(id = identity1).first()
    #for primary key we dont use filterby function, we use get function and we dont use primary key name in the get function
    user = User.query.get(identity2)
    print(f"with filter function:{usr.name}, using get function for primary key {user.name}")
    return f"Only filtered id's data is printed on the console:{usr.name}, primary key use get function:{user.name}"
@app.route("/update/<id>/<name>/<role>/<email>")
def update(id,name,role,email):
    user = User.query.get(id)
    user.name = name
    user.role= role
    user.email = email
    db.session.commit()
    return f"Update value are {user.name}, {user.role} and {user.email}"
@app.route("/delete/<id>")
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return "deleted successfully!"
@app.route("/show_all")
def show_all():
    user = User.query.all()
    return render_template("index.html",user = user)
@app.route("/show_f")
def show_f():
    user = User.query.filter(User.email.like("%gmail.com")).all()
    return render_template("index.html",user = user )

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
