import boto
import os
import tempfile
import helper

config = boto.config #Yet to figure out what this does!


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

def downloadObjects(bucketname,objnames,dest_dir):
	"""Download a specific object from an exising bucket into a specified directory"""
	for objname in objnames:
		src_uri = boto.storage_uri(bucketname+"/"+objname,"gs")
		dst_uri = boto.storage_uri(dest_dir,"file")

		dst_key_name = dst_uri.object_name + os.sep + src_uri.object_name
		new_dst_uri = dst_uri.clone_replace_name(dst_key_name)
		
		dst_key = new_dst_uri.new_key()
		
		src_key = src_uri.get_key()
		
		tmp = tempfile.TemporaryFile()
		src_key.get_file(tmp)
		tmp.seek(0)

		dst_key.set_contents_from_file(tmp)

def uploadObject(bucketname,filenames):
        """upload(s) all given files into the specified bucket"""
	for name in filenames:
		fname =  helper.getFilenameFromPath(name) #name is actually the path, the helper function gets just the filename
		src_uri = boto.storage_uri(name,"file")
		dst_uri = boto.storage_uri(bucketname,"gs")

		dst_key_name = dst_uri.object_name + os.sep + fname
		new_dst_uri = dst_uri.clone_replace_name(dst_key_name)
		
		dst_key = new_dst_uri.new_key()
		
		src_key = src_uri.get_key()
		
		tmp = tempfile.TemporaryFile()
		src_key.get_file(tmp)
		tmp.seek(0)
		dst_key.set_contents_from_file(tmp)
		
def deleteObjects(bucketname,filenames):
		for filename in filenames:
			uri = boto.storage_uri(bucketname,"gs")
			objs = uri.get_bucket()
			if objs:
				for obj in objs:
					if obj.name == filename:
						obj.delete()
		
					
		

	
