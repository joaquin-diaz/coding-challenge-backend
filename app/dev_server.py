import json
from urllib.parse import urlparse, parse_qs

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

    parsed_url = urlparse(self.path)
    # Output: {"name": ['value1', 'value2']}
    parsed_qs = parse_qs(parsed_url.query)
    # Mock lambda event
    mock_event = {
      "queryStringParameters": {
        "query": parsed_qs.get('query', ''),
        "limit": parsed_qs.get('limit', ''),
      }
    }

    response = handler(mock_event, None)
    self.wfile.write(str.encode(response))

httpd = HTTPServer(('', PORT), Handler)
print("Starting server at:", PORT)
httpd.serve_forever()