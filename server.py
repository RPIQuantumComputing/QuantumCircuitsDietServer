from flask import Flask, abort, request, send_from_directory
import os
import json
import ssl
import sqlite3
import requests
import base64
import os

import UserLogin
import FileTransfer


#from OpenSSL import SSL

app = Flask(__name__)


host = "127.0.0.1"
port = 5000
debug = False

def verify_login(func):
    def decorator(*args, **kwargs):
        session = request.headers.get('session')
        if(not UserLogins.verify_session(session)):
            return abort(401, description="Unauthorized")
        return func(*args, **kwargs)
    decorator.__name__ = func.__name__
    return decorator

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
    username = request.body.get('username')
    hashed_pw = request.body.get('hashed_password')
    
    return UserLogin.user_login(username,hashed_pw)


@app.route("/api/download", methods=['GET'])
@verify_login
def api_download():
    session = request.headers.get('session')

    username = UserLogin.get_username_from_session(session)
    file_name = request.body.get('file_name')

    return FileTransfer.get_file(username,fole_name)


@app.route("/api/upload", methods=['POST'])
@verify_login
def api_upload():

    session = request.headers.get('session')

    username = UserLogin.get_username_from_session(session)
    circuit_json = request.body.get('circuit_json')
    
    return FileTransfer.add_file(username,circuit_json)


##########
# DRIVER #
##########

@app.before_request
def limit_remote_addr():
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

