import json
import boto3
import re


# def recursively_evaluate_folder_string(folder_str, output_dict):
# 	first_index = {
# 		"dict_delim": folder_str.find(dict_delimiter),
# 		"nested_list_delim": folder_str.find(nested_list_delimiter),
# 		"slash": folder_str.find("/"),
# 	}
# 	lowest_index = min(foo, key=foo.get)
# 	# lowest_index = [x for x in first_index.items()]


def recursively_evaluate_folder_string(folder_str, output_dict):
	for n, char in enumerate(folder_str):

		if char not in [":", "/"]:
			continue

		elif char == "/" and folder_str[n+1] not in [":", "/"]:
			pass # TODO - item in list, no nesting beneath
		
		elif folder_str[n:n+3] == dict_delimiter:
			key, val = folder_str.split(dict_delimiter, 1)
			output_dict[key] = value
			return value, 'foo' # TODO - k,v pair in dict, no nesting beneath
		
		elif re.match(":{2}\d*:{2}", folder_str): # check if returns index
			pass # TODO - item in list, definite nesting beneath

		elif "foo" == "bar":
			pass # TODO - dict in dict, definite nesting beneath

# The path should be `folder/` NOT `/folder`
def list_s3_bucket_contents(bucket, path, **kwargs):
	# s3 = boto3.resource("s3")
	# bucket = s3.Bucket(bucket)
	s3 = boto3.client("s3")

	# return list(bucket.list(path, "/"))
	s3_objects = s3.list_objects_v2(
		Bucket=bucket,
		Prefix=path,
		MaxKeys=1000
	)

	return [x['Key'] for x in s3_objects['Contents']]
	# return [x.key for x in bucket.objects.filter(Prefix=path)]


if __name__ == '__main__':
	bucket_name = BUCKETNAME
	bucket_file_folder = "test.json"
	dict_delimiter = "::::"
	nested_list_delimiter = "::#::"
	""" overflow_str_delimiter = "__" + i + "__" """ # don't change this
	# global dict_delimiter
	# global nested_list_delimiter

	data = list_s3_bucket_contents(bucket_name, bucket_file_folder)
	
	for folder in data:
		folder_str = folder.split(bucket_file_folder + "/")[1].rstrip("/")

		top_level_key = min(folder_str[:folder_str.find(":")], folder_str[:folder_str.find("/")])
		print(top_level_key)
	# output_dict = {}
	# 	print(folder_str)
	# 	dict_delim_index = folder_str.find(dict_delimiter)
	# 	nested_list_delim_index = folder_str.find(nested_list_delimiter)
	# 	slash_index = folder_str.find("/")


