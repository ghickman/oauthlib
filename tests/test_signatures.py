from __future__ import absolute_import

from .unittest import TestCase

import urllib

from oauthlib.signature import *


class SignatureTests(TestCase):

    def test_construct_base_string(self):
        """
        Example text to be turned into a base string::

            POST /request?b5=%3D%253D&a3=a&c%40=&a2=r%20b HTTP/1.1
            Host: example.com
            Content-Type: application/x-www-form-urlencoded
            Authorization: OAuth realm="Example",
                           oauth_consumer_key="9djdj82h48djs9d2",
                           oauth_token="kkk9d7dh3k39sjv7",
                           oauth_signature_method="HMAC-SHA1",
                           oauth_timestamp="137131201",
                           oauth_nonce="7d8f3e4a",
                           oauth_signature="bYT5CMsGcbgUdFHObYMEfcx6bsw%3D"

        Sample Base string generated and tested against::
            
            POST&http%3A//example.com/request%3Fb5%3D%253D%25253D%26a3%3Da%26c%2540%3D
            %26a2%3Dr%2520b&OAuth%20realm%3D%22Example%22%2Coauth_consumer_key%3D%229d
            jdj82h48djs9d2%22%2Coauth_token%3D%22kkk9d7dh3k39sjv7%22%2Coauth_signature
            _method%3D%22HMAC-SHA1%22%2Coauth_timestamp%3D%22137131201%22%2Coauth_nonc
            e%3D%227d8f3e4a%22%2Coauth_signature%3D%22bYT5CMsGcbgUdFHObYMEfcx6bsw%253D
            %22
        """

        # This is the string we want to match
        control_test_string = "POST&http%3A//example.com/request%3Fb5%3D%253D%25253D%26a3%3Da%26c%2540%3D%26a2%3Dr%2520b&OAuth%20realm%3D%22Example%22%2Coauth_consumer_key%3D%229djdj82h48djs9d2%22%2Coauth_token%3D%22kkk9d7dh3k39sjv7%22%2Coauth_signature_method%3D%22HMAC-SHA1%22%2Coauth_timestamp%3D%22137131201%22%2Coauth_nonce%3D%227d8f3e4a%22%2Coauth_signature%3D%22bYT5CMsGcbgUdFHObYMEfcx6bsw%253D%22"

        # Create test variables
        # Create test variables
        # Create test variables
        http_method = "post"
        base_string_url = urllib.quote("http://example.com/request?b5=%3D%253D&a3=a&c%40=&a2=r%20b")
        normalized_encoded_request_parameters = urllib.quote("""OAuth realm="Example",oauth_consumer_key="9djdj82h48djs9d2",oauth_token="kkk9d7dh3k39sjv7",oauth_signature_method="HMAC-SHA1",oauth_timestamp="137131201",oauth_nonce="7d8f3e4a",oauth_signature="bYT5CMsGcbgUdFHObYMEfcx6bsw%3D" """.strip())

        base_string = construct_base_string(http_method, base_string_url , normalized_encoded_request_parameters)

        self.assertEqual(control_test_string, base_string)

    def test_normalize_base_string_uri(self):
        """
        Example text to be turned into a normalized base string uri::
            
            GET /?q=1 HTTP/1.1
            Host: www.example.net:8080
        
        Sample string generated::
            
            https://www.example.net:8080/
        """
        
        # test for unicode failure
        uri = "www.example.com:8080"
        self.assertRaises(ValueError, normalize_base_string_uri, uri)

        uri = u"http://www.example.com:80"
        self.assertEquals(normalize_base_string_uri(uri), "http://www.example.com")

    def test_collect_parameters(self):
        """ We check against parameters multiple times in case things change after more
                parameters are added.
        """
        # check against empty parameters
        # check against empty parameters
        # check against empty parameters
        self.assertEquals(collect_parameters(), [])

        # Check against uri_query
        # Check against uri_query
        # Check against uri_query
        uri_query = "b5=%3D%253D&a3=a&c%40=&a2=r%20b"
        parameters = collect_parameters(uri_query=uri_query)

        self.assertEquals(len(parameters), 3)
        self.assertEquals(parameters[0], ('b5', '=%3D'))
        self.assertEquals(parameters[1], ('a3', 'a'))
        self.assertEquals(parameters[2], ('a2', 'r b'))

        # check against authorization header as well
        # check against authorization header as well
        # check against authorization header as well
        authorization_header = """OAuth realm="Example",
oauth_consumer_key="9djdj82h48djs9d2",
oauth_token="kkk9d7dh3k39sjv7",
oauth_signature_method="HMAC-SHA1",
oauth_timestamp="137131201",
oauth_nonce="7d8f3e4a",
oauth_signature="djosJKDKJSD8743243%2Fjdk33klY%3D" """.strip()

        parameters = collect_parameters(uri_query=uri_query, authorization_header=authorization_header)

        # Redo the checks against all the parameters. Duplicated code but better safety
        self.assertEquals(len(parameters), 8)
        self.assertEquals(parameters[0], ('b5', '=%3D'))
        self.assertEquals(parameters[1], ('a3', 'a'))
        self.assertEquals(parameters[2], ('a2', 'r b'))
        self.assertEquals(parameters[3], ('oauth_nonce', '7d8f3e4a'))
        self.assertEquals(parameters[4], ('oauth_timestamp', '137131201'))
        self.assertEquals(parameters[5], ('oauth_consumer_key', '9djdj82h48djs9d2'))
        self.assertEquals(parameters[6], ('oauth_signature_method', 'HMAC-SHA1'))
        self.assertEquals(parameters[7], ('oauth_token', 'kkk9d7dh3k39sjv7'))

        # Add in the body.
        # TODO - add more valid content for the body. Daniel Greenfeld 2012/03/12
        body = "content=This is being the body of things"

        # Redo again the checks against all the parameters. Duplicated code but better safety
        parameters = collect_parameters(uri_query=uri_query, authorization_header=authorization_header, body=body)
        self.assertEquals(len(parameters), 9)
        self.assertEquals(parameters[0], ('b5', '=%3D'))
        self.assertEquals(parameters[1], ('a3', 'a'))
        self.assertEquals(parameters[2], ('a2', 'r b'))
        self.assertEquals(parameters[3], ('oauth_nonce', '7d8f3e4a'))
        self.assertEquals(parameters[4], ('oauth_timestamp', '137131201'))
        self.assertEquals(parameters[5], ('oauth_consumer_key', '9djdj82h48djs9d2'))
        self.assertEquals(parameters[6], ('oauth_signature_method', 'HMAC-SHA1'))
        self.assertEquals(parameters[7], ('oauth_token', 'kkk9d7dh3k39sjv7'))
        self.assertEquals(parameters[8], ('content', 'This is being the body of things'))