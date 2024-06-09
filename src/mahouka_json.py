#!/usr/bin/env python3

from src import constants
import json


def deserialize_file(file):
    deserialized_json = json.loads(file)

    _type = deserialized_json['type']
    file_path = deserialized_json['file_path']
    blocks = deserialized_json['blocks']

    deserialized = None
    if _type == constants.TYPE_LUA:
        deserialized = deserialize_lua(blocks)
    elif _type == constants.TYPE_BIN_CHAR_BATTLE_PARAM:  # Not yet supported TODO
        deserialized = deserialize_bin_char_battle_param(blocks)
    elif _type == constants.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin TODO
        deserialized = deserialize_bin_menu_param(blocks)
    elif _type == constants.TYPE_BIN_CHAR_MENU_PARAM:  # CadTextParam.bin TODO
        deserialized = deserialize_bin_char_menu_param(blocks)
    elif _type == constants.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        deserialized = deserialize_bin_cad_param(blocks)
    elif _type == constants.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        deserialized = deserialize_bin_magic_text(blocks)
    elif _type == constants.TYPE_BIN_TUTORIAL_LIST:
        deserialized = deserialize_bin_tutorial_list(blocks)
    elif _type == constants.TYPE_BIN_TUNING_LIST:
        deserialized = deserialize_bin_tuning_list(blocks)
    return [_type, file_path, deserialized]


def serialize_file(_type, input_dir_path, file_name, block):
    wrapped_block = {}
    wrapped_block.update({'type': _type})
    wrapped_block.update({'file_path': input_dir_path + "/" + file_name})
    wrapped_block.update({'block': block})
    return json.dumps(wrapped_block, indent=2, ensure_ascii=False)


def serialize_lua(input_dir_path, file_name, block):
    return serialize_file(constants.TYPE_LUA, input_dir_path, file_name, block)


def deserialize_lua(blocks):
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
    elif _type == constants.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin TODO
        return serialize_bin_text_param(_bin)
    elif _type == constants.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        return serialize_bin_param(_bin)
    elif _type == constants.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        return serialize_bin_text(_bin)
    elif _type == constants.TYPE_BIN_TUTORIAL_LIST:
        return serialize_bin_list(_bin)
    elif _type == constants.TYPE_BIN_TUNING_LIST:
        return serialize_bin_tuning_list(_bin)


def serialize_bin_battle_param(_bin):
    print()
    return None  # TODO


def deserialize_bin_char_battle_param(blocks):
    return None  # TODO


def serialize_bin_menu_param(_bin):
    print()
    return None  # TODO


def deserialize_bin_menu_param(blocks):
    return None  # TODO


def serialize_bin_text_param(_bin):
    print()
    return None # TODO


def deserialize_bin_char_menu_param(blocks):
    return None  # TODO


def serialize_bin_param(_bin):
    print()
    return None  # TODO


def deserialize_bin_cad_param(blocks):
    return None  # TODO


def serialize_bin_text(_bin):
    print()
    return None  # TODO


def deserialize_bin_magic_text(blocks):
    return None  # TODO


def serialize_bin_list(_bin):
    print()
    return None  # TODO


def deserialize_bin_tutorial_list(blocks):
    print()
    return None  # TODO


def serialize_bin_tuning_list(_bin):
    blocks = []
    for entry in _bin.entries:
        block_map = {}

        entry_index = entry.index
        entries = []

        for text_block in entry.text_blocks:
            text_block_map = {}
            text_block_map.update({'title': text_block.title})
            text_block_map.update({'text': text_block.text})
            entries.append(text_block_map)
            continue

        block_map.update({'entry_index': entry_index})
        block_map.update({'entries': entries})

        blocks.append(block_map)
        continue
    return blocks


def deserialize_bin_tuning_list(blocks):
    print()
    return None  # TODO
