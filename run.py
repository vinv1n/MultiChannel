import argparse
from app import create_app
from flask import render_template


def main():
    parser = argparse.ArgumentParser(description="Multichannel")  # TODO write better description
    parser.add_argument("--disable-bots", help="Disables bot from running on background", action="store")

    args = parser.parse_args()
    app = create_app(args)
    app.run(host='0.0.0.0', port=5000)
    print("here")

if __name__ == '__main__':
    main()
