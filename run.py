from app import create_app
from flask import render_template

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
