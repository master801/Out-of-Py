#!/usr/bin/env python3
import struct

from src import mahouka_json, constants
from src.builders import builders


def encode_file(input_dir_path, full_input_dir_path, input_file_name, output_dir_path):
    input_file_path = full_input_dir_path + '/' + input_file_name

    print('Found json file \"{0}\"'.format(input_file_path))

    input_file = open(input_file_path, mode='rt')
    input_file_data = input_file.read()
    deserialized_file_container = mahouka_json.deserialize_file_container(input_file_data)

    _type = deserialized_file_container[0]
    deserialized_file_path = deserialized_file_container[1]
    deserialized_block = deserialized_file_container[2]

    encoded_file_data = encode_file_data(_type, deserialized_block)

    if encoded_file_data is None:
        print('Failed to deserialize file?!')
        return

    write_encoded(deserialized_file_path, output_dir_path, _type, encoded_file_data)

    print('Wrote deserialized file \"{0}\" to \"{1}\"\n'.format(input_file_path, output_dir_path + '/' + deserialized_file_path))


def encode_file_data(_type, deserialized):
    if _type == constants.TYPE_LUA:
        return encode_lua(deserialized)  # TODO
    elif _type == constants.TYPE_BIN_CHAR_BATTLE_PARAM:  # Not yet supported TODO
        return encode_bin_char_battle_param(deserialized)  # TODO
    elif _type == constants.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin TODO
        return encode_bin_menu_param(deserialized)
    elif _type == constants.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin TODO
        return encode_bin_char_menu_param(deserialized)
    elif _type == constants.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        return encode_bin_cad_param(deserialized)
    elif _type == constants.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        return encode_bin_magic_text(deserialized)
    elif _type == constants.TYPE_BIN_TUTORIAL_LIST:  # TutorialList.bin
        return encode_bin_tutorial_list(deserialized)
    elif _type == constants.TYPE_BIN_TUNING_LIST:  # IMH_Tuning_List_X_XX.bin
        return encode_bin_tuning_list(deserialized)


def encode_lua(deserialized):
    blocks = []
    for deserialized_block_key in deserialized:
        deserialized_block = deserialized[deserialized_block_key]

        name = None
        txt_list = None
        voice = None

        if len(deserialized_block) > 0:
            name = deserialized_block['0']['name']
            txt_list = deserialized_block['1']['txt']
            voice = deserialized_block['2']['voice']

        builder = builders.BlockBuilder(deserialized_block_key, name, txt_list, voice)
        line = builder.to_source()

        blocks.append(line)
        continue

    data = bytearray()

    for block in blocks:
        encoded_bytes = block.encode('utf-8')
        data[len(data):len(encoded_bytes)] = encoded_bytes
        continue

    return data


def encode_bin_char_battle_param(deserialized):
    print()  # TODO
    return None


def encode_bin_menu_param(deserialized):
    print()  # TODO
    return None


def encode_bin_char_menu_param(deserialized):
    data_block = bytearray(constants.LENGTH_BIN_CHAR_MENU_PARAM_CHUNK * len(deserialized))

    for index in range(len(deserialized)):
        block = deserialized[index]

        block_data = bytearray(constants.LENGTH_BIN_CHAR_MENU_PARAM_CHUNK)
        block_data[0x00:0x04] = struct.pack('<L', block['index'])
        block_data[0x04:0x44] = bytearray(block['title'].encode('utf-8')).ljust(0x40).replace(b' ', b'\x00')
        block_data[0x44:0x144] = bytearray(block['text'].encode('utf-8')).ljust(0x100).replace(b' ', b'\x00')

        data_block[index * constants.LENGTH_BIN_CHAR_MENU_PARAM_CHUNK: (index + 1) * constants.LENGTH_BIN_CHAR_MENU_PARAM_CHUNK] = block_data
        continue

    return data_block


def encode_bin_cad_param(deserialized):
    params = deserialized['params']

    data_block = bytearray(constants.LENGTH_BIN_CAD_PARAM_CHUNK * len(params))

    for param_index in range(len(params)):
        param = params[param_index]
        param_data_block = bytearray(constants.LENGTH_BIN_CAD_PARAM_CHUNK)

        index = param['index']
        sub_index = param['sub_index']
        text = param['text']
        unknown_1 = param['unknown_1']
        unknown_2 = param['unknown_2']
        unknown_3 = param['unknown_3']
        unknown_4 = param['unknown_4']
        unknown_5 = param['unknown_5']
        unknown_6 = param['unknown_6']
        unknown_7 = param['unknown_7']
        unknown_8 = param['unknown_8']
        unknown_9 = param['unknown_9']
        unknown_10 = param['unknown_10']
        # unknown_11 = param['unknown_11']
        unknown_12 = param['unknown_12']

        param_data_block[0x00:0x04] = struct.pack('<L', index)
        param_data_block[0x04:0x104] = bytearray(text.encode('utf-8')).ljust(0x100).replace(b' ', b'\x00')
        param_data_block[0x104:0x108] = struct.pack('<L', sub_index)
        param_data_block[0x108:0x10C] = struct.pack('<L', unknown_1)
        param_data_block[0x10C:0x110] = struct.pack('>L', unknown_2)
        param_data_block[0x110:0x114] = struct.pack('>L', unknown_3)
        param_data_block[0x114:0x118] = struct.pack('>L', unknown_4)
        param_data_block[0x118:0x11C] = struct.pack('>L', unknown_5)
        param_data_block[0x11C:0x120] = struct.pack('>L', unknown_6)
        param_data_block[0x120:0x124] = struct.pack('>L', unknown_7)
        param_data_block[0x124:0x128] = struct.pack('>L', unknown_8)
        param_data_block[0x128:0x12C] = struct.pack('>L', unknown_9)
        param_data_block[0x12C:0x130] = struct.pack('>L', unknown_10)
        # 0x130-0x160 contains only 0x00 padding
        param_data_block[0x160:0x164] = struct.pack('<L', unknown_12)

        data_block[param_index * constants.LENGTH_BIN_CAD_PARAM_CHUNK: (param_index + 1) * constants.LENGTH_BIN_CAD_PARAM_CHUNK] = param_data_block
        continue

    return data_block


def encode_bin_magic_text(deserialized):
    data_block = bytearray()

    for entry_index in range(len(deserialized)):
        entry = deserialized[entry_index]

        entry_data = bytearray()

        id_1 = entry['id_1']
        id_2 = entry['id_2']
        text = entry['text']

        entry_data[0x00:0x04] = struct.pack('<L', id_1)
        entry_data[0x04:0x08] = struct.pack('<L', id_2)
        entry_data[0x08:0x208] = text.encode('utf-8').ljust(0x200, b'\x00')

        start_offset = constants.LENGTH_BIN_MAGIC_TEXT_CHUNK * entry_index
        end_offset = constants.LENGTH_BIN_MAGIC_TEXT_CHUNK * (entry_index + 1)

        data_block[start_offset:end_offset] = entry_data
        continue
    return data_block


def encode_bin_tutorial_list(deserialized):
    length = deserialized['length']
    entries = deserialized['entries']

    data_block = bytearray()

    data_block[0x00:0x04] = struct.pack('<L', length)

    for entry_index in range(len(entries)):
        entry = entries[entry_index]

        entry_data_block = bytearray()

        current_page_index = entry['current_page_index']
        last_page_index = entry['last_page_index']
        previous_page_index = entry['previous_page_index']
        next_page_index = entry['next_page_index']

        unknown_1 = entry['unknown_1']
        unknown_2 = entry['unknown_2']
        unknown_3 = entry['unknown_3']

        title = entry['title']
        text = entry['text']

        title_data = title.encode('utf-8')
        text_data = text.encode('utf-8')

        entry_data_block[0x00:0x04] = struct.pack('<L', current_page_index)
        entry_data_block[0x04:0x08] = struct.pack('<L', last_page_index)
        entry_data_block[0x08:0x0C] = struct.pack('<L', previous_page_index)
        entry_data_block[0xC:0x10] = struct.pack('<L', next_page_index)

        entry_data_block[0x10:0x14] = struct.pack('<L', unknown_1)
        entry_data_block[0x18:0x1C] = struct.pack('<L', unknown_2)
        entry_data_block[0x1C:0x20] = struct.pack('<L', unknown_3)

        entry_data_block[0x20:0xA0] = title_data.ljust(0x80, b'\x00')
        entry_data_block[0xA0:0x00] = text_data.ljust(0x200, b'\x00')

        start_offset = 0x04 + (constants.LENGTH_BIN_TUTORIAL_LIST_CHUNK * entry_index)
        end_offset = 0x04 + (constants.LENGTH_BIN_TUTORIAL_LIST_CHUNK * (entry_index + 1))
        data_block[start_offset:end_offset] = entry_data_block
        continue
    return data_block


def encode_bin_tuning_list(deserialized):
    data_block = bytearray()

    for map_index in range(len(deserialized)):
        map = deserialized[map_index]
        sub_data_block = bytearray()

        id = map['id']
        entries = map['entries']

        sub_data_block[0x00:0x04] = struct.pack('<L', id)

        for entry_index in range(len(entries)):
            entry = entries[entry_index]

            text_data_block = bytearray(0x140)

            title = entry['title']
            text = entry['text']

            text_data = text.encode('utf-8')
            title_data = title.encode('utf-8')

            padded_text_data = text_data.ljust(0x100, b'\x00')
            padded_title_data = title_data.ljust(0x40, b'\x00')

            text_data_block[0x00:0x100] = padded_text_data
            text_data_block[0x100:0x140] = padded_title_data

            previous_index = 0x04 + (0x140 * entry_index)
            next_index = 0x04 + (0x140 * (entry_index + 1))

            sub_data_block[previous_index:next_index] = text_data_block
            continue

        previous_index_1 = 0x04 + (0x04 + (0x140 * len(entries))) * map_index
        next_index_1 = (0x04 + (0x140 * len(entries))) * (map_index + 1)
        data_block[previous_index_1:next_index_1] = sub_data_block
        continue
    return data_block


def write_encoded(output_file_path, output_dir, _type, deserialized_file):
    output_file_complete_path = output_dir + '/' + output_file_path

    # TODO REMOVE - DEBUG
    import os
    if os.path.exists(output_file_complete_path):
        os.remove(output_file_complete_path)

    output_file = open(output_file_complete_path, mode='x+b')
    try:
        output_file.write(deserialized_file)
    finally:
        output_file.close()
