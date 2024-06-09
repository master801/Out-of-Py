#!/usr/bin/env python3
# Created by Master on 6/5/2019

import argparse
import os
import pathlib
import glob
import multiprocessing

import constants
import decode
import encode


def find_files(mode, _dir):
    if mode == constants.MODE_DECODE:
        return [
            [
                pathlib.Path(i) for i in glob.iglob(os.path.join(_dir, '**', '*_Txt.lua'), recursive=True)
            ],
            [
                pathlib.Path(i) for i in glob.iglob(os.path.join(_dir, '**', '*.bin'), recursive=True)
            ]
        ]
    elif mode == constants.MODE_ENCODE:
        return [
            pathlib.Path(i) for i in glob.iglob(os.path.join(_dir, '**', '*.json'), recursive=True)
        ]
    else:
        return None


# noinspection PyComparisonWithNone
def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mode',
        required=True,
        nargs=1,
        type=str,
        choices=[constants.MODE_DECODE, constants.MODE_ENCODE],
        help='Mode'
    )
    group = parser.add_argument_group('FIFO')
    group.add_argument(
        '--input',
        required=True,
        nargs=1,
        type=str,
        help='Input directory'
    )
    group.add_argument(
        '--output',
        required=True,
        nargs=1,
        type=str,
        help='Output directory'
    )
    del group
    parser.add_argument(
        '--threads',
        required=False,
        nargs=1,
        type=int,
        default=[1],
        help='Max threads to use. Default is 1'
    )
    parser.add_argument(
        '--overwrite',
        required=False,
        action='store_true'
    )
    args = parser.parse_args()
    del parser

    mode = args.mode[0].upper()
    _input = args.input[0]
    _output = args.output[0]
    threads = args.threads[0]

    files = find_files(mode, _input)  # Find files in given input dir
    if files == None:
        print('Could not find any files?!')
        return

    jobs: list[multiprocessing.Process] = []
    if mode == constants.MODE_DECODE:
        for path_lua in files[0]:
            fp_out_lua = os.path.join(_output, path_lua.name + '.json')
            if os.path.isfile(fp_out_lua):
                if not args.overwrite:
                    print(f'Found already decoded JSON file \"{path_lua}\"...{os.linesep}')
                    continue
                pass
            pass

            # Decode lua
            if threads <= 2:
                decode.decode_file(path_lua, fp_out_lua, args.overwrite)
                pass
            else:
                process = multiprocessing.Process(
                    target=decode.decode_file,
                    args=(path_lua, fp_out_lua, args.overwrite)
                )
                jobs.append(process)
                pass
            del fp_out_lua
            continue
        del path_lua

        for path_bin in files[1]:
            fp_out_bin = os.path.join(_output, path_bin.name + '.json')
            if os.path.isfile(fp_out_bin):
                if not args.overwrite:
                    print(f'Found already decoded JSON file \"{path_bin}\"...{os.linesep}')
                    continue
                pass
            pass

            # Decode bin
            if threads < 2:
                decode.decode_file(path_bin, fp_out_bin, args.overwrite)
                pass
            else:
                process = multiprocessing.Process(
                    target=decode.decode_file,
                    args=(path_bin, fp_out_bin, args.overwrite)
                )
                jobs.append(process)
                del process
                pass
            del fp_out_bin
            continue
        del path_bin
        pass
    elif mode == constants.MODE_ENCODE:
        for path_json in files:
            # Encode file
            if threads <= 2:
                encode.encode_file(path_json, _output, args.overwrite)
                pass
            else:
                process = multiprocessing.Process(
                    target=encode.encode_file,
                    args=(path_json, _output, args.overwrite)
                )
                jobs.append(process)
                del process
                pass
            continue
        del path_json
        pass
    else:
        print('No mode specified!')
        return

    if len(jobs) < 1:
        print('Done!')
        return

    processed_jobs: list[multiprocessing.Process] = []
    for job_index in range(len(jobs)):
        job: multiprocessing.Process = jobs[job_index]
        if len(processed_jobs) == threads:
            for processed_job_index in range(len(processed_jobs)):
                processed_job = processed_jobs[processed_job_index]
                processed_job.join()
                continue

            processed_jobs.clear()
            pass
        job.start()
        processed_jobs.append(job)
        del job
        continue
    del job_index
    del processed_jobs

    jobs.clear()
    return


if __name__ == '__main__':
    __main__()
    pass
