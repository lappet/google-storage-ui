import socket

def ping():
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		sock.connect(("google.com",80))
		print "Success!"
	        return 1	
	except socket.error:
		print "Server offline"
		return 0
	sock.close()

