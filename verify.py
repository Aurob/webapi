from flask import Flask, request
import requests
import jwt
import json
import os
app = Flask(__name__)


# The Application Audience (AUD) tag for your application
POLICY_AUD = 'c4caae125a9a145bf660dcd5fa139f15008b977bb25082c7371763e27432fe25' #os.getenv("POLICY_AUD")

# Your CF Access team domain
TEAM_DOMAIN = 'https://audev.cloudflareaccess.com' #os.getenv("TEAM_DOMAIN")
CERTS_URL = "{}/cdn-cgi/access/certs".format(TEAM_DOMAIN)

def _get_public_keys():
    """
    Returns:
        List of RSA public keys usable by PyJWT.
    """
    r = requests.get(CERTS_URL)
    public_keys = []
    jwk_set = r.json()
    for key_dict in jwk_set['keys']:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key_dict))
        public_keys.append(public_key)
    return public_keys

def verify_token(f):
    """
    Decorator that wraps a Flask API call to verify the CF Access JWT
    """
    def wrapper():
        token = ''
        if 'CF_Authorization' in request.cookies:
            token = request.cookies['CF_Authorization']
        else:
            return "missing required cf authorization token", 403
        keys = _get_public_keys()

        # Loop through the keys since we can't pass the key set to the decoder
        valid_token = False
        for key in keys:
            try:
                # decode returns the claims that has the email when needed
                jwt.decode(token, key=key, audience=POLICY_AUD, algorithms=['RS256'])
                valid_token = True
                break
            except:
                pass
        if not valid_token:
            return "invalid token", 403

        return f()
    return wrapper


@app.route('/hello')
@verify_token
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)