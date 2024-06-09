#!/usr/bin/env python3


import mahouka_json


def encode_file(input_dir_path, full_input_dir_path, input_file_name, output_dir_path):
    input_file_path = full_input_dir_path + '/' + input_file_name

    print('Found json file \"{0}\"'.format(input_file_path))

    input_file = open(input_file_path, mode='rt')
    input_file_data = input_file.read()
    mahouka_json.deserialize_file(input_file_data)

    return None


def write_serialized(serialized, output_file_name, output_dir):
    # TODO
    return
