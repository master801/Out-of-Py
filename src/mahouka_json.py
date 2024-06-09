#!/usr/bin/env python3

import constants
import json
import struct


def deserialize_file(file):
    deserialized_json = json.loads(file)

    _type = deserialized_json['type']
    file_path = deserialized_json['file_path']
    blocks = deserialized_json['blocks']

    deserialized = None
    if _type == constants.TYPE_LUA:
        deserialized = deserialize_lua(blocks)
    elif _type == constants.TYPE_BIN_BATTLE_PARAM:  # Not yet supported TODO
        deserialized = deserialize_bin_battle_param(blocks)
    elif _type == constants.TYPE_BIN_MENU_PARAM:  # CharMenuParam.bin TODO
        deserialized = deserialize_bin_menu_param(blocks)
    elif _type == constants.TYPE_BIN_MENU_PARAM:  # CadTextParam.bin TODO
        deserialized = deserialize_bin_text_param(blocks)
    elif _type == constants.TYPE_BIN_PARAM:  # CadParam.bin
        deserialized = deserialize_bin_param(blocks)
    elif _type == constants.TYPE_BIN_TEXT:  # MagicText.bin
        deserialized = deserialize_bin_text(blocks)
    elif _type == constants.TYPE_BIN_LIST:
        deserialized = deserialize_bin_list(blocks)
    elif _type == constants.TYPE_BIN_PAGE:
        deserialized = deserialize_bin_page(blocks)
    return [_type, file_path, deserialized]


def serialize_lua(input_dir_path, file_name, block):
    wrapped_block = {}
    wrapped_block.update({'type': constants.TYPE_LUA})
    wrapped_block.update({'file_path': input_dir_path + "/" + file_name})
    wrapped_block.update({'blocks': block})
    return json.dumps(wrapped_block, indent=2, ensure_ascii=False)


def deserialize_lua(blocks):

    print()
    return None


def serialize_bin(input_dir_path, file_name, _type, _bin):
    blocks = serialize_bin_type(_type, _bin)

    wrapped_block = {}
    wrapped_block.update({'type': _type})
    wrapped_block.update({'file_path': input_dir_path + "/" + file_name})
    wrapped_block.update({'blocks': blocks})
    return json.dumps(wrapped_block, indent=2, ensure_ascii=False)


def serialize_bin_type(_type, _bin):
    if _type == constants.TYPE_BIN_BATTLE_PARAM:  # Not yet supported TODO
        return serialize_bin_battle_param(_bin)
    elif _type == constants.TYPE_BIN_MENU_PARAM:  # CharMenuParam.bin TODO
        return serialize_bin_menu_param(_bin)
    elif _type == constants.TYPE_BIN_TEXT_PARAM:  # CadTextParam.bin TODO
        return serialize_bin_text_param(_bin)
    elif _type == constants.TYPE_BIN_PARAM:  # CadParam.bin
        return serialize_bin_param(_bin)
    elif _type == constants.TYPE_BIN_TEXT:  # MagicText.bin
        return serialize_bin_text(_bin)
    elif _type == constants.TYPE_BIN_LIST:
        return serialize_bin_list(_bin)
    elif _type == constants.TYPE_BIN_PAGE:
        return serialize_bin_page(_bin)


def serialize_bin_battle_param(_bin):
    return None  # TODO


def deserialize_bin_battle_param(blocks):
    return None  # TODO


def serialize_bin_menu_param(_bin):
    return None  # TODO


def deserialize_bin_menu_param(blocks):
    return None  # TODO


def serialize_bin_text_param(_bin):
    block_chain = []
    for bin_block in _bin:
        block = []

        _index = struct.unpack('<L', bin_block[0])[0]

        title_bytes = bin_block[1]
        title_bytes_trim_index = title_bytes.find(b'\x00')
        if title_bytes_trim_index != -1:
            title_bytes_trimmed = title_bytes[:title_bytes_trim_index]
        else:
            title_bytes_trimmed = title_bytes
        title = title_bytes_trimmed.decode('utf-8')

        text_bytes = bin_block[2]
        text_bytes_trim_index = text_bytes.find(b'\x00')
        if text_bytes_trim_index != -1:
            text_bytes_trimmed = text_bytes[:text_bytes_trim_index]
        else:
            text_bytes_trimmed = text_bytes
        text = text_bytes_trimmed.decode('utf-8')

        block.append({'index': _index})
        block.append({'title': title})
        block.append({'text': text})

        block_chain.append(block)
        continue
    return block_chain


def deserialize_bin_text_param(blocks):
    return None  # TODO


def serialize_bin_param(_bin):
    block_chain = []
    for bin_block in _bin:
        block = []

        _id = struct.unpack('<L', bin_block[0])[0]

        text_bytes = bin_block[1]
        text_bytes_trim_index = text_bytes.find(b'\x00')
        text_bytes_trimmed = text_bytes[:text_bytes_trim_index]
        text = text_bytes_trimmed.decode('utf-8')

        index = struct.unpack('<L', bin_block[2])[0]
        unknown_1 = struct.unpack('<L', bin_block[3])[0]
        # unknown_2 = struct.unpack('<L', bin_block[4])[0]  # Empty zeros - no need to serialize
        unknown_3 = struct.unpack('<L', bin_block[5])[0]
        unknown_4 = struct.unpack('<L', bin_block[6])[0]
        unknown_5 = struct.unpack('<L', bin_block[7])[0]
        unknown_6 = struct.unpack('<L', bin_block[8])[0]
        unknown_7 = struct.unpack('<L', bin_block[9])[0]
        unknown_8 = struct.unpack('<L', bin_block[10])[0]
        # unknown_9 = struct.unpack('<L', bin_block[11])[0]  # Empty zeros - no need to serialize
        unknown_10 = struct.unpack('<L', bin_block[12])[0]

        block.append({'id': _id})
        block.append({'text': text})
        block.append({'index': index})
        block.append({'unknown_1' :unknown_1})
        # block.append({'unknown_2':unknown_2})  # Empty zeros - no need to serialize
        block.append({'unknown_3': unknown_3})
        block.append({'unknown_4': unknown_4})
        block.append({'unknown_5': unknown_5})
        block.append({'unknown_6': unknown_6})
        block.append({'unknown_7': unknown_7})
        block.append({'unknown_8': unknown_8})
        # block.append({'unknown_9': unknown_9})  # Empty zeros - no need to serialize
        block.append({'unknown_10': unknown_10})

        block_chain.append(block)
        continue
    return block_chain


def deserialize_bin_param(blocks):
    bin_param_data = bytearray(0x164 * len(blocks))

    block_data_list = []
    for block_index in range(len(blocks)):
        block = blocks[block_index]

        id_dict = block[0]
        text_dict = block[1]
        index_dict = block[2]
        unknown_01_dict = block[3]
        unknown_03_dict = block[4]
        unknown_04_dict = block[5]
        unknown_05_dict = block[6]
        unknown_06_dict = block[7]
        unknown_07_dict = block[8]
        unknown_08_dict = block[9]
        unknown_10_dict = block[10]

        block_data = bytearray(0x164)

        print(len(block_data))

        _id = id_dict['id']
        struct.pack_into('<L', block_data, 0x00, _id)  # id

        print(len(block_data))

        text = text_dict['text']
        text_data = bytes(text, encoding='utf-8')
        block_data[0x04:0x104] = text_data  # text

        print(len(block_data))

        index = index_dict['index']
        struct.pack_into('<L', block_data, 0x104, index)  # index

        unknown_01 = unknown_01_dict['unknown_1']
        struct.pack_into('<L', block_data, 0x108, unknown_01)  # unknown 1

        # Not used - Empty zeros
        # unknown_02 = unknown_02_dict['unknown_2']
        # struct.pack_into('<L', block_data, ????, unknown_02)  # unknown 2

        unknown_03 = unknown_03_dict['unknown_3']
        struct.pack_into('<L', block_data, 0x10E, unknown_03)  # unknown 2

        unknown_04 = unknown_04_dict['unknown_4']
        struct.pack_into('<L', block_data, 0x112, unknown_04)  # unknown 4

        unknown_05 = unknown_05_dict['unknown_5']
        struct.pack_into('<L', block_data, 0x116, unknown_05)  # unknown 5

        unknown_06 = unknown_06_dict['unknown_6']
        struct.pack_into('<L', block_data, 0x11A, unknown_06)  # unknown 6

        unknown_07 = unknown_07_dict['unknown_7']
        struct.pack_into('<L', block_data, 0x11E, unknown_07)  # unknown 7

        unknown_08 = unknown_08_dict['unknown_8']
        struct.pack_into('<L', block_data, 0x122, unknown_08)  # unknown 5

        # unknown_09 = unknown_09_dict['unknown_9']
        # Not used - Empty zeros (this is a bytearray)

        unknown_10 = unknown_10_dict['unknown_10']
        struct.pack_into('<L', block_data, 0x160, unknown_10)  # unknown 2

        block_data_list.append(block_data)
        continue

    previous_index = 0x00
    for block_data_index in range(len(block_data_list)):
        block_data = block_data_list[block_data_index]

        start_index = previous_index
        end_index = previous_index + (block_data_index + 1) * 164

        bin_param_data[start_index:end_index] = block_data

        previous_index = end_index
        continue

    print()
    return bin_param_data


def serialize_bin_text(_bin):
    block_chain = []
    for bin_block in _bin:
        block = []
        text_id_1 = struct.unpack('<L', bin_block[0])[0]
        text_id_2 = struct.unpack('<L', bin_block[1])[0]

        text_bytes = bin_block[2]
        text_bytes_trim_index = text_bytes.find(b'\x00')
        text_bytes_trimmed = text_bytes[:text_bytes_trim_index]
        text = text_bytes_trimmed.decode('utf-8')

        block.append({'text_id_1': text_id_1})
        block.append({'text_id_2': text_id_2})
        block.append({'text': text})

        block_chain.append(block)
        continue
    return block_chain


def deserialize_bin_text(blocks):
    return None  # TODO


def serialize_bin_list(_bin):
    block_chain = []
    for bin_block in _bin:
        block = []

        current_page_index = struct.unpack('<L', bin_block[0])[0]
        last_page_index = struct.unpack('<L', bin_block[1])[0]
        previous_page_index = struct.unpack('<L', bin_block[2])[0]

        next_page_index = struct.unpack('<L', bin_block[3])[0]
        if next_page_index == 4294967295:  # -1
            next_page_index = -1

        unknown_1 = struct.unpack('<L', bin_block[4])[0]  # Should we even put this in?
        if unknown_1 == 4294967295:  # -1
            unknown_1 = -1
        unknown_2 = struct.unpack('<L', bin_block[5])[0]  # Should we even put this in?
        unknown_3 = struct.unpack('<L', bin_block[6])[0]  # Should we even put this in?

        text_bytes = bin_block[8]
        text_bytes_trim_index = text_bytes.find(b'\x00')
        text_bytes_trimmed = text_bytes[:text_bytes_trim_index]
        text = text_bytes_trimmed.decode('utf-8')

        title_bytes = bin_block[7]
        title_bytes_trim_index = title_bytes.find(b'\x00')
        title_bytes_trimmed = title_bytes[:title_bytes_trim_index]
        title = title_bytes_trimmed.decode('utf-8')

        block.append({'current_page_index': current_page_index})
        block.append({'last_page_index': last_page_index})
        block.append({'previous_page_index': previous_page_index})
        block.append({'next_page_index': next_page_index})
        block.append({'current_page_index': current_page_index})
        block.append({'unknown_1': unknown_1})
        block.append({'unknown_2': unknown_2})
        block.append({'unknown_3': unknown_3})
        block.append({'title': title})
        block.append({'text': text})

        block_chain.append(block)
        continue
    return block_chain


def deserialize_bin_list(blocks):
    return None  # TODO


def serialize_bin_page(_bin):
    block_chain = []

    for bin_block in _bin:
        block = []

        _id = struct.unpack('<L', bin_block[0])

        lines = []
        for _bin_block_index in range(len(bin_block) - 1):
            sub_block = bin_block[_bin_block_index + 1]

            line_block = []

            text_bytes = sub_block[0]
            text_bytes_trim_index = text_bytes.find(b'\x00')
            if text_bytes_trim_index != -1:
                text_bytes_trimmed = text_bytes[:text_bytes_trim_index]
            else:
                text_bytes_trimmed = text_bytes
            try:
                text = text_bytes_trimmed.decode('utf-8')
            except UnicodeDecodeError:
                print('Failed to decode trimmed text... not decoding...')
                text = text_bytes_trimmed.hex()

            title_bytes = sub_block[1]
            title_bytes_trim_index = title_bytes.find(b'\x00')
            if title_bytes_trim_index != -1:
                title_bytes_trimmed = title_bytes[:title_bytes_trim_index]
            else:
                title_bytes_trimmed = title_bytes
            title = title_bytes_trimmed.decode('utf-8')

            line_block.append({'index': _bin_block_index})
            line_block.append({'text': text})
            line_block.append({'name': title})

            lines.append(line_block)
            continue

        block.append({'id': _id})
        block.append({'lines': lines})

        block_chain.append(block)
        continue
    return block_chain


def deserialize_bin_page(blocks):
    return None  # TODO
