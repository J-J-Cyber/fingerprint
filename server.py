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
		# self.send_header('Content-type', 'text/html')
		# self.end_headers()

	def do_GET(self):

		if self.path == "/":
			self.set_headers()
			self.path = "/index.html"
			# print(self.path)

		return SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		'''Reads post request body'''
		self.set_headers()
		content_len = int(self.headers.get('Content-Length'))
		post_body = self.rfile.read(content_len).decode("unicode_escape")
		pb = str(post_body)
		body_list = pb.split("-----------------------------")
		del body_list[0], body_list[-1]
		filename_temp = body_list[1].split("filename=\"")[1]
		filename = ""
		for char in filename_temp:
			if char == "\"":
				break
			filename += char

		calculation_temp = body_list[2].split("\r\n\r\n")[1]
		calculation = ""
		for char in calculation_temp:
			if char == "\r":
				break
			calculation += char

		print("filename: " + filename + " calc_feature: " + calculation)

		### call feature stuff
		# check if valid input
		if filename == "" or calculation == "0":
			return

		result = FeatExt.handle_feature_call(filename, calculation)
		print(result)
		string_result = ""
		for item in result:
			string_result += str(item) + " "

		# self.wfile.write(bytes("<html><head><title> Results: .</title></head>", "utf-8"))
		self.wfile.write(bytes(string_result, "utf-8"))
		# self.wfile.write(bytes("</body></html>", "utf-8"))
		# self.wfile.close()


if __name__ == "__main__":
	DLServer = socketserver.TCPServer((HOST_NAME, SERVER_PORT), WebServer)
	print("Server started http://%s:%s" % (HOST_NAME, SERVER_PORT))

	try:
		DLServer.serve_forever()
	except KeyboardInterrupt:
		pass

	DLServer.server_close()
	print("Server stopped.")
