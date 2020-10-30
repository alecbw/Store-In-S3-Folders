import json
import boto3



"""
Order of lists will not be preserved
Duplicate items in lists will be removed
Everything gets converted into and out of str, so be very careful using weird typings
	e.g. "8" will be interpreted as 8 on read.

Folder names will silently overwrite. 
The write does not do any other deleting and doesn't check if the folder is empty

TODO: the maximum length of 1024 applies to the most nested child path
	e.g. a/b/c/d cant' be >1024, therefore a/b/c minus d can't be > 1024
"""

def read_local_json(filename):
    with open(filename) as f_in:
        return(json.load(f_in, strict=False))


def write_str_int_float_bool_null_value(bucket_name, key, key_delim, value):
    value = str(value)

    if (len(key) + len(value)) < 1020:
        return create_new_folder(bucket_name, key + key_delim + value)

    n = (1015-len(key))
    for i in range(0, len(value), n):
        if key_delim == dict_delimiter:
            specific_key = key + "__" + i + "__" + key_delim #key + "____" + i + dict_delimiter
        else:
            specific_key = key + key_delim + "__" + i + "__"

        return create_new_folder(bucket_name, specific_key + value[i:i+n])


def handle_list_value(bucket_name, key, value_list):
    for n, val in enumerate(value_list):
        if isinstance(val, list):
            handle_list_value(bucket_name, key + "/" + nested_list_delimiter.replace("#", str(n)), val)

        elif isinstance(val, dict):
            handle_dict_value(bucket_name, key, val)

        else:
            write_str_int_float_bool_null_value(bucket_name, key, "/", val)


def handle_dict_value(bucket_name, key, value_dict):  # key,        
    for k,v in value_dict.items():
        k = key + "/" + k

        if isinstance(v, list):
            handle_list_value(bucket_name, k, v)

        elif isinstance(v, dict):
            handle_dict_value(bucket_name, k, v)

        else:
            write_str_int_float_bool_null_value(bucket_name, k, dict_delimiter, v)


def create_new_folder(bucket_name, folder_path):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=(folder_path+'/'))



### TODO: differentiate dict in dict-val and str in list (both are just /)


if __name__ == '__main__':
    bucket_name = BUCKETNAME
    local_json_filename = "test.json"
    dict_delimiter = "::::"
    nested_list_delimiter = "::#::"
    """ overflow_str_delimiter = "__" + i + "__" """ # don't change this

    local_json = read_local_json(local_json_filename)

    handle_dict_value(bucket_name, local_json_filename, local_json)

