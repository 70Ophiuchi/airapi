import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = 'AirAPI'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code



def get_token_auth_header():

    auth = request.headers.get('Authorization', None)

    if not auth:
       raise AuthError({
           'code': 'authorization_header_missing',
           'description': 'Authorization header is expected'
       }, 401)

    parts = auth.split()

    if parts[0].casefold() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "bearer"'
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
        }, 401)
    
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token'
        })


def verify_decode_jwt(token):

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverf_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverf_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorizaton malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverf_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
                )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'desciption': 'Incorrect claims, please check audience and issuer'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'unable to parse authentication token.'
            }, 401)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key'
    }, 400)

def check_permissions(permission, payload):

    if permission not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not in JWT token'
        }, 401)
    
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True



def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator