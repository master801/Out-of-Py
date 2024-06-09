#!/usr/bin/env python3

from src import constants

import json


def deserialize_file_container(file):
    deserialized_json = json.loads(file)

    _type = deserialized_json['type']
    file_path = deserialized_json['file_path']
    block = deserialized_json['block']

    return [_type, file_path, block]


def serialize_file(_type, input_dir_path, file_name, block):
    wrapped_block = {}
    wrapped_block.update({'type': _type})
    wrapped_block.update({'file_path': input_dir_path + "/" + file_name})
    wrapped_block.update({'block': block})
    return json.dumps(wrapped_block, indent=2, ensure_ascii=False)


def serialize_lua(input_dir_path, file_name, block):
    return serialize_file(constants.TYPE_LUA, input_dir_path, file_name, block)


def deserialize_lua(block):
    print()  # TODO
    return None


def serialize_bin(input_dir_path, file_name, _type, _bin):
    blocks = serialize_bin_type(_type, _bin)
    return serialize_file(_type, input_dir_path, file_name, blocks)


def serialize_bin_type(_type, _bin):
    if _type == constants.TYPE_BIN_CHAR_BATTLE_PARAM:  # Not yet supported TODO
        return serialize_bin_battle_param(_bin)
    elif _type == constants.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin TODO
        return serialize_bin_menu_param(_bin)
    elif _type == constants.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin
        return serialize_bin_cad_text_param(_bin)
    elif _type == constants.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        return serialize_bin_param(_bin)
    elif _type == constants.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        return serialize_bin_text(_bin)
    elif _type == constants.TYPE_BIN_TUTORIAL_LIST:  # TutorialList.bin
        return serialize_bin_list(_bin)
    elif _type == constants.TYPE_BIN_TUNING_LIST:  # IMH_Tuning_List_X_XX.bin
        return serialize_bin_tuning_list(_bin)


def serialize_bin_battle_param(_bin):
    print()  # TODO
    return None  # TODO


def deserialize_bin_char_battle_param(block):
    print()  # TODO
    return None  # TODO


def serialize_bin_menu_param(_bin):
    print()  # TODO
    return None  # TODO


def deserialize_bin_menu_param(block):
    # print()  # TODO
    return None  # TODO


def serialize_bin_cad_text_param(_bin):
    serialized = []

    for block in _bin.blocks:
        block_serialized = {}

        index = block.index

        try:
            title = block.title.decode('utf-8')
        except UnicodeDecodeError:
            title = block.title.hex()

        try:
            text = block.text.decode('utf-8')
        except UnicodeDecodeError:
            text = block.text.hex()

        block_serialized.update({'index': index})
        block_serialized.update({'title': title})
        block_serialized.update({'text': text})

        serialized.append(block_serialized)
        continue

    return serialized


def deserialize_bin_char_menu_param(blocks):
    print()  # TODO
    return None  # TODO


def serialize_bin_param(_bin):
    serialized = {}

    params = []
    for param in _bin.params:
        param_serialized = {}

        param_serialized.update({'index': param.index})
        param_serialized.update({'sub_index': param.sub_index})
        param_serialized.update({'text': param.text})
        param_serialized.update({'unknown_1': param.unknown_1})
        param_serialized.update({'unknown_2': param.unknown_2})
        param_serialized.update({'unknown_3': param.unknown_3})
        param_serialized.update({'unknown_4': param.unknown_4})
        param_serialized.update({'unknown_5': param.unknown_5})
        param_serialized.update({'unknown_6': param.unknown_6})
        param_serialized.update({'unknown_7': param.unknown_7})
        param_serialized.update({'unknown_8': param.unknown_8})
        param_serialized.update({'unknown_9': param.unknown_9})
        param_serialized.update({'unknown_10': param.unknown_10})
        # param_serialized.update({'unknown_11': param.unknown_11})
        param_serialized.update({'unknown_12': param.unknown_12})

        params.append(param_serialized)
        continue

    serialized.update({'params': params})
    return serialized


def deserialize_bin_cad_param(block):
    for param in block.params:
        continue

    print()  # TODO
    return None  # TODO


def serialize_bin_text(_bin):
    serialized = []

    for block in _bin.blocks:
        block_serialized = {}

        block_serialized.update({'id_1': block.id_1})
        block_serialized.update({'id_2': block.id_2})
        block_serialized.update({'text': block.text})

        serialized.append(block_serialized)
        continue

    return serialized


def deserialize_bin_magic_text(block):
    print()  # TODO
    return None  # TODO


def serialize_bin_list(_bin):
    serialized = {}

    entries = []
    for entry in _bin.entries:
        mapping = {}

        mapping.update({'current_page_index': entry.current_page_index})
        mapping.update({'last_page_index': entry.last_page_index})
        mapping.update({'previous_page_index': entry.previous_page_index})
        mapping.update({'next_page_index': entry.next_page_index})
        mapping.update({'unknown_1': entry.unknown_1})
        mapping.update({'unknown_2': entry.unknown_2})
        mapping.update({'unknown_3': entry.unknown_3})
        mapping.update({'title': entry.title})
        mapping.update({'text': entry.text})

        entries.append(mapping)
        continue

    serialized.update({'length': _bin.length})
    serialized.update({'entries': entries})
    return serialized


def deserialize_bin_tutorial_list(block):
    print()
    return None  # TODO


def serialize_bin_tuning_list(_bin):  # IMH_Tuning_List_X_XX.bin
    blocks = []

    for entry in _bin.entries:
        block_map = {}

        _id = entry.id
        entries = []

        for text_block in entry.text_blocks:
            text_block_map = {}

            title = text_block.title

            try:
                text = text_block.text.decode('utf-8')
            except UnicodeDecodeError:
                print('Failed to decode trimmed text... not decoding...')
                text = text_block.text.hex()

            text_block_map.update({'title': title})
            text_block_map.update({'text': text})
            entries.append(text_block_map)
            continue

        block_map.update({'id': _id})
        block_map.update({'entries': entries})

        blocks.append(block_map)
        continue

    return blocks


def deserialize_bin_tuning_list(block):
    print()
    return None  # TODO
