import argparse
import logging
import OpenSSL
import os
import ssl

from app import create_app
from flask import render_template, request, redirect
from app.database.db_handler import database_handler

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Multichannel")  # TODO write better description
    parser.add_argument("--disable-bots", help="Disables bot from running on background", action="store")

    args = parser.parse_args()
    app = create_app(args)

    # certs
    #context = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    #context = (cert, key)
    #context = ("/api/cert.pem", "/api/key.pem")
    # NOTE will break dev env
    app.run(ssl_context=context, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
