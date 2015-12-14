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
import syslog


class ActionHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):
        """
        Handles the POST request sent by TrueSight Pulse Url Action
        """

        # Send back a 200 result code and html page indicating success
        self.send_response(urllib2.httplib.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("<!DOCTYPE html><html><head><title>Result</title></head><body>SUCCESS</body>")

        # Read the contents which contains a JSON payload
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        alarm = json.loads(body)

	# Print out Alarm status
        print("Status: {0}".format(alarm['status']))

        # For each affected server and resolved servers output it's associated test on its status
        affected_servers = alarm['affectedServers']
        if affected_servers is not None:
            for server in affected_servers:
                alarm_text = affected_servers[server]['text']['labelText']
                print(alarm_text)
                syslog.syslog(syslog.LOG_ALERT, alarm_text)

        resolved_servers = alarm['resolvedServers']
        if resolved_servers is not None:
            for server in resolved_servers:
                alarm_text = resolved_servers[server]['text']['labelText']
                print(alarm_text)
                syslog.syslog(syslog.LOG_INFO, alarm_text)


def main():
    address = '0.0.0.0'
    port = 80
    server = HTTPServer((address, port), ActionHandler)
    print("Starting ActionHandler on {0}:{1}, use <Ctrl-C> to stop".format(address, port))
    server.serve_forever()


if __name__ == "__main__":
    main()
