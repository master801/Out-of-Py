#!/usr/bin/env python3

import os
import struct

from luaparser import ast
from luaparser import astnodes

from src import constants
from src import mahouka_json

from src.formats import cadparam
from src.formats import cadtextparam
from src.formats import charmenuparam
from src.formats import imh_tuning_list_x_xx
from src.formats import magictext
from src.formats import tutoriallist


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
        if _type == 'TuningList':  # TODO
            write_json(serialized_bin_json, input_file_name, output_dir_path)  # TODO


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

    if _type == constants.TYPE_BIN_CHAR_BATTLE_PARAM:  # CharBattleParam.bin
        parsed_bin = parse_bin_char_battle_param(bin_file)  # TODO
    elif _type == constants.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin
        parsed_bin = parse_bin_char_menu_param(bin_file)
    elif _type == constants.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin
        parsed_bin = parse_bin_cad_text_param(bin_file)
    elif _type == constants.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        parsed_bin = parse_bin_cad_param(bin_file)
    elif _type == constants.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        parsed_bin = parse_bin_magic_text(bin_file)
    elif _type == constants.TYPE_BIN_TUTORIAL_LIST:  # TutorialList.bin
        parsed_bin = parse_bin_tutorial_list(bin_file)
    elif _type == constants.TYPE_BIN_TUNING_LIST:  # IMH_Tuning_List_X_XX.bin
        parsed_bin = parse_bin_tuning_list(bin_file)
    elif _type is None:
        print('Unknown bin type!')
        return None
    return [_type, parsed_bin]


def parse_bin_char_battle_param(bin_file):
    return [bytes]  # TODO


def parse_bin_char_menu_param(bin_file):
    return cadtextparam.Cadtextparam.from_io(bin_file)


def parse_bin_cad_text_param(bin_file):  # CadTextParam.bin
    return cadtextparam.Cadtextparam.from_io(bin_file)


def parse_bin_cad_param(bin_file):  # CadParam.bin
    return cadparam.Cadparam.from_io(bin_file)


def parse_bin_magic_text(bin_file):  # MagicText.bin
    return magictext.Magictext.from_io(bin_file)


def parse_bin_tutorial_list(bin_file):  # TutorialList.bin
    return tutoriallist.Tutoriallist.from_io(bin_file)


def parse_bin_tuning_list(bin_file):  # IMH_Tuning_List_X_XX.bin
    return imh_tuning_list_x_xx.ImhTuningListXXx.from_io(bin_file)
