from http.server import BaseHTTPRequestHandler, HTTPServer

"""
This is a sample http server
"""

class Request_handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(bytes("<p>hello</p>", "utf-8"))

    def do_HEAD(self):
        self._set_headers()


def run(server_class=HTTPServer, *, handler_class=Request_handler, port=8088):
    """
    运行server
    :param server_class:
    :param handler_class:
    :param port:
    :return:
    """
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
