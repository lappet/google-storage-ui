import boto
import os
import tempfile

config = boto.config


def getbuckets():
        uri = boto.storage_uri("","gs")
        buckets = uri.get_all_buckets()
        bucket_list = []
        for bucket in buckets:
        	bucket_list.append(bucket.name)
        return bucket_list

def getobjects(bucketname):
        uri = boto.storage_uri(bucketname,"gs")
        objs = uri.get_bucket()
        file_list = []
        for obj in objs:
                file_list.append(obj.name)
        return file_list

def downloadObject(bucketname,objname,dest_dir):
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
	
