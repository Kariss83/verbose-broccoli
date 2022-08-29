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

"""
import os
import sys
from datafetcher.oauthclient.oauth2api import oauth2api
from datafetcher.oauthclient.credentialutil import credentialutil
from datafetcher.oauthclient.model.model import environment
import unittest

from django.test import TestCase

sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))

app_scopes = ["https://api.ebay.com/oauth/api_scope"]
invalid_app_scopes = ["https://api.ebay.com/oauth/api_scope", "https://api.ebay.com/oauth/api_scope/sell.inventory"]


class TestGetApplicationCredential(TestCase):

    def test_invalid_oauth_scope(self):
        credentialutil.load('datafetcher/oauthclient/ebay-config-sample.json')
        oauth2api_inst = oauth2api()
        app_token = oauth2api_inst.get_application_token(environment.SANDBOX, invalid_app_scopes)
        self.assertIsNone(app_token.access_token)
        self.assertIsNotNone(app_token.error)

    def test_client_credentials_grant_sandbox(self):
        oauth2api_inst = oauth2api()
        credentialutil.load('datafetcher/oauthclient/ebay-config-sample.json')
        app_token = oauth2api_inst.get_application_token(environment.SANDBOX, app_scopes)
        self.assertIsNone(app_token.error)
        self.assertIsNotNone(app_token.access_token)
        self.assertTrue(len(app_token.access_token) > 0)
        print('\n *** test_client_credentials_grant_sandbox ***:\n', app_token)

    def test_client_credentials_grant_production(self):
        oauth2api_inst = oauth2api()
        credentialutil.load('datafetcher/oauthclient/ebay-config-sample.json')
        app_token = oauth2api_inst.get_application_token(environment.PRODUCTION, app_scopes)
        self.assertIsNone(app_token.error)
        self.assertIsNotNone(app_token.access_token)
        self.assertTrue(len(app_token.access_token) > 0)


if __name__ == '__main__':
    unittest.main()
