from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///project.db"

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    role = db.Column(db.String(20))
    email = db.Column(db.String(50),unique=True,nullable = False)
    status = db.Column(db.Boolean, Default = True, nullable = False)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id),nullable = False)
    created_at = db.Column(db.Datetime)


@app.route("/")
def home():
    return "<h1>Home</h1>"
@app.route("/add/<name>/<role>/<email>")
def add(name,role,email):
    admin = User(name=name,role=role,email=email)
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Email already exist! {e}"
    return "Database Created!"

@app.route("/show")
def show():
    user = User.query.all()
    for items in user:
        print(items.id,":",items.name,":",items.role)
    print(user)
    return f"Data is in console"

@app.route("/filter/<identity1>/<identity2>")
def particular(identity1,identity2):
    usr = User.query.filter_by(id = identity1).first()
    #for primary key we dont use filterby function, we use get function and we dont use primary key name in the get function
    user = User.query.get(identity2)
    print(f"with filter function:{usr.name}, using get function for primary key {user.name}")
    return f"Only filtered id's data is printed on the console:{usr.name}, primary key use get function:{user.name}"
@app.route("/update/<int:id>/<name>/<role>/<email>")
def update(id,name,role,email):
    user = User.query.get(id)
    user.name = name
    user.role= role
    user.email = email
    db.session.commit()
    return f"Update value are {user.name}, {user.role} and {user.email}"
@app.route("/delete/<int:id>")
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
@app.route("/show_user/<name>")
def show_user(name):
    user = User.query.filter(User.name.like(f"{name}%")).all()
    return render_template("index.html",user = user)

@app.route("/byorder")
def show_order():
    #order_by query used to arrange the order of the data(desc() is for descending order) and for ascending remove the desc() function and put only order_by(User.<attribute>) 
    user = User.query.order_by(desc(User.id)).all()
    return render_template("index.html",user=user)

@app.route("/count")
def aggregate():
    user_count = User.query.count()
    return f"Total number of users are {user_count}"

@app.route("/post")
def post():
    user = User(name = "Alina",role="Spy", email = "alina13@jamil.com")
    db.session.add(user)
    db.session.commit()
    post = Post(title="Kuch BHi",content = "Haathi",user_id = user.id)
    db.session.add(post)
    db.session.commit()
    return f"Post title:{post.title} \n User_ID:{post.id}"

@app.route("/post_by/<name>")
def post_by(name):
    user = User.query.filter(User.name==name).first()
    if user:
        post = Post(title="News Post",content = "Breaking News",user_id = user.id)
        db.session.add(post)
        db.session.commit()
        return f"This post is created by {user.name}"
    return f"no user found"

@app.route("/show_post")
def show_post():
    page = request.args.get('page',1,type=int)
    posts = db.session.query(User,Post)\
    .join(User,Post.user_id == User.id)\
    .paginate(
        page = page,
        per_page = 2
    )
    for post in posts:
        print(f"{post.Post.title} by {post.User.name} ")
    return render_template("post.html",posts=posts)

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
