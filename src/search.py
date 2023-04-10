

from flask import Blueprint, request, render_template
from src.auth import login_required
from cs50 import SQL
import os

search = Blueprint("search", __name__, static_folder="static", template_folder="templates")

db = SQL("sqlite:///src/main.db")

@search.route("/search", methods=["GET", "POST"])
@login_required
def landing():
    if request.method == "GET":
        return render_template("search.html")
    else:
        target_uname = request.form.get("username")
        match=db.execute("SELECT * FROM users WHERE username=:target_uname", target_uname=target_uname)
        if not match:
            return render_template("search.html", method="POST")
        dp = "static/dp/" + match[0]['username'] + "." + match[0]['dp']
        if not os.path.exists(dp):
            dp = "../static/dp/"+"default.png"
        else:
            dp = "../static/dp/" + match[0]['username'] + "." + match[0]['dp']
        return render_template("search.html", method="POST", dp=dp, results=match)
