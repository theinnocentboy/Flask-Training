from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
db = SQLAlchemy(app)

class Inventory(db.Model):
    s_no = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Integer,nullable=False)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, default = datetime.now(), onupdate= datetime.now())

@app.route("/")
def home():
    return "<h1>Home Page</h1>"

@app.route("/add/<name>/<price>/<quantity>")
def add(name,price,quantity):
    product = Inventory(name=name,price=price,quantity=quantity)
    db.session.add(product)
    db.session.commit()
    return f"Data of {product.name} added!"

@app.route("/update/<num>/<name>/<price>/<quantity>")
def update(num,name,price,quantity):
    product = Inventory.query.get(num)
    product.name = name
    product.price = price
    product.quantity = quantity
    return f"{product.name} is updated"

@app.route("/delete/<num>")
def delete(num):
    product = Inventory.query.get(num)
    db.session.delete(product)
    db.session.commit()
    return f"{product.name} is deleted"

@app.route("/show_all")
def show_all():
    products = Inventory.query.all()
    return render_template("inventory.html",products=products)

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)