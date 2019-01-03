from flask import render_template, redirect

# redirect to webui
def index():
    return redirect(location="/webui/login", code=302)