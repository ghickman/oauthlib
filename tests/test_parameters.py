from __future__ import absolute_import

from .unittest import TestCase

from oauthlib.parameters import *


class ParameterTests(TestCase):
    auth_only_params = [
        (u'oauth_consumer_key', u"9djdj82h48djs9d2"),
        (u'oauth_token', u"kkk9d7dh3k39sjv7"),
        (u'oauth_signature_method', u"HMAC-SHA1"),
        (u'oauth_timestamp', u"137131201"),
        (u'oauth_nonce', u"7d8f3e4a"),
        (u'oauth_signature', u"bYT5CMsGcbgUdFHObYMEfcx6bsw%3D")
    ]
    auth_and_data = list(auth_only_params)
    auth_and_data.append((u'data_param_foo', u'foo'))
    auth_and_data.append((u'data_param_1', u'1'))
    realm = 'testrealm'
    norealm_authorization_header = 'OAuth oauth_consumer_key=9djdj82h48djs9d2,oauth_token=kkk9d7dh3k39sjv7,oauth_signature_method=HMAC-SHA1,oauth_timestamp=137131201,oauth_nonce=7d8f3e4a,oauth_signature=bYT5CMsGcbgUdFHObYMEfcx6bsw%3D'
    withrealm_authorization_header = 'OAuth realm=testrealm,oauth_consumer_key=9djdj82h48djs9d2,oauth_token=kkk9d7dh3k39sjv7,oauth_signature_method=HMAC-SHA1,oauth_timestamp=137131201,oauth_nonce=7d8f3e4a,oauth_signature=bYT5CMsGcbgUdFHObYMEfcx6bsw%3D'

    def test_order_oauth_parameters(self):
        unordered = {
            'oauth_foo': 'foo',
            'oauth_bar': 'bar',
            'lala': 123,
            'oauth_baz': 'baz', }
        expected = [
            ('oauth_bar', 'bar'),
            ('oauth_baz', 'baz'),
            ('oauth_foo', 'foo'),
            ('lala', 123)]
        self.assertEqual(order_oauth_parameters(unordered), expected)

    def test_prepare_authorization_header(self):
        self.assertEqual(
            prepare_authorization_header(self.auth_only_params),
            self.norealm_authorization_header)
        self.assertEqual(
            prepare_authorization_header(self.auth_only_params, realm=self.realm),
            self.withrealm_authorization_header)

    def test_prepare_authorization_header_ignore_data(self):
        self.assertEqual(
            prepare_authorization_header(self.auth_and_data),
            self.norealm_authorization_header)
        self.assertEqual(
            prepare_authorization_header(self.auth_and_data, realm=self.realm),
            self.withrealm_authorization_header)

    def test_prepare_form_encoded_body(self):
        form_encoded_body = 'oauth_signature=bYT5CMsGcbgUdFHObYMEfcx6bsw%253D&oauth_nonce=7d8f3e4a&oauth_timestamp=137131201&oauth_signature_method=HMAC-SHA1&oauth_token=kkk9d7dh3k39sjv7&oauth_consumer_key=9djdj82h48djs9d2&data_param_foo=foo&data_param_1=1'
        self.assertEqual(
            prepare_form_encoded_body(self.auth_and_data), form_encoded_body)

    def test_prepare_request_uri_query(self):
        url = u'http://notarealdomain.com/foo/bar/baz?some=args&go=here'
        request_uri_query = u'http://notarealdomain.com/foo/bar/baz?some=args&go=here&data_param_foo=foo&data_param_1=1&oauth_signature=bYT5CMsGcbgUdFHObYMEfcx6bsw%253D&oauth_nonce=7d8f3e4a&oauth_timestamp=137131201&oauth_signature_method=HMAC-SHA1&oauth_token=kkk9d7dh3k39sjv7&oauth_consumer_key=9djdj82h48djs9d2'
        self.assertEqual(
            prepare_request_uri_query(self.auth_and_data, url),
            request_uri_query)
