#!/usr/bin/env python3

import argparse
import glob
import os
import multiprocessing

if not __debug__:  # Dev workspace
    from src import constants, decode, encode
else:
    import constants
    import decode
    import encode


def find_files(mode, dir):
    if mode == constants.MODE_DECODE:
        lua_files = []
        bin_files = []
        for root, subdirs, files in os.walk(dir):
            if len(files) < 1:  # Skip dirs with no files
                continue
            for lua_txt in glob.iglob(root + '\\' + '*_Txt.lua'):
                lua_files.append(lua_txt)
            for _bin in glob.iglob(root + '\\' + '*.bin'):
                bin_files.append(_bin)
        return [lua_files, bin_files]
    elif mode == constants.MODE_ENCODE:
        json_files = []
        for root, subdirs, files in os.walk(dir):
            if len(files) < 1:  # Skip dirs with no files
                continue
        for _bin in glob.iglob(root + '\\' + '*.json'):
            json_files.append(_bin)
        return json_files


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input_dir', required=True, nargs=1, type=str, help='Input directory')
    parser.add_argument('--output', dest='output_dir', required=True, nargs=1, type=str, help='Output directory')
    parser.add_argument('--mode', dest='mode', required=True, nargs=1, choices=['DECODE', 'ENCODE'], type=str, help='Mode')
    parser.add_argument('--threads', dest='threads', required=False, nargs=1, type=int, default=2, help='Max threads to use. Default is 2')
    args = parser.parse_args()

    mode = args.mode[0].upper()
    _input = args.input_dir[0]
    _output = args.output_dir[0]
    threads = args.threads

    files = find_files(mode, _input)  # Find files in given input dir

    jobs = []

    if mode == constants.MODE_DECODE:
        lua_files = files[0]
        bin_files = files[1]

        for lua_file_path in lua_files:
            something = something_to_do_with_files(_input, _output, lua_file_path)

            if os.path.isfile(_output + '\\' + something[2] + '.json'):
                if __debug__:  # Skip if not in dev workspace
                    print('Found already decoded json file... not decoding {0}...'.format(something[1] + '\\' + something[2]))
                    continue

            # Decode lua
            process = multiprocessing.Process(target=decode.decode_file, args=(something[0], something[1], something[2], _output))
            jobs.append(process)
            continue

        for bin_file_path in bin_files:
            something = something_to_do_with_files(_input, _output, bin_file_path)

            if os.path.isfile(_output + '\\' + something[2] + '.json'):
                if __debug__:  # Skip if not in dev workspace
                    print('Found already decoded json file... not decoding {0}...'.format(something[1] + '\\' + something[2]))
                    continue

            # Decode bin
            process = multiprocessing.Process(target=decode.decode_file, args=(something[0], something[1], something[2], _output))
            jobs.append(process)
            continue

        pass

    elif mode == constants.MODE_ENCODE:
        json_files = files

        for json_file_path in json_files:
            something = something_to_do_with_files(_input, _output, json_file_path)

            # Encode file
            process = multiprocessing.Process(target=encode.encode_file, args=(something[0], something[1], something[2], _output))
            jobs.append(process)
            continue

        pass

    processed_jobs = []
    for job_index in range(len(jobs)):
        job = jobs[job_index]

        if len(processed_jobs) == threads:
            for processed_job_index in range(len(processed_jobs)):
                processed_job = processed_jobs[processed_job_index]
                processed_job.join()
                continue

            processed_jobs.clear()
            pass

        job.start()

        processed_jobs.append(job)
        continue

    jobs.clear()


# Returns the input file's path, name
def something_to_do_with_files(_input, _output, input_file_path):
    file_name = None

    index1 = input_file_path.rfind('\\')
    if index1 != -1:
        file_name = input_file_path[(index1 + 1):]
    if file_name is None:
        raise file_name.UnknownError('Failed to get index of the file\'s name? This is not supposed to happen! Please inform the developer(s) about this error!')

    # Get only the path of the input file's directory
    index2 = input_file_path.find(file_name) - 1
    input_dir_path = input_file_path[:index2]
    input_dir_path = input_dir_path[(len(_input) + 1):]

    return [
        input_dir_path.replace('\\', '/'),
        input_file_path[:index1],
        file_name
    ]


if __name__ == '__main__':
    __main__()
