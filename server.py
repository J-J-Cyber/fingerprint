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
		#self.send_header('Content-type', 'text/html')
		#self.end_headers()

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
		calc_list = []
		name_list = []
		for item in body_list:
			if "calculation" in item:
				calc_list.append(item)

			if "filename" in item:
				name_list.append(item)

		file_name_list = []
		calculation_num_list = []

		for name in name_list:
			filename_temp = name.split("filename=\"")[1]
			filename = ""
			for char in filename_temp:
				if char == "\"":
					break
				filename += char
			file_name_list.append(filename)

		for calc in calc_list:
			calculation_temp = calc.split("\r\n\r\n")[1]
			calculation = ""
			for char in calculation_temp:
				if char == "\r":
					break
				calculation += char
			calculation_num_list.append(calculation)

		print("filename: ", file_name_list, " calc_feature: ", calculation_num_list)

		### call feature stuff
		# check if valid input
		if file_name_list == [''] or calculation_num_list == ['']:
			print("Name empty or No Feature selected!")
			return

		result = FeatExt.handle_feature_call(file_name_list, calculation_num_list)
		print("server got result")

		self.path = "/results.html"

		# handle results page:
		canvas_img = """<div>
							<img src="IMAGEPATH">
						</div>"""

		canvas_res = """<div id="canvas" class="col-md-6 compress">
						<p>FILENAME</p>
							<section class="regular slider slick">
								IMAGECANVAS
							</section>
						</div>"""

		canvas_main_pre = ""
		canvas_main = ""

		for file in file_name_list:
			for feature in calculation_num_list:
				temp_image = canvas_img.replace("IMAGEPATH", "img/" + file[:-4] + feature + ".png")
				canvas_main_pre += temp_image
			temp_res = canvas_res.replace("FILENAME", file[:-4])
			temp_res = temp_res.replace("IMAGECANVAS", canvas_main_pre)
			canvas_main += temp_res
			canvas_main_pre = ""

		file = open("result.html", "r")
		file_string = file.read().replace("<!-- Insert-Results -->", canvas_main)
		file.close()

		outfile = open('results.html', 'w+')
		outfile.truncate(0)
		outfile.write(file_string)
		outfile.close()

		return SimpleHTTPRequestHandler.do_GET(self)

		# f = open("result.html")
		# self.wfile.write(bytes(f.read(), "utf-8"))
		# self.wfile.write(bytes("<html><head><title> Results: .</title></head>", "utf-8"))
		# self.wfile.write(bytes(string_result, "utf-8"))
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
