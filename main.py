from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import pathlib
import socketserver
import socket
import threading
import urllib.parse
from datetime import datetime
import json
from pymongo import MongoClient


PORT = 3000
SOCKET_PORT = 5000

client = MongoClient("mongodb://mongodb:27017/")
db = client["message_db"]
collection = db["messages"]


class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message.html":
            self.send_html_file("message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode("utf-8"))

            username = post_data["username"][0]
            message = post_data["message"][0]

            data = {
                "date": str(datetime.now()),
                "username": username,
                "message": message,
            }

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("localhost", SOCKET_PORT))
            sock.sendall(json.dumps(data).encode("utf-8"))
            sock.close()

            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def run_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", SOCKET_PORT))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024)
        if data:
            message_data = json.loads(data.decode("utf-8"))
            collection.insert_one(message_data)
        client_socket.close()


if __name__ == "__main__":
    handler = MyHttpRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)

    socket_server_thread = threading.Thread(target=run_socket_server)
    socket_server_thread.daemon = True
    socket_server_thread.start()

    print(f"Serving HTTP on port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
