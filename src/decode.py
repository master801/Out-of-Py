#!/usr/bin/env python3

import os
import luaparser
from luaparser import ast
from luaparser import astnodes

if not __debug__:  # Dev workspace
    from src import constants
    from src import mahouka_json
    from src.formats import cadparam, cadtextparam, charmenuparam, imh_tuning_list_x_xx, magictext, magicparam, tutoriallist
else:
    import constants
    import mahouka_json
    from formats import cadparam, cadtextparam, charmenuparam, imh_tuning_list_x_xx, magictext, magicparam, tutoriallist


# Do not have output file as a file - No need to create a file if we're not using it yet
def decode_file(input_dir_path, full_input_dir_path, input_file_name, output_dir_path, overwrite):
    input_file_path = full_input_dir_path + constants.FILE_PATH_SEPARATOR + input_file_name
    ext = input_file_name[-4:].lower()
    if ext == '.lua':
        lua_input_file = open(input_file_path, 'rt', encoding='UTF-8')  # Open file as text for reading
        block = parse_lua(lua_input_file)
        serialized_lua_json = mahouka_json.serialize_lua(input_dir_path, input_file_name, block)
        write_json(serialized_lua_json, input_file_name, output_dir_path, overwrite)
        pass
    elif ext == '.bin':
        bin_input_file = open(input_file_path, 'rb')
        parsed_bin_blob = parse_bin(bin_input_file)

        if parsed_bin_blob is None:
            return

        _type = parsed_bin_blob[0]
        parsed_bin = parsed_bin_blob[1]
        serialized_bin_json = mahouka_json.serialize_bin(input_dir_path, input_file_name, _type, parsed_bin)
        write_json(serialized_bin_json, input_file_name, output_dir_path, overwrite)
        pass
    return


def parse_lua(lua_file):
    print('Decoding lua input file {0}...'.format(lua_file.name))

    tree = ast.parse(lua_file.read())

    block = {}
    for node in ast.walk(tree):
        if isinstance(node, astnodes.Block):
            print('Contains {0} blocks'.format(len(node.body)))
            for body_block in node.body:
                key_name = body_block.targets[0].id
                fields = body_block.values[0].fields

                print('Decoding text block \'{0}\''.format(key_name))
                print('Text block contains {0} entries'.format(len(fields)))

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
                continue
            continue
        continue
    return block


def decode_hex_utf8_string(encoded_hex_utf8_string):
    # Empty string
    if len(encoded_hex_utf8_string) < 1:
        return encoded_hex_utf8_string

    # String not encoded
    if not encoded_hex_utf8_string.startswith('\\x'):
        return encoded_hex_utf8_string

    split = encoded_hex_utf8_string.split('\\x')
    split.pop(0)

    concat = ''
    for i in range(len(split)):
        split_i = split[i]

        concat += split_i
        continue

    hexed = bytes.fromhex(concat)

    try:
        decoded = hexed.decode('utf-8')
        pass
    except UnicodeDecodeError:
        print('Failed to decode string!')
        print('String: \'{0}\''.format(encoded_hex_utf8_string))
        return encoded_hex_utf8_string

    return decoded


def write_json(serialized_json, input_file_name, output_dir_path, overwrite):
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
        pass

    output_file_path = output_dir_path + constants.FILE_PATH_SEPARATOR + input_file_name + '.json'

    if os.path.isfile(output_file_path):
        if overwrite:  # Only in dev workspace or if specified
            os.remove(output_file_path)
            pass
        else:
            print('Json file {0} already exists\n'.format(output_file_path))
            return
        pass

    output_file = open(output_file_path, mode='xt', newline=os.linesep)
    try:
        output_file.write(serialized_json)
        pass
    finally:
        output_file.close()
        pass
    return


def parse_bin(bin_file):
    bin_file_path = str
    some_index = bin_file.name.rindex(constants.FILE_PATH_SEPARATOR) + 1
    if some_index is not 0:
        bin_file_path = bin_file.name[some_index:]
        pass
    else:
        bin_file_path = bin_file_path
        pass

    bin_file_name = bin_file_path[:-4]

    _type = None
    for iterating_type in constants.TYPES_BIN:
        if bin_file_name.startswith(iterating_type[0]):
            _type = iterating_type[1]
            print('Detected type \"{0}\" for bin file {1}'.format(_type, bin_file.name))
            break
        elif bin_file_name.startswith('CharBattleParam') or bin_file_name.startswith('MeleeParam'):
            print('Bin file \"{0}\" is not supported!'.format(bin_file_path))
            return None
        continue

    if _type is None:
        print('Unknown type for bin file {0} - Defaulting to \"{1}\"'.format(bin_file.name, constants.TYPE_BIN_TUNING_LIST))
        _type = constants.TYPE_BIN_TUNING_LIST

    if _type == constants.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin
        parsed_bin = parse_bin_char_menu_param(bin_file)
        pass
    elif _type == constants.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin
        parsed_bin = parse_bin_cad_text_param(bin_file)
        pass
    elif _type == constants.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        parsed_bin = parse_bin_cad_param(bin_file)
        pass
    elif _type == constants.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        parsed_bin = parse_bin_magic_text(bin_file)
        pass
    elif _type == constants.TYPE_BIN_MAGIC_PARAM:  # MagicParam.bin
        parsed_bin = parse_bin_magic_param(bin_file)
        pass
    elif _type == constants.TYPE_BIN_TUTORIAL_LIST:  # TutorialList.bin
        parsed_bin = parse_bin_tutorial_list(bin_file)
        pass
    elif _type == constants.TYPE_BIN_TUNING_LIST:  # IMH_Tuning_List_X_XX.bin
        parsed_bin = parse_bin_tuning_list(bin_file)
        pass
    else:
        print('Unknown bin type!')
        print(_type)
        return None
    return [_type, parsed_bin]


def parse_bin_char_menu_param(bin_file):  # CharMenuParam.bin
    return charmenuparam.Charmenuparam.from_io(bin_file)


def parse_bin_cad_text_param(bin_file):  # CadTextParam.bin
    return cadtextparam.Cadtextparam.from_io(bin_file)


def parse_bin_cad_param(bin_file):  # CadParam.bin
    return cadparam.Cadparam.from_io(bin_file)


def parse_bin_magic_text(bin_file):  # MagicText.bin
    return magictext.Magictext.from_io(bin_file)


def parse_bin_magic_param(bin_file):  # MagicParam.bin
    return magicparam.Magicparam.from_io(bin_file)


def parse_bin_tutorial_list(bin_file):  # TutorialList.bin
    return tutoriallist.Tutoriallist.from_io(bin_file)


def parse_bin_tuning_list(bin_file):  # IMH_Tuning_List_X_XX.bin
    return imh_tuning_list_x_xx.ImhTuningListXXx.from_io(bin_file)
