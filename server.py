import socketserver
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
import time, os, platform
import py.feature_extraction as FeatExt

HOST_NAME = "localhost"
SERVER_PORT = 8080
"""
HOME_DIR = ""
if platform.system() == "Windows":
	temp_homedir = os.getcwd().split("\\")
	del temp_homedir[-1]
	for dir in temp_homedir:
		HOME_DIR += dir + "\\"
else:
	temp_homedir = os.getcwd().split("/")
	del temp_homedir[-1]
	for dir in temp_homedir:
		HOME_DIR += dir + "/"
"""


class WebServer(SimpleHTTPRequestHandler):

	def set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):

		if self.path == "/":
			self.set_headers()
			self.path = "/index.html"
			print(self.path)

			return SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		print("Handle POST request - (call from index.html with params) - then display with inline html?")
		FeatExt.test_call()

		'''Reads post request body'''
		self.set_headers()
		content_len = int(self.headers.get('Content-Length'))
		post_body = self.rfile.read(content_len)
		print(post_body)
		# self.wfile.write("received post request:<br>{}".format(post_body))




if __name__ == "__main__":
	DLServer = socketserver.TCPServer((HOST_NAME, SERVER_PORT), WebServer)
	print("Server started http://%s:%s" % (HOST_NAME, SERVER_PORT))

	try:
		DLServer.serve_forever()
	except KeyboardInterrupt:
		pass

	DLServer.server_close()
	print("Server stopped.")
