from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.secret_key = "litchi"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    status = db.Column(
        db.Enum('pending','in_progress','completed',name="task_status"),
        default='pending',
        nullable=False
    )


def validate_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "name" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def is_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if "name" not in session:
            return redirect(url_for("login"))

        user = User.query.filter_by(name=session["name"]).first()

        if user.role != "admin":
            return "Unauthorized"

        return f(*args, **kwargs)

    return wrapper


def redirect_if_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if "name" in session:
            return redirect(url_for("tasks"))

        return f(*args, **kwargs)

    return wrapper


@app.route("/")
def index():
    return "<h1>Home</h1>"


@app.route("/user/register", methods=["GET","POST"])
@redirect_if_logged_in
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        existing = User.query.filter_by(email=email).first()

        if existing:
            return "User already exists"

        role = "admin" if name == "admin" else "user"

        new_user = User(
            name=name,
            email=email,
            password=hashed,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("user/User_Register.html")

@app.route("/user/login", methods=["GET","POST"])
@redirect_if_logged_in
def login():

    if request.method == "POST":

        name = request.form["name"]
        password = request.form["password"]

        user = User.query.filter_by(name=name).first()

        if not user or not bcrypt.check_password_hash(user.password,password):
            return "Invalid login"

        session["name"] = user.name

        return redirect(url_for("tasks"))

    return render_template("user/userLogin.html")


@app.route("/tasks")
@validate_user
def tasks():

    user = User.query.filter_by(name=session["name"]).first()

    tasks = Task.query.all()

    return render_template("task.html",tasks=tasks,user=user)


@app.route("/add_task",methods=["POST"])
@validate_user
def add_task():

    title = request.form["title"]
    description = request.form["description"]

    user = User.query.filter_by(name=session["name"]).first()

    new_task = Task(
        title=title,
        description=description,
        user_id=user.id,
        status="pending"
    )

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for("tasks"))


@app.route("/update_task/<int:task_id>",methods=["POST"])
@validate_user
def update_task(task_id):

    task = Task.query.get_or_404(task_id)

    task.status = request.form["status"]

    db.session.commit()

    return redirect(url_for("tasks"))



@app.route("/delete_task/<int:task_id>",methods=["POST"])
@validate_user
def delete_task(task_id):

    task = Task.query.get_or_404(task_id)

    db.session.delete(task)

    db.session.commit()

    return redirect(url_for("tasks"))



@app.route("/logout")
def logout():

    session.pop("name",None)

    return redirect(url_for("login"))



@app.route("/user/show")
def show():

    user = User.query.all()

    return render_template("user/userShow.html",user=user)



if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)