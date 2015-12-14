#!/usr/bin/env python
#
# Copyright 2015 BMC Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import json
import urllib2


class ActionHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        self.send_response(urllib2.httplib.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("<!DOCTYPE html><html><head><title>Hello</title></head><body>Hello World!</body>")
        self.wfile.flush()

    def do_POST(self):
        """
        Handles the POST request sent by Boundary Url Action
        """
        self.send_response(urllib2.httplib.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("<!DOCTYPE html><html><head><title>Result</title></head><body>SUCCESS</body>")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print("Client: {0}".format(str(self.client_address)))
        print("headers: {0}".format(self.headers))
        print("path: {0}".format(self.path))
        print("body: {0}".format(body))

    def process_payload(self, json_data):
        data = json.loads(json_data)
        return data


def main():
    address = '0.0.0.0'
    port = 80
    server = HTTPServer((address, port), ActionHandler)
    print("Starting Webhook on {0}:{1}, use <Ctrl-C> to stop".format(address, port))
    server.serve_forever()


if __name__ == "__main__":
    main()
