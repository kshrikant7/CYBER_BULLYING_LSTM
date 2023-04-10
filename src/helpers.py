

from flask import redirect, render_template, request, session
import os, random
from cs50 import SQL
from src import meme

def UserInfo(db, username = None):
    if not username:
        user_id_info = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])[0]
        dp = "static/dp/" + user_id_info['username'] + "." + user_id_info['dp']
        if not os.path.exists(dp):
            dp = "../static/dp/"+"default.png"
        else:
            dp = "../static/dp/" + user_id_info['username'] + "." + user_id_info['dp']
    else:
        user_id_info = db.execute("SELECT * FROM users WHERE username = :username", username = username)[0]
        dp = "static/dp/" + user_id_info['username'] + "." + user_id_info['dp']
        if not os.path.exists(dp):
            dp = "../static/dp/"+"default.png"
        else:
            dp = "../static/dp/" + user_id_info['username'] + "." + user_id_info['dp']
    return user_id_info, dp

def error(message, code=400):
    meme.meme(message)
    # The random variable prevents browser caching by adding a
    # randomly generated query string to each request for the dynamic image.
    print(message)
    return render_template("error.html", random=random.randint(1,32500),random1=random.randint(1,32500))