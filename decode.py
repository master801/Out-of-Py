#!/usr/bin/env python3
# Created by Master on 4/3/2019

import os
import typing
import pathlib
import luaparser
from luaparser import ast
from luaparser import astnodes

import constants
import mahouka_json
from formats import cadparam, cadtextparam, charmenuparam, imh_tuning_list_x_xx, magictext, magicparam, tutoriallist


# Do not have output file as a file - No need to create a file if we're not using it yet
def decode_file(path_file: pathlib.Path, out_file: str, overwrite: bool):
    if path_file.suffix == '.lua':
        with open(path_file, 'rt', encoding='utf-8') as lua_input_file:
            block = parse_lua(lua_input_file)
            serialized_lua_json = mahouka_json.serialize_lua(block)
            write_json(serialized_lua_json, out_file, overwrite)
            pass
    elif path_file.suffix == '.bin':
        with open(path_file, 'rb') as io_bin:
            parsed_bin_blob = parse_bin(path_file.name, io_bin)
            if parsed_bin_blob is None:
                print(f'Failed to parse bin file \"{path_file}\"!')
                return
            pass
        del io_bin

        _type = parsed_bin_blob[0]
        parsed_bin = parsed_bin_blob[1]
        serialized_bin_json = mahouka_json.serialize_bin(_type, parsed_bin)
        write_json(serialized_bin_json, out_file, overwrite)
        del serialized_bin_json
        pass
    return


def parse_lua(lua_file: typing.TextIO) -> dict:
    print(f'Decoding lua input file {lua_file.name}...')

    tree = ast.parse(lua_file.read())

    block = {}
    for node in ast.walk(tree):
        if isinstance(node, astnodes.Block):
            print(f'Contains {len(node.body)} blocks')
            for body_block in node.body:
                key_name = body_block.targets[0].id
                fields = body_block.values[0].fields

                print(f'Decoding text block \'{key_name}\'')
                print(f'Text block contains {len(fields)} entries')

                sub_blocks = {}
                for index in range(len(fields)):
                    field = fields[index]
                    field_name = field.key.id

                    if isinstance(field.value, luaparser.astnodes.String):
                        field_value = decode_hex_utf8_string(field.value.s)
                        pass
                    elif isinstance(field.value, luaparser.astnodes.Concat):
                        values = []

                        tmp = field.value
                        while isinstance(tmp, astnodes.Concat):
                            if isinstance(tmp.left, astnodes.String):
                                values.append(tmp.left.s)
                                pass

                            values.append(tmp.right.s)
                            tmp = tmp.left
                            continue

                        value = []

                        if len(values) == 2:
                            value.append(decode_hex_utf8_string(values[0]))
                            value.append(decode_hex_utf8_string(values[1]))
                            pass
                        elif len(values) == 3:
                            value.append(decode_hex_utf8_string(values[1]))
                            value.append(decode_hex_utf8_string(values[2]))
                            value.append(decode_hex_utf8_string(values[0]))
                            pass
                        else:
                            print('More lines than expected in lua script file!')
                            pass

                        field_value = value
                        pass

                    sub_blocks[index] = {field_name: field_value}  # Add our mapped value
                    continue

                block.update({key_name: sub_blocks})

                print()  # New line = Pretty
                continue
            continue
        continue
    return block


def decode_hex_utf8_string(encoded_hex_utf8_string: str) -> str:
    # Empty string
    if len(encoded_hex_utf8_string) < 1:
        return encoded_hex_utf8_string

    # String not encoded
    if not encoded_hex_utf8_string.startswith('\\x'):
        return encoded_hex_utf8_string

    split = encoded_hex_utf8_string.split('\\x')
    split.pop(0)

    hexed = bytes.fromhex(''.join(split))
    try:
        decoded = hexed.decode('utf-8')
        pass
    except UnicodeDecodeError:
        print('Failed to decode string!')
        print(f'String: \'{encoded_hex_utf8_string}\'')
        return encoded_hex_utf8_string
    del hexed

    return decoded


def write_json(serialized_json, fp_out: str, overwrite: bool):
    if os.path.exists(fp_out):
        if overwrite:
            mode = 'w+'
            pass
        else:
            print(f'Json file \"{fp_out}\" already exists{os.linesep}!?')
            return
        pass
    else:
        mode = 'x'
        pass
    with open(fp_out, mode=f'{mode}t', newline=os.linesep, encoding='utf-8') as io_of:
        io_of.write(serialized_json)
        pass
    print(f'Wrote decoded JSON file \"{fp_out}\"')
    del mode
    del io_of
    return


def parse_bin(fn_bin: str, bin_file: typing.BinaryIO):
    _type = None
    for iterating_type in constants.TYPES_BIN:
        if fn_bin.startswith(iterating_type[0]):
            _type = iterating_type[1]
            print(f'Detected type \"{_type}\" for bin file {bin_file.name}')
            break
        elif fn_bin.startswith('CharBattleParam') or fn_bin.startswith('MeleeParam'):
            print(f'Bin file \"{fn_bin}\" is not supported!')
            return None
        continue

    if _type is None:
        print(f'Unknown type for bin file \"{bin_file.name}\" - Defaulting to \"{constants.Type.TYPE_BIN_TUNING_LIST}\"')
        _type = constants.Type.TYPE_BIN_TUNING_LIST
        pass

    if _type == constants.Type.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin
        parsed_bin = charmenuparam.Charmenuparam.from_io(bin_file)
        pass
    elif _type == constants.Type.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin
        parsed_bin = cadtextparam.Cadtextparam.from_io(bin_file)
        pass
    elif _type == constants.Type.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        parsed_bin = cadparam.Cadparam.from_io(bin_file)
        pass
    elif _type == constants.Type.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        parsed_bin = magictext.Magictext.from_io(bin_file)
        pass
    elif _type == constants.Type.TYPE_BIN_MAGIC_PARAM:  # MagicParam.bin
        parsed_bin = magicparam.Magicparam.from_io(bin_file)
        pass
    elif _type == constants.Type.TYPE_BIN_TUTORIAL_LIST:  # TutorialList.bin
        parsed_bin = tutoriallist.Tutoriallist.from_io(bin_file)
        pass
    elif _type == constants.Type.TYPE_BIN_TUNING_LIST:  # IMH_Tuning_List_X_XX.bin
        parsed_bin = imh_tuning_list_x_xx.ImhTuningListXXx.from_io(bin_file)
        pass
    else:
        print('Unknown bin type!')
        print(_type)
        return None
    return [_type, parsed_bin]
