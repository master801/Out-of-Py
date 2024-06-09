#!/usr/bin/env python3

import os
import struct

from luaparser import ast
from luaparser import astnodes

import constants
import mahouka_json


# Do not have output file as a file - No need to create a file if we're not using it yet
def decode_file(input_dir_path, full_input_dir_path, input_file_name, output_dir_path):
    input_file_path = full_input_dir_path + '\\' + input_file_name
    ext = input_file_name[-4:].lower()
    if ext == '.lua':
        output_file_path = output_dir_path + '\\' + input_file_name + '.json'
        if os.path.isfile(output_file_path):
            print('Found already decoded json file... not decoding {0}...'.format(input_file_path))
            return

        lua_input_file = open(input_file_path, 'rt', encoding='UTF-8')  # Open file as text for reading
        block = parse_lua(lua_input_file)
        serialized_lua_json = mahouka_json.serialize_lua(input_dir_path, input_file_name, block)
        write_json(serialized_lua_json, input_file_name, output_dir_path)
    elif ext == '.bin':
        bin_input_file = open(input_file_path, 'rb')
        parsed_bin_blob = parse_bin(bin_input_file)
        _type = parsed_bin_blob[0]
        parsed_bin = parsed_bin_blob[1]
        serialized_bin_json = mahouka_json.serialize_bin(input_dir_path, input_file_name, _type, parsed_bin)
        if _type == 'Param' or _type == 'Text' or _type == 'List' or _type == 'Page' or _type == 'TextParam':  # TODO
            write_json(serialized_bin_json, input_file_name, output_dir_path) # TODO


def parse_lua(lua_file):
    print('Decoding lua input file {0}...'.format(lua_file.name))

    tree = ast.parse(lua_file.read())

    block = {}
    for node in ast.walk(tree):
        if isinstance(node, astnodes.Block):
            for body_block in node.body:
                value_map = body_block.values[0]

                key_name = body_block.targets[0].id

                key_list = value_map.keys
                value_list = value_map.values

                if len(key_list) != len(value_list):  # Check lists for consistency
                    print('Key ({0}) and values ({1}) for block \"{2}\" are inconsistent!'.format(len(key_list), len(value_list), key_name))
                    break

                sub_blocks = {}
                for index in range(len(key_list)):
                    key = key_list[index].id
                    value = value_list[index]

                    if isinstance(value, astnodes.Concat):
                        concants = []

                        tmp = value
                        while isinstance(tmp, astnodes.Concat):
                            concants.insert(0, tmp)  # Insert at the top of the stack
                            tmp = tmp.left
                            continue

                        value = []
                        last_index = -1
                        for concant_index in range(len(concants) - 1):  # Iterate over all concants besides the last
                            concant = concants[concant_index]

                            if last_index == -1 or last_index == concant_index + 1:
                                last_index = concant_index + 1

                            value.insert(concant_index, concant.left.s)
                            value.insert(last_index, concant.right.s)
                            continue

                        if len(concants) > 0:
                            # Insert the 'right' concant last
                            value.insert(last_index + 1, concants[len(concants) - 1].right.s)
                    else:
                        value = value.s

                    # if key == 'txt' and len(value) > 0:
                    #     for value_index in range(len(value)):
                    #         decoded_string = decode_string_bullshit(value[value_index])
                    #         value[value_index] = decoded_string
                    #         continue
                    # else:
                    #     decoded_string = decode_string_bullshit(value)
                    #     value = decoded_string

                    sub_blocks[index] = {key: value}  # Add our mapped value
                    continue

                block.update({key_name: sub_blocks})
                continue
            continue
        continue
    return block


def decode_string_bullshit(bullshit_string):
    # TODO
    return bullshit_string


def write_json(serialized_json, input_file_name, output_dir_path):
    output_file_path = output_dir_path + '\\' + input_file_name + '.json'

    if os.path.isfile(output_file_path):
        print('Json file {0} already exists'.format(output_file_path))
        return

    output_file = open(output_file_path, mode='xt', newline='\n')
    try:
        output_file.write(serialized_json)
    finally:
        output_file.close()


def parse_bin(bin_file):
    bin_file_path = str
    some_index = bin_file.name.rindex('\\') + 1
    if some_index != 0:
        bin_file_path = bin_file.name[some_index:]
    else:
        bin_file_path = bin_file_path

    bin_file_name = bin_file_path[:-4]

    _type = None
    parsed_bin = None
    for iterating_type in constants.TYPES_BIN:
        if bin_file_name.endswith(iterating_type):
            _type = iterating_type
            print('Detected type \"{0}\" for bin file {1}'.format(_type, bin_file.name))
            break
        continue

    if _type is None:
        print('Unknown type for bin file {0} - Defaulting to \"{1}\"'.format(bin_file.name, _type))
        _type = constants.TYPES_BIN[len(constants.TYPES_BIN) - 1]

    if _type == constants.TYPE_BIN_BATTLE_PARAM:  # CharBattleParam.bin
        parsed_bin = parse_bin_battle_param(bin_file)  # TODO
    elif _type == constants.TYPE_BIN_MENU_PARAM:  # CharMenuParam.bin
        parsed_bin = parse_bin_menu_param(bin_file)  # TODO
    elif _type == constants.TYPE_BIN_TEXT_PARAM:  # CadTextParam.bin
        parsed_bin = parse_bin_text_param(bin_file)
    elif _type == constants.TYPE_BIN_PARAM:  # CadParam.bin
        parsed_bin = parse_bin_param(bin_file)
    elif _type == constants.TYPE_BIN_TEXT:  # MagicText.bin
        parsed_bin = parse_bin_text(bin_file)
    elif _type == constants.TYPE_BIN_LIST:  # TutorialList.bin
        parsed_bin = parse_bin_list(bin_file)
    elif _type == constants.TYPE_BIN_PAGE:
        parsed_bin = parse_bin_page(bin_file)
    elif _type is None:
        print('Unknown bin type!')
        return None
    return [_type, parsed_bin]


def parse_bin_battle_param(bin_file):
    return [bytes]  # TODO


def parse_bin_menu_param(bin_file):
    return [bytes]  # TODO


def parse_bin_text_param(bin_file):
    chunk_size = 0x144
    offsets = [0x00, 0x04, 0x44, 0x100]
    read_chunks = []

    # Read chunks by 0x144
    read_chunk = bin_file.read(chunk_size)
    while read_chunk:
        read_chunks.append(read_chunk)
        read_chunk = bin_file.read(chunk_size)
        continue

    parsed_chunk_data = []
    for chunk in read_chunks:
        parsed_chunk = []
        index_bytes = chunk[offsets[0]:offsets[1]]
        title_bytes = chunk[offsets[1]:offsets[2]]
        text_bytes = chunk[offsets[2]:offsets[3]]

        parsed_chunk.append(index_bytes)
        parsed_chunk.append(title_bytes)
        parsed_chunk.append(text_bytes)

        parsed_chunk_data.append(parsed_chunk)
        continue

    return parsed_chunk_data


def parse_bin_param(bin_file):
    lengths = [0x04, 0x100, 0x04, 0x04, 0x02, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x3A, 0x04]
    chunk_size = 0x164
    read_chunks = []

    read_chunk = bin_file.read(chunk_size)
    while read_chunk:
        read_chunks.append(read_chunk)
        read_chunk = bin_file.read(chunk_size)
        continue

    parsed_chunk_data = []
    for chunk in read_chunks:
        chunk_data = []

        last_index = 0x0
        length_index = 0
        while last_index != chunk_size:
            first_index = last_index
            last_index = last_index + lengths[length_index]
            length_index += 1

            read_chunk_data = chunk[first_index:last_index]
            chunk_data.append(read_chunk_data)
            continue
        parsed_chunk_data.append(chunk_data)
        continue
    return parsed_chunk_data


def parse_bin_text(bin_file):
    chunk_length = 0x208

    read_chunks = []
    read_data = bin_file.read(chunk_length)
    while read_data:
        read_chunks.append(read_data)
        read_data = bin_file.read(chunk_length)
        continue

    read_chunk_data = []
    lengths = [0x4, 0x4, 0x200]
    for read_chunk in read_chunks:
        chunk_data = []
        end_offset = 0x0
        for length_index in range(len(lengths)):
            length = lengths[length_index]
            start_offset = end_offset
            end_offset = end_offset + length

            got_chunk = read_chunk[start_offset:end_offset]
            chunk_data.append(got_chunk)
            continue
        read_chunk_data.append(chunk_data)
        continue
    return read_chunk_data


def parse_bin_list(bin_file):
    read_data = bin_file.read()

    read_chunks = []

    # Read amount of entries
    entries = struct.unpack('<L', read_data[0x00:0x04])[0]  # Num of entries in this list

    # Read chunk blocks from amount of entries
    chunk_length = 0x29C
    start_index = 0x4
    end_index = start_index + chunk_length
    for entry_index in range(entries):
        chunk_data = read_data[start_index:end_index]
        read_chunks.append(chunk_data)

        start_index = end_index
        end_index = start_index + chunk_length
        continue

    # Read chunk data
    read_chunk_data = []
    for read_chunk in read_chunks:
        lengths = [0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x80, 0x200]
        chunk = []

        end_offset = 0x0
        for length_index in range(len(lengths)):
            length = lengths[length_index]
            start_offset = end_offset
            end_offset = end_offset + length

            got_chunk = read_chunk[start_offset:end_offset]
            chunk.append(got_chunk)
            continue
        read_chunk_data.append(chunk)
        continue

    return read_chunk_data


def parse_bin_page(bin_file):
    read_bin_data = bin_file.read()

    data_chunks = []

    data_chunk_length = 0x140
    start_offset = 0x00
    end_offset = 0x04
    data_chunk = []
    while True:
        if end_offset >= len(read_bin_data):
            break

        _id = None
        read_data = read_bin_data[start_offset:end_offset]
        if read_data[1] == 0x00 and read_data[2] == 0x00 and read_data[3] == 0x00:
            if len(read_data) > 4:
                _id = read_data[0:4]
            else:
                _id = read_data
            start_offset = start_offset + 0x04
            end_offset = start_offset + data_chunk_length
            if len(data_chunk) > 0:
                data_chunks.append(data_chunk)
                data_chunk = []
        elif read_data[0] == 0x00 and read_data[1] and read_data[2] and read_data[3]:
            start_offset += 0x04
            end_offset += 0x04
            continue

        if _id is not None and len(_id) == 0x04:
            data_chunk.append(_id)
        else:
            if len(data_chunk) > 0:
                data_chunk.append(read_data)
                start_offset = end_offset
                end_offset += data_chunk_length
        continue

    data_blocks = []
    for data_chunk_index in range(len(data_chunks)):
        data_chunk = data_chunks[data_chunk_index]

        data_block = [data_chunk[0]]
        for data_block_index in range(len(data_chunk) - 1):
            data_sub_block = []
            data_block_index += 1  # Offset by 1 to avoid getting id

            text_data = data_chunk[data_block_index][0x00:0x100]
            title_data = data_chunk[data_block_index][0x100:0x140]

            data_sub_block.append(text_data)
            data_sub_block.append(title_data)

            data_block.append(data_sub_block)
            continue
        data_blocks.append(data_block)
        continue

    return data_blocks
