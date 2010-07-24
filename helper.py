#Helper functions
import os

def list2str(array):
	op = str(array)
	op = op.strip('[')
	op = op.strip(']')
	return op

def getFilenameFromPath(path):
	return os.path.basename(path)	
