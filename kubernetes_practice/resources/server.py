import http.server as server
import logging
import sys

"""
This is a sample http server
"""
class RequestHandler(server.BaseHTTPRequestHandler):
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger("HttpServer")

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_get(self):
        self._set_headers()
        self.wfile.write(bytes("<p>hello</p>", "utf-8"))

    def do_head(self):
        self._set_headers()


def run(server_class=server.HTTPServer, *, handler_class=RequestHandler, port=8088):
    """
    运行server
    :param server_class:
    :param handler_class:
    :param port:
    :return:
    """
    RequestHandler.logger.setLevel(logging.INFO)
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)

    RequestHandler.logger.info("starting httpd")

    httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(port=int(sys.argv[1]))
    else:
        run()
