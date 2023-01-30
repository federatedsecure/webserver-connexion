#!/usr/bin/env python3

"""
the main module
"""

import sys
import connexion
import waitress

from flask import current_app

from federatedsecure.server.bus import Bus
from encoder import JSONEncoder


def main():
    """runs the webserver"""

    # enable the following line to log endpoint traffic
    # logging.basicConfig(level=logging.INFO)

    port = 8080
    for arg in sys.argv:
        if arg[:7] == "--port=":
            port = int(arg[7:])

    bus = Bus()

    app = connexion.App(__name__, specification_dir='openapi/')
    app.app.json_encoder = JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Federated Secure Computing'},
                pythonic_params=True)

    with app.app.app_context():
        current_app.bus = bus

    @app.app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE')
        return response

    waitress.serve(app, host="0.0.0.0", port=port)


if __name__ == '__main__':
    main()
