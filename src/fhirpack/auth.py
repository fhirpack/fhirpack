import json
import requests
from authlib.integrations.requests_client import OAuth2Session
import jwt
from fhirpack.constants import CONFIG

LOGGER = CONFIG.getLogger(__name__)


class Auth:
    @staticmethod
    def getToken(grant_type, params={}):

        token = None

        if grant_type == "password":
            token = Auth.tokenViaPasswordGrant(params)
        else:
            raise NotImplementedError

        return token

    @staticmethod
    def tokenViaPasswordGrant(params):
        username = CONFIG.get("OAUTH_USERNAME")
        password = CONFIG.get("OAUTH_PASSWORD")

        # this is a public client, no separate Client ID nor Client Secret shall be provided
        # https://www.oauth.com/oauth2-servers/client-registration/client-id-secret/
        clientId = username
        clientSecret = password

        # scope is recommended, but we often deal with non-standard claims and scopes
        # https://www.oauth.com/oauth2-servers/access-tokens/access-token-response/
        scope = None

        tokenEndpoint = CONFIG.get("OAUTH_TOKEN_ENDPOINT")

        # session = OAuth2Session(clientId, clientSecret)
        session = OAuth2Session(
            clientId,
            clientSecret,
            token_endpoint_auth_method="client_secret_basic",
        )

        # basicAuth = requests.auth.HTTPBasicAuth(
        # 	username,
        # 	password
        # )

        if params.get("preprocessTokenEndpointResponse"):
            session.register_compliance_hook(
                "access_token_response", params.get("tokenEndpointResponsePreprocessor")
            )

        token = session.fetch_token(
            tokenEndpoint,
            grant_type="password",
            # username=username,
            # password=password,
            method="get",
            # auth=basicAuth,
            # headers={'Accept': '*/*'}
            headers=params.get("headers"),
        )
        return token

    # ------------------------------------------------------------------------

    @staticmethod
    def oAuthTokenFromJWT(token):
        decodedToken = jwt.decode(
            token,
            # 'eyJuhbGc__SAMPLE__rS6cKsJ8vI',
            "secret",
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        data = dict(
            access_token=token, token_type="bearer", expires_in=decodedToken["exp"]
        )
        return lambda: data

    @staticmethod
    def parseSHIPTokenEndpointResponse(response):
        response.json = Auth.oAuthTokenFromJWT(response.text)
        return response


AUTH_PARAMS_PRESETS = {
    "ship": {
        "preprocessTokenEndpointResponse": True,
        "tokenEndpointResponsePreprocessor": Auth.parseSHIPTokenEndpointResponse,
        "headers": {"Acept": "*/*"},
    }
}

# print(Auth.getToken(
#     'password',
#     {
#       'preprocessTokenEndpointResponse': True,
#       'tokenEndpointResponsePreprocessor': Auth.parseSHIPTokenEndpointResponse,
#       'headers': {'Acept': '*/*'}
#       }
# )
# )
