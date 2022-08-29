# -*- coding: utf-8 -*-
"""
Copyright 2019 eBay Inc.

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

*** This file has been modified from original to be integrated in this
app ***

"""
import json
import requests

from datetime import datetime, timedelta

from datafetcher.oauthclient import model
from .credentialutil import credentialutil
from .model.model import oAuth_token


class oauth2api(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    def get_application_token(self, env_type, scopes):
        """
            makes call for application token and stores result in credential object
            returns credential object
        """
        credential = credentialutil.get_credentials(env_type)
        headers = model.util._generate_request_headers(credential)
        body = model.util._generate_application_request_body(credential, ' '.join(scopes))

        resp = requests.post(env_type.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)
        token = oAuth_token()

        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            # set token expiration time 5 minutes before actual expire time
            token.token_expiry = datetime.utcnow() + timedelta(seconds=int(content['expires_in'])) - timedelta(minutes=5)

        else:
            token.error = str(resp.status_code) + ': ' + content['error_description']
        return token
