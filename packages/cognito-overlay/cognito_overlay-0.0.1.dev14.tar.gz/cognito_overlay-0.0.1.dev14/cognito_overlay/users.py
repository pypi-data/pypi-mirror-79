from flask import Blueprint, request, jsonify
import boto3
from ._config import CLIENT_ID

users = Blueprint('users', __name__)
_client = boto3.client('cognito-idp')

@users.route('/users', methods=['POST'])
def create_user():
  req_data = request.get_json(force=True)
  username = req_data.get('username', req_data.get('email', ''))
  password = req_data.get('password', '')
  password_confirmation = req_data.get('password_confirmation', '')
  if not username:
    return jsonify({'error': 'username is required'}), 400
  if not password:
    return jsonify({'error': 'password is required'}), 400
  if not password_confirmation:
    return jsonify({'error': 'password confirmation is required'}), 400
  if password != password_confirmation:
    return jsonify({'error': 'password and password confirmation do not match'}), 400
  
  result = _client.sign_up(
    ClientId=CLIENT_ID,
    Username=username,
    Password=password
  )

  # TODO: Recover from password errors and return friendly errors
  # TODO: Recover from duplicate users

  return result, 200

@users.route('/signin', methods=['POST'])
def sign_in():
  req_data = request.get_json(force=True)
  username = req_data.get('username', req_data.get('email', ''))
  password = req_data.get('password', '')

  try:
    result = _client.initiate_auth(
      AuthFlow='USER_PASSWORD_AUTH',
      AuthParameters={
        'USERNAME': username,
        'PASSWORD': password
      },
      ClientId=CLIENT_ID
    )
  except (_client.exceptions.NotAuthorizedException, _client.exceptions.UserNotFoundException) as err:
    print(err)
    return jsonify({'error': 'incorrect password or user not found'}), 400
  # TODO: Handle not confirmed error

  if result:
    print(result)
    # TODO: Return JSON with token from "AuthenticationResult.AccessToken"
    return '', 204

@users.route('/signout', methods=['POST'])
def sign_out():
  pass

@users.route('/users/confirm', methods=['PUT'])
def confirm():
  req_data = request.get_json(force=True)
  username = req_data.get('username', '')
  confirmation_code = req_data.get('confirmation_code', '')

  result = _client.confirm_sign_up(
    ClientId=CLIENT_ID,
    Username=username,
    ConfirmationCode=confirmation_code
  )

  return '', 204

@users.route('/password/start', methods=['PUT'])
def start_password_change():
  req_data = request.get_json(force=True)
  username = req_data.get('username', '')

  result = _client.forgot_password(
    ClientId=CLIENT_ID,
    Username=username
  )

  return '', 204

@users.route('/password/confirm', methods=['PUT'])
def complete_password_change():
  req_data = request.get_json(force=True)
  username = req_data.get('password', '')
  confirmation_code = req_data.get('confirmation_code', '')
  password = req_data.get('password', '')

  result = _client.confirm_forgot_password(
    ClientId=CLIENT_ID,
    Username=username,
    ConfirmationCode=confirmation_code,
    Password=password
  )

  return '', 204