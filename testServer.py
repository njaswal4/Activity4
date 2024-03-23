# Name: Nisarg Jaswal
#Student Id: 226088220
import http
import unittest
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
import http.client
import json
import threading

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_get_method(self):
        # Send a GET request to the server and check the response
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('GET', '/')
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        # Verify the response status, headers, and content type
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, {'message': 'This is a response to a GET request'})

    def test_post_method(self):
        # Send a POST request to the server and check the response
        connection = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-type': 'application/json'}
        test_data = {'key': 'value'}
        connection.request('POST', '/', body=json.dumps(test_data), headers=headers)
        response = connection.getresponse()

        # Read and decode the response
        data = response.read().decode()
        connection.close()

        # Verify the response status, headers, and content type
        self.assertEqual(response.status, 200)
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, {'received': test_data})

if __name__ == '__main__':
    unittest.main()
