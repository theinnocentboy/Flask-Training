from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date_create = db.Column(db.DateTime, default= datetime.now(timezone.utc))
    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"
@app.route('/')
def hello():
    return"Home"
@app.route('/add')
def add():
    todo = Todo(title="my task",desc = "demo insert")
    db.session.add(todo)
    db.session.commit()
    print(todo)
    return 'Data Added!'
@app.route("/show")
def show():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)
if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)