from flask import render_template

# functions for main view

def index():
    return render_template("index.html")