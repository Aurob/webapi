
from flask import Flask, jsonify, session, render_template, request, send_file, make_response, redirect, url_for
from flask_cors import CORS, cross_origin
from flask import Response
import base64
import io
import secrets
import os
from os import environ as env
from urllib.parse import quote_plus, urlencode
import json

import sys
from jinja2 import TemplateNotFound

import tools as T
from lib.verify import *

WEB_BASE = '/var/www/web/'

app = Flask(__name__)

CORS(app, support_credentials=True)
_accounts = {
    'admin': {
        'id': secrets.token_hex(14),
    }
}

app.config['SECRET_KEY'] = _accounts['admin']['id']

print(_accounts['admin']['id'])

subdomain = 'api'

def _render_template(template, **kwargs):
    try:
        return render_template(template, **kwargs)
    except TemplateNotFound:
        return render_template('404.html', **kwargs)


def try_template(subpath, args):
    print(f'{subpath}/index.html')
    return render_template(f'{subpath}/index.html', test=args)

def get_client_ip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    
def handle_result(result):
    if 'result' in result:
        if (isinstance(result['result'], dict)):
            if result['result']:
    
                if 'imgtype' in result['result']:
                    imgtype = result['result']['imgtype']
                else:
                    imgtype = 'image/jpeg'
                    
                if 'image' in result['result']:
                    # Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
                    # return send_file(io.BytesIO(base64.b64decode(result['result']['image'])), mimetype=imgtype)
                    
                    # return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + result['result']['image'] + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
                    # regular image repsonse
                    return send_file(io.BytesIO(result['result']['image']), mimetype=imgtype)
                if 'b64image' in result['result']:
                    # return send_file(result['result']['b64image'], mimetype=imgtype)
                    return send_file(io.BytesIO(base64.b64decode(result['result']['b64image'])), mimetype=imgtype)

                if 'raw' in result['result']: #  and 'data' in result['result']
                    return f'{result["result"]["raw"]}'

                if 'local' in result['result']:
                    # return send_file(result['result']['local'], mimetype='image/jpeg', cache_timeout=0)

                    response = make_response(send_file(result['result']['local'], mimetype='image/jpeg'))
                    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                    response.headers['Pragma'] = 'no-cache'
                    response.headers['Expires'] = '0'
                    return response
                
                if 'redirect' in result['result']:
                    return redirect(result['result']['redirect'])

                if 'audio' in result['result']:
                    return send_file(result['result']['audio'], mimetype='audio/mpeg')

                if 'template' in result['result']:
                    args = {}
                    if 'args' in result['result']:
                        args = result['result']['args']
                        
                    return _render_template(result['result']['template'], **args)
    
    if isinstance(result, dict):
        result = jsonify(result)
    
    return result
                
@app.route('/api/', strict_slashes=False)
@cross_origin(supports_credentials=True)
def index():
    return {'status': 'ok'}

@app.route('/api/<path:subpath>', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def api_redirect(subpath):

    try:
        
        args = {}
        if request.method == 'GET':
            args = request.args
            args = dict(args)
        else:
            args = request.get_json()
            
        request.args = args
        # First attempt to load the subpath as a template
        # if it fails, try to load it as a tool
        # if it fails, return an error

        try:
            return try_template(subpath, args)
        except TemplateNotFound:
            pass

        result = T.api(subpath, args, request)
        
        result = handle_result(result)
                
        return result
    except Exception as e:
        err_data = 'An unexpected error occurred'
        # if validate():
        err_data = f'{e}'
            
        return _render_template('error.html', error=err_data)

def downloadable(filename):
    if len(filename.split('.')) > 1:
        if os.path.exists(WEB_BASE + filename):
            return True
    return False

if __name__ == "__main__":
  app.run(host='localhost', port=8000, debug=True)
