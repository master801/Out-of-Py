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


def _find_files(mode, _dir):
    if mode == constants.MODE_DECODE:
        return [
            *(pathlib.Path(i) for i in glob.iglob(os.path.join(_dir, '**', '*_Txt.lua'), recursive=True)),
            *(pathlib.Path(i) for i in glob.iglob(os.path.join(_dir, '**', '*.bin'), recursive=True))
        ]
    elif mode == constants.MODE_ENCODE:
        return [
            *(pathlib.Path(i) for i in glob.iglob(os.path.join(_dir, '**', '*.csv'), recursive=True)),
            *(pathlib.Path(i) for i in glob.iglob(os.path.join(_dir, '**', '*.json'), recursive=True))
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
    _output = pathlib.Path(args.output[0])
    threads = args.threads[0]

    fps: list[pathlib.Path] = _find_files(mode, _input)  # Find files in given input dir
    if fps == None:
        print('Could not find any files?!')
        return

    if not os.path.exists(_output):
        os.makedirs(_output)
        pass

    jobs: list[multiprocessing.Process] = []
    if mode == constants.MODE_DECODE:
        for fp in fps:
            for _type in constants.Type:
                matches = _type.value.regex.match(fp.name)
                if matches != None:
                    if threads <= 1:
                        decode.decode_file(
                            fp,
                            pathlib.Path(
                                os.path.join(_output, ''.join([fp.name, _type.value.decode_ext]))
                            ),
                            _type,
                            args.overwrite
                        )
                        pass
                    else:
                        process = multiprocessing.Process(
                            target=decode.decode_file,
                            args=(
                                fp,
                                pathlib.Path(
                                    os.path.join(_output, ''.join([fp.name, _type.value.decode_ext]))
                                ),
                                _type,
                                args.overwrite
                            )
                        )
                        jobs.append(process)
                        del process
                        pass
                    break
                del matches
                continue
            del _type
            continue
        del fp
        pass
    elif mode == constants.MODE_ENCODE:
        for fp in fps:
            for _type in constants.Type:
                matches = _type.value.regex.match(fp.name)
                if matches != None:
                    if threads <= 1:
                        encode.encode_file(
                            fp,
                            pathlib.Path(_output),
                            _type,
                            args.overwrite
                        )
                        pass
                    else:
                        process = multiprocessing.Process(
                            target=encode.encode_file,
                            args=(
                                fp,
                                pathlib.Path(_output),
                                _type,
                                args.overwrite
                            )
                        )
                        jobs.append(process)
                        del process
                        pass
                    break
                continue
            del _type
            continue
        del fp
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
