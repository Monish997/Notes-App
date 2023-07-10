from flask import Blueprint, render_template, request

main = Blueprint("main", __name__)


@main.route("/")
def home():
    # fmt: off
    reviews = [
        {"name": "John Doe", "content": "I love using the Notes App. It helps me stay organized and productive. Highly recommended!"},
        {"name": "Jane Smith", "content": "This app has become an essential part of my daily routine. It's simple yet powerful. Great job!"},
        {"name": "David Williams", "content": "The Notes App has made note-taking a breeze. I can access my notes from anywhere. Excellent work!"}
    ]
    # fmt: on
    return render_template("home.html", reviews=reviews)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
