import os
from endpoints import Endpoint


__version__ = '0.1.1'
__app_name__ = 'tinder_endpoints'
__author__ = 'Ramon Moraes'
__author_email__ = 'ramonmoraes8080@gmail.com'
__license__ = 'MIT'
__description__ = "Tinder's API endpoints"


TINDER_TOKEN = os.environ.get("TINDER_TOKEN")


#                                                                          Auth
# -----------------------------------------------------------------------------


class BaseAuthSmsEndpoint(Endpoint):
    domain = 'https://api.gotinder.com'
    headers = {
        'user-agent': 'Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)',
        'content-type': 'application/json',
    }


class AuthSmsSend(BaseAuthSmsEndpoint):

    path = '/v2/auth/sms/send'
    params = {
        'auth_type': 'sms'
    }


class AuthSmsValidate(BaseAuthSmsEndpoint):
    path = '/v2/auth/sms/validate'
    params = {
        'auth_type': 'sms'
    }


class AuthLoginSms(BaseAuthSmsEndpoint):
    path = '/v2/auth/login/sms'


#                                                                      Services
# -----------------------------------------------------------------------------


class ApiEndpoint(Endpoint):
    domain = 'https://api.gotinder.com'
    headers = {
        'app_version': '6.9.4',
        'platform': 'ios',
        'content-type': 'application/json',
        'User-agent': (
            'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:74.0)'
            ' Gecko/20100101 Firefox/74.0'
            ),
        'X-Auth-Token': None,
    }
    api_token = None

    def get_headers(self):
        headers = super(ApiEndpoint, self).get_headers()
        if not self.api_token:
            self.api_token = self.get_api_token()
        headers['X-Auth-Token'] = self.api_token
        return headers

    def get_api_token(self):
        """
        The TINDER_TOKEN can be either a path to a file with the token or the
        actual token
        """
        if os.path.isfile(TINDER_TOKEN):
            with open(os.path.expanduser(TINDER_TOKEN), 'r') as f:
                return f.read().strip()
        else:
            return TINDER_TOKEN


class MatchesEndpoint(ApiEndpoint):
    path = '/v2/matches'
    params = {
        'count': 60,
        'is_tinder_u': 'false',
        'locale': 'en',
        'message': 0,
        }

    def get_headers(self):
        headers = super(MatchesEndpoint, self).get_headers()
        headers['x-supported-image-formats'] = 'webp,jpeg'
        return headers


class LikeEndpoint(ApiEndpoint):
    path = '/like/{uid}'
    params = {
        'locale': 'en',
        }


class RecommendationsEndpoint(ApiEndpoint):
    path = '/v2/recs/core'
    params = {
        'locale': 'en',
        }


class UserMatchesEndpoint(ApiEndpoint):
    path = '/user/matches/{match_id}'
