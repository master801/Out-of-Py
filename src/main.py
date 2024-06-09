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
            for lua_txt in glob.iglob(root + constants.FILE_PATH_SEPARATOR + '*_Txt.lua'):
                lua_files.append(lua_txt)
                continue
            for _bin in glob.iglob(root + constants.FILE_PATH_SEPARATOR + '*.bin'):
                bin_files.append(_bin)
                continue
        return [lua_files, bin_files]
    elif mode == constants.MODE_ENCODE:
        json_files = []
        for root, subdirs, files in os.walk(dir):
            if len(files) < 1:  # Skip dirs with no files
                continue
            continue
        for _bin in glob.iglob(root + constants.FILE_PATH_SEPARATOR + '*.json'):
            json_files.append(_bin)
            continue
        return json_files


# Returns the input file's path, name
def something_to_do_with_files(_input, _output, input_file_path):
    file_name = None

    index1 = input_file_path.rfind(constants.FILE_PATH_SEPARATOR)
    if index1 != -1:
        file_name = input_file_path[(index1 + 1):]
        pass

    if file_name is None:
        raise file_name.UnknownError('Failed to get index of the file\'s name? This is not supposed to happen! Please inform the developer(s) about this error!')
        pass

    # Get only the path of the input file's directory
    index2 = input_file_path.find(file_name) - 1
    input_dir_path = input_file_path[:index2]
    input_dir_path = input_dir_path[(len(_input) + 1):]

    return [
        input_dir_path.replace('\\', '/'),
        input_file_path[:index1],
        file_name
    ]


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input_dir', required=True, nargs=1, type=str, help='Input directory')
    parser.add_argument('--output', dest='output_dir', required=True, nargs=1, type=str, help='Output directory')
    parser.add_argument('--mode', dest='mode', required=True, nargs=1, type=str, choices=['DECODE', 'ENCODE'], help='Mode')
    parser.add_argument('--threads', dest='threads', required=False, nargs=1, type=int, default=1, help='Max threads to use. Default is 1')
    parser.add_argument('--overwrite', dest='overwrite', required=False, nargs=1, type=bool, choices=[False, True], default=False)
    args = parser.parse_args()

    mode = args.mode[0].upper()
    _input = args.input_dir[0]
    _output = args.output_dir[0]
    overwrite = args.overwrite
    threads = args.threads[0]

    files = find_files(mode, _input)  # Find files in given input dir

    jobs = []

    if mode == constants.MODE_DECODE:
        lua_files = files[0]
        bin_files = files[1]

        for lua_file_path in lua_files:
            something = something_to_do_with_files(_input, _output, lua_file_path)

            if os.path.isfile(_output + constants.FILE_PATH_SEPARATOR + something[2] + '.json'):
                if not overwrite:
                    print('Found already decoded json file... not decoding file \"{0}/{1}\"'.format(something[1], something[2]))
                    continue
                pass
            pass

            # Decode lua
            if threads < 2:
                decode.decode_file(something[0], something[1], something[2], _output, overwrite)
                pass
            else:
                process = multiprocessing.Process(target=decode.decode_file, args=(something[0], something[1], something[2], _output, overwrite))
                jobs.append(process)
                pass
            continue

        for bin_file_path in bin_files:
            something = something_to_do_with_files(_input, _output, bin_file_path)

            if os.path.isfile(_output + constants.FILE_PATH_SEPARATOR + something[2] + '.json'):
                if not overwrite:
                    print('Found already decoded json file... not decoding file \"{0}/{1}\"'.format(something[1], something[2]))
                    continue
                pass
            pass

            # Decode bin
            if threads < 2:
                decode.decode_file(something[0], something[1], something[2], _output, overwrite)
                pass
            else:
                process = multiprocessing.Process(target=decode.decode_file, args=(something[0], something[1], something[2], _output, overwrite))
                jobs.append(process)
                pass
            continue
        pass
    elif mode == constants.MODE_ENCODE:
        json_files = files
        for json_file_path in json_files:
            something = something_to_do_with_files(_input, _output, json_file_path)

            # Encode file
            if threads < 2:
                encode.encode_file(something[0], something[1], something[2], _output, overwrite)
                pass
            else:
                process = multiprocessing.Process(target=encode.encode_file, args=(something[0], something[1], something[2], _output, overwrite))
                jobs.append(process)
                pass
            continue
        pass
    else:
        print('No mode specified!')
        return

    if len(jobs) < 1:
        print('Done!')
        return

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
    return


if __name__ == '__main__':
    __main__()
