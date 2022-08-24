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
import base64

def _generate_request_headers(credential):

    credentials = credential.client_id + ':' + credential.client_secret
    credentials_bytes = credentials.encode('ascii')
    b64_credentials_bytes = base64.b64encode(credentials_bytes)
    b64_credentials = b64_credentials_bytes.decode('ascii')
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + b64_credentials
    }

    return headers


def _generate_application_request_body(credential, scopes):


    body = {
            'grant_type': 'client_credentials',
            'redirect_uri': credential.ru_name,
            'scope': scopes
    }
    

    return body
