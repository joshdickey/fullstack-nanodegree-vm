from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

import os
import sys
from sqlalchemy import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
sesssion.commit()

class WebServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</html></body>"
				self.wfile.write(output.encode(encoding='utf_8'))
				print (output)
				return
			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>"
				output += "&#16Hola <a href = '/hello' > Back to Hello<a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</html></body>"
				self.wfile.write(output.encode(encoding='utf_8'))
				print (output)
				return
				
			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()				
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>"
				#TODO add for loop restaurant in restaurants: output += restaurant.name output += "</br>"
				output += "</html></body>"
				self.wfile.write(output.encode(encoding='utf_8'))
				print (output)
				return
				
		except:
			self.send_error(404, "file not found %s" % self.path)
			
	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()
			
			ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
			pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
				
				output = ""
				output += "<html><body>"
				output += " <h2> Okay, how about this: </h2>"
				output += "<h1> "
				self.wfile.write(bytes(output, "UTF-8"))
				self.wfile.write(messagecontent[0])
				output = ""
				output += " </h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"

				self.wfile.write(bytes(output, "UTF-8"))
				print (output)
				
		except:
			pass
				
def main():
    try:
        port = 8080
        server = HTTPServer(('localhost', port), WebServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()
				

		
if __name__ == '__main__':
	main()