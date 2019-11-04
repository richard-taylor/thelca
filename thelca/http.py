
import http.server
import json

class Handler(http.server.BaseHTTPRequestHandler):

    server_version = 'TheElectricCat/0.1'
    sys_version = ''
            
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')  
        self.end_headers()
        self.wfile.write(b'Hello\n')

