#!/usr/bin/env python3


from src import mahouka_json


def encode_file(input_dir_path, full_input_dir_path, input_file_name, output_dir_path):
    input_file_path = full_input_dir_path + '/' + input_file_name

    print('Found json file \"{0}\"'.format(input_file_path))

    input_file = open(input_file_path, mode='rt')
    input_file_data = input_file.read()
    deserialized = mahouka_json.deserialize_file(input_file_data)

    _type = deserialized[0]
    deserialized_file_path = deserialized[1]
    deserialized_file = deserialized[2]

    write_deserialized(deserialized_file_path, output_dir_path, _type, deserialized_file)

    print('Wrote deserialized json file \"{0}\" to \"{1}\"'.format(input_file_path, output_dir_path + '/' + deserialized_file_path))


def write_deserialized(output_file_path, output_dir, _type, deserialized_file):
    output_file_complete_path = output_dir + '/' + output_file_path

    # TODO REMOVE - DEBUG
    import os
    if os.path.exists(output_file_complete_path):
        os.remove(output_file_complete_path)

    output_file = open(output_file_complete_path, mode='wb')
    try:
        output_file.write(deserialized_file)
    finally:
        output_file.close()
