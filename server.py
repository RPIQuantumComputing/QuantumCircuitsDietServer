from flask import Flask, abort, request, send_from_directory
import os
import json
import ssl
import sqlite3
import requests
import base64
import os

import UserLogins


#from OpenSSL import SSL

app = Flask(__name__)


host = "127.0.0.1"
port = 5000
debug = False


#########
# BASIC #
#########
@app.route("/favicon.ico", methods=['GET'])
def favicon():
    #app.send_static_file('favicon.ico')
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsoft.icon')

##########
# CUSTOM #
##########
@app.route("/", methods=['GET','POST'])
def index():
    return "Quantum Circits"

@app.route("/api/login", methods=['POST'])
def api_login():
    return 404 # wrapped_api_login(request)

@app.route("/api/download", methods=['GET'])
def api_download():
    pass


##########
# DRIVER #
##########

@app.before_request
def limit_remote_addr():

    #if request.remote_addr not in trusted_ips:
    #    abort(404)  # Not Found
    pass

@app.after_request
def display_ip(response):
    forwarded_for = request.headers.get('X-Forwarded-For')
    remote_addr = request.remote_addr
    if forwarded_for:
        remote_addr = forwarded_for.split(',')[0]
    line = '{} - - "{}"\n'.format(
        remote_addr,
        request.user_agent
    )

    print("\n",line,end="")
    #print(request.headers)
    return response


if __name__ == "__main__":
    ssl_context = None
    app.run(host=host, port=port, debug=debug, ssl_context=ssl_context)

