#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import yaml

from flask import Flask
from flask import request

from two1.lib.wallet.two1_wallet import Wallet
from two1.lib.bitserv.flask import Payment

from bitroute import bitroute

app = Flask(__name__)

# setup wallet
wallet = Wallet()
payment = Payment(app, wallet)

# hide logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/manifest')
def manifest():
    """Provide the app manifest to the 21 crawler.
    """
    with open('./manifest.yaml', 'r') as f:
        manifest = yaml.load(f)
    return json.dumps(manifest)


@app.route('/')
@payment.required(10)
def traceroute():
    """ Runs traceroute on the provided url

    Returns: HTTPResponse 200 with a json containing the traceroute info.
    HTTP Response 400 if no uri is specified or the uri is malformed/cannot be tracerouted.
    """
    try:
        uri = request.args['uri']
    except KeyError:
        return 'HTTP Status 400: URI query parameter is missing from your request.', 400

    try:
        data = bitroute(uri)
        response = json.dumps(data, indent=4, sort_keys=True)
        return response
    except ValueError as e:
        return 'HTTP Status 400: {}'.format(e.args[0]), 400


if __name__ == '__main__':
    print("Server running...")
    app.run(host='0.0.0.0', port=6003)
