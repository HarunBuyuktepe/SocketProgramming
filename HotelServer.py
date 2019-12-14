from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET\nPath: {}\nHeaders:\n{}\n".format(str(self.path), str(self.headers)))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode())

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=33333):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Hotel server has been started.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Hotel server has been stopped.")
        httpd.server_close()

run()
