#Helper functions go here
import os
import socket

def list2str(array):
	op = str(array)
	op = op.strip('[')
	op = op.strip(']')
	return op

def getFilenameFromPath(path):
	return os.path.basename(path)	

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

