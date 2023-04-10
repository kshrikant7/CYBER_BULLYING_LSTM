# MIT License


from flask import Blueprint, request, render_template, redirect, session
from src.auth import login_required
from src.helpers import error, UserInfo
from cs50 import SQL
from tensorflow.keras.models import load_model
from . import cmodel

home = Blueprint("home", __name__, static_folder="static", template_folder="templates")

db = SQL("sqlite:///src/main.db")
# Load the ML model and initiate Mindhunters
model = load_model('src/cmodel.h5')
word_to_index, max_len = cmodel.init()

@home.route("/", methods=["GET", "POST"])
@login_required
def index():
    userInfo, dp = UserInfo(db)
    if request.method == "GET":
        get_posts = db.execute("SELECT * FROM :tablename", tablename=userInfo['username'])
        get_posts = add_publisher(get_posts, userInfo['username'])
        follow_metadata = db.execute("SELECT following FROM :tablename", tablename=userInfo["username"]+'Social')
        posts_metadata = {userInfo['username']:dp}
        for following in follow_metadata:
            following_posts = db.execute("SELECT * FROM :tablename", tablename=following['following'])
            following_posts = add_publisher(following_posts, following['following'])
            other_user_info, other_user_dp = UserInfo(db, following['following'])
            posts_metadata[following['following']] = other_user_dp
            get_posts.extend(following_posts)
        get_posts.sort(key=get_timestamp, reverse=True)
        if get_posts:
            return render_template("index.html", posts=get_posts, posts_metadata=posts_metadata, dp=dp, user=userInfo, reputation = ((userInfo['score']/userInfo['total'])*10))
        else:
            return render_template("index.html")
    else:
        post_text = request.form.get("post")
        if not post_text:
            return redirect("/")
        text = [cmodel.clean_text(post_text)]
        text = cmodel.sentences_to_indices(text, word_to_index, max_len)
        ans = model.predict(text)[0][0]
        db.execute("INSERT INTO :tablename ('text', 'nature') VALUES (:post_text, :score)", tablename=userInfo['username'], post_text=post_text, score=str(ans))
        if (ans < 0.4):
            score = (0.4 - ans)
            total = "{:.2f}".format(userInfo['total'] + score)
            good_score = "{:.2f}".format(userInfo['score'] + score)
            db.execute("UPDATE users SET score=:score, total=:total WHERE id=:user_id", score = good_score, total = total, user_id = session["user_id"])
            return redirect("/")
        else:
            score = (ans - 0.4)
            total = "{:.2f}".format((userInfo['total'] + score))
            db.execute("UPDATE users SET total=:total WHERE id=:user_id", total = total, user_id = session["user_id"])
            return redirect("/")

@home.route("/about", methods=["GET"])
@login_required
def about():
    return render_template("about.html")

def get_timestamp(post):
    return post.get('timestamp')

def add_publisher(posts, publisher):
    for item in posts:
        item["publisher"] = publisher
    return posts
