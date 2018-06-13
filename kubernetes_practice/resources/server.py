import http.server as server
import logging
import sys
import socket

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

    def do_GET(self):
        self._set_headers()
        self.wfile.write(bytes("<p>hello</p>", "utf-8"))

    def do_HEAD(self):
        self._set_headers()


def run(server_class=server.HTTPServer, *, handler_class=RequestHandler, host="localhost", port=8088):
    """
    运行server
    :param server_class:
    :param handler_class:
    :param port:
    :return:
    """
    RequestHandler.logger.setLevel(logging.INFO)
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)

    RequestHandler.logger.info("starting httpd")

    httpd.serve_forever()

def get_local_ip():
    ip = [l for l in ([
                          ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                          if not ip.startswith("127.")][:1],
                      [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                        for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]])
          if l][0][0]
    return ip

if __name__ == "__main__":
    ip = get_local_ip()
    if len(sys.argv) == 3:
        run(host=sys.argv[1], port=int(sys.argv[2]))
    else:
        run(host=ip, port=8088)
