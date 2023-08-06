from flask import Blueprint, request, jsonify, current_app
from google_auth_oauthlib.flow import Flow
from base64 import urlsafe_b64encode
import json

oauth = Blueprint('oauth', __name__)

@oauth.route('/oauth/start', methods=['POST'])
def oauth_start():
  flow = Flow.from_client_config(
    current_app.config['AUTH_SA_SECRET_CONTENTS'],
    ['https://www.googleapis.com/auth/userinfo.email']
  )
  flow.redirect_uri = f'https://{current_app.config["AUTH_ROOT"]}/oauth/token'
  authorization_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
  return jsonify({
    'redirect_url': authorization_url
  }), 200

@oauth.route('/oauth/exchange', methods=['POST'])
def oauth_exchange():
  req_data = request.get_json(force=True)
  code = req_data.get('code', '')
  state = req_data.get('state', '')
  if not code:
    return jsonify({'error': 'Must provide authorization code'}), 400
  if not state:
    return jsonify({'error': 'Must provide state'}), 400
  flow = Flow.from_client_config(
    current_app.config['AUTH_SA_SECRET_CONTENTS'],
    ['https://www.googleapis.com/auth/userinfo.email'],
    state=state
  )
  flow.fetch_token(code=code)
  credentials = flow.credentials
  assembled_credentials = {
    'token': credentials.token,
    'refresh_token': credentials.refresh_token
  }
  return jsonify({
    'token': urlsafe_b64encode(json.stringify(assembled_credentials))
  }), 200
