import boto
from boto.exception import *
import os
import tempfile
import helper

config = boto.config #Yet to figure out what this does!

def callBack(trans,total):
	print trans,total	

def createBucket(bucketName):
	"""Create  a new bucket"""
	try:
		bucket_uri = boto.storage_uri(bucketName,"gs")
		bucket_uri.create_bucket()
		return (0,"Successfully created!")
	except S3CreateError, e:
		return (e.code,e.reason)

def deleteBucket(bucketName):
	"Delete a specified bucket"""
	try:
		bucket_uri = boto.storage_uri(bucketName,"gs")
		objs = bucket_uri.get_bucket()
		if objs:
			for obj in objs:
				obj.delete()
		bucket_uri.delete_bucket()
	except StandardError, e:
		return (e.code,e.reason)


def getBuckets():
	"""Get all the buckets in your account"""
        uri = boto.storage_uri("","gs")
        buckets = uri.get_all_buckets()
        bucket_list = []
        for bucket in buckets:
        	bucket_list.append(bucket.name)
        return bucket_list

def getObjects(bucketname):
	"""Get objects in specified bucketname"""
        uri = boto.storage_uri(bucketname,"gs")
        objs = uri.get_bucket()
        file_list = []
        for obj in objs:
                file_list.append(obj.name)
        return file_list

def downloadObject(bucketname,objname,dest_dir,cb=callBack):
	"""Download a specific object from an exising bucket into a specified directory"""
	src_uri = boto.storage_uri(bucketname+"/"+objname,"gs")
	dst_uri = boto.storage_uri(dest_dir,"file")

	dst_key_name = dst_uri.object_name + os.sep + src_uri.object_name
	new_dst_uri = dst_uri.clone_replace_name(dst_key_name)
	
	dst_key = new_dst_uri.new_key()
	
	src_key = src_uri.get_key()
	
	tmp = tempfile.TemporaryFile()
	src_key.get_file(tmp,None,cb,100)
	tmp.seek(0)

	dst_key.set_contents_from_file(tmp)

def uploadObject(bucketname,filename,cb=callBack):
        """upload(s) all given files into the specified bucket"""
	fname =  helper.getFilenameFromPath(filename) #name is actually the path, the helper function gets just the filename
	src_uri = boto.storage_uri(filename,"file")
	dst_uri = boto.storage_uri(bucketname,"gs")

	dst_key_name = dst_uri.object_name + os.sep + fname
	new_dst_uri = dst_uri.clone_replace_name(dst_key_name)
	
	dst_key = new_dst_uri.new_key()
	
	src_key = src_uri.get_key()
	
	tmp = tempfile.TemporaryFile()
	src_key.get_file(tmp)
	tmp.seek(0)
	dst_key.set_contents_from_file(tmp,cb=cb,num_cb=100)
		
def deleteObjects(bucketname,filenames):
		"""Delete a list of files in a  bucket"""
		for filename in filenames:
			uri = boto.storage_uri(bucketname,"gs")
			objs = uri.get_bucket()
			if objs:
				for obj in objs:
					if obj.name == filename:
						obj.delete()
		
def getObjectSize(bucketname,objectname):
	"""Gets the object size"""
	uri = boto.storage_uri(bucketname,"gs")
	objs = uri.get_bucket()
	if objs:
		for obj in objs:
			if obj.name == objectname:
				return obj.size					

def download(bucketname,objectname,directory, cb = callBack):
	"""Alternate Download approach, which returns status too!"""
	uri = boto.storage_uri(bucketname,"gs")
	objs = uri.get_bucket()
	k = None
	if objs:
		for obj in objs:
			if obj.name == objectname:
				k = obj
				break
	k.get_contents_to_filename(os.path.join(directory,objectname),None,cb)


