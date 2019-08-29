import json

from http.server import BaseHTTPRequestHandler, HTTPServer

from film_locations_service.handler import handler

PORT = 8000

class Handler(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def do_HEAD(self):
      self._set_headers()

  def do_GET(self):
    self._set_headers()
    response = handler(None, None)
    self.wfile.write(str.encode(response))

httpd = HTTPServer(('', PORT), Handler)
print("Starting server at:", PORT)
httpd.serve_forever()