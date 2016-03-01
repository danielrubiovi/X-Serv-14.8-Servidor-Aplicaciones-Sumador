#!/usr/bin/python
# -*- coding: utf-8 -*-

# Daniel Rubio Villegas

import random
import socket


class WebApp:
	
	def parse(self, request):
		numRcv = int(request.split()[1][1:])
		return numRcv
		
	def process(self, numRcv, num1):
		if num1 == None:
			num1 = numRcv
			answer = "<html><body><h2>" 'Numero uno: ' + str(num1) + ", Deme otro numero</h2></body></html>"
		else:
			suma = str(num1 + numRcv)
			answer = "<html><body><h2>"+'Suma: '+ str(num1)+ '+' + str(numRcv) + ' = ' + str(suma) + "</h2></body></html>"
			num1 = None
		return ("HTTP/1.1 200 OK", answer, num1)
		
	def fail (self, numRand):
		answer = ("\r\n\r\n"+
				"<html><body bgcolor='red'>" +
				"<p><h2>"
				"Quiero un numero NO CHAR!! ERROR 400000004 Numero not found" +
				"</h2><p>"
				"</p>"
				"<p>"
				"<IMG SRC='http://globalgamejam.org/sites/default/files/styles/game_sidebar__normal/public/game/featured_image/promo_5.png'>" +
				"</p>"
				"<a href='http://localhost:1234/" + str(numRand) + 
				"'>Dame un numero aleatorio :)</a>" +
				"</p>"
				"</body></html>" + "\r\n")
		return ("HTTP/1.1 200 OK", answer)
			
	def __init__(self, host, port):
		numRcv = None
		mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		mySocket.bind((host, port))

		mySocket.listen(5)
		
		while True:
			print 'Waiting for connections'
			(recvSocket, address) = mySocket.accept()
			print 'HTTP request received:'
			request = recvSocket.recv(1024)
			print request
			
			try:
				parsRequest = int(self.parse(request))
			except ValueError:
				randNum = random.randint(0,500)
				(returnCode, htmlAnswer) = self.fail(randNum)
				print "No he recibido un número sino otro cosa!! Bad chars.."
				recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
							+ htmlAnswer + "\r\n")
				recvSocket.close()
				continue
			
				
			(returnCode, htmlAnswer, numRcv) = self.process(parsRequest, numRcv)
			print 'Answering back...'
			recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
							+ htmlAnswer + "\r\n")
			recvSocket.close()
			
if __name__ == "__main__":
    testWebApp = WebApp("localhost", 1234)
	
		
