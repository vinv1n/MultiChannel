import argparse
import logging

from app import create_app
from flask import render_template

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)-8s %(message)s', datefmt="%a, %d %b %Y %H:%M:%S")  # TODO reformat
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

def main():
    parser = argparse.ArgumentParser(description="Multichannel")  # TODO write better description
    parser.add_argument("--disable-bots", help="Disables bot from running on background", action="store")

    args = parser.parse_args()
    app = create_app(args)
    app.run(host='0.0.0.0', port=5000)
    print("here")

if __name__ == '__main__':
    main()
