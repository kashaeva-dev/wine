from http.server import HTTPServer, SimpleHTTPRequestHandler

print(1)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
