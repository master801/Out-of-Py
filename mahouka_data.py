#!/usr/bin/env python3
# Created by Master on 4/2/2019

import json

import constants

from formats import imh_tuning_list_x_xx


def _serialize_file(_type: constants.Type, block: dict) -> str:
    return json.dumps(
        block,
        indent=2,
        ensure_ascii=False
    )


def serialize_bin(_type, _bin) -> str:
    return _serialize_file(
        _type,
        _serialize_bin_type(_type, _bin)
    )


def _serialize_bin_type(_type, _bin):
    if _type == constants.Type.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin
        return _serialize_bin_char_menu_param(_bin)
    elif _type == constants.Type.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin
        return _serialize_bin_cad_text_param(_bin)
    elif _type == constants.Type.TYPE_BIN_MAGIC_PARAM:  # MagicParam.bin
        return _serialize_bin_magic_param(_bin)
    elif _type == constants.Type.TYPE_BIN_TUTORIAL_LIST:  # TutorialList.bin
        return _serialize_bin_tutorial_list(_bin)
    elif _type == constants.Type.TYPE_BIN_TUNING_LIST:  # IMH_Tuning_List_X_XX.bin
        return _serialize_bin_tuning_list(_bin)
    else:
        raise Exception(f'Type \"{_type}\" not specified or is invalid!')


def _serialize_bin_char_menu_param(_bin):
    serialized = []

    for block in _bin.blocks:
        block_serialized = {}

        block_serialized.update({'index': block.index})
        block_serialized.update({'id': block.id})
        block_serialized.update({'title': block.title})
        block_serialized.update({'text_1': block.text_1})
        block_serialized.update({'unknown_1': block.unknown_1})
        block_serialized.update({'unknown_2': block.unknown_2})
        block_serialized.update({'text_2': block.text_2})
        block_serialized.update({'unknown_3': block.unknown_3})
        block_serialized.update({'unknown_4': block.unknown_4})
        block_serialized.update({'unknown_5': block.unknown_5})
        block_serialized.update({'unknown_6': block.unknown_6})
        block_serialized.update({'unknown_7': block.unknown_7})
        block_serialized.update({'unknown_8': block.unknown_8})
        block_serialized.update({'unknown_9': block.unknown_9})
        block_serialized.update({'unknown_10': block.unknown_10})
        block_serialized.update({'unknown_11': block.unknown_11})
        block_serialized.update({'unknown_12': block.unknown_12})
        block_serialized.update({'unknown_13': block.unknown_13})
        block_serialized.update({'unknown_14': block.unknown_14})
        # block_serialized.update({'unknown_15': block.unknown_15})  # Zeros padding?
        block_serialized.update({'unknown_16': block.unknown_16})
        block_serialized.update({'unknown_17': block.unknown_17})
        block_serialized.update({'unknown_18': block.unknown_18})
        block_serialized.update({'unknown_19': block.unknown_19})
        block_serialized.update({'unknown_20': block.unknown_20})
        block_serialized.update({'unknown_21': block.unknown_21})
        block_serialized.update({'unknown_22': block.unknown_22})
        block_serialized.update({'unknown_23': block.unknown_23})
        block_serialized.update({'unknown_24': block.unknown_24})
        # block_serialized.update({'unknown_25': block.unknown_25})  # Zeros padding?
        block_serialized.update({'unknown_26': block.unknown_26})
        # block_serialized.update({'unknown_27': block.unknown_27})  # Zeros padding?
        # block_serialized.update({'unknown_28': block.unknown_28})  # Zeros padding?
        block_serialized.update({'unknown_29': block.unknown_29})
        block_serialized.update({'unknown_30': block.unknown_30})
        block_serialized.update({'unknown_31': block.unknown_31})
        block_serialized.update({'unknown_32': block.unknown_32})
        block_serialized.update({'unknown_33': block.unknown_33})
        block_serialized.update({'unknown_34': block.unknown_34})
        block_serialized.update({'unknown_35': block.unknown_35})
        block_serialized.update({'unknown_36': block.unknown_36})
        block_serialized.update({'unknown_37': block.unknown_37})
        block_serialized.update({'unknown_38': block.unknown_38})

        serialized.append(block_serialized)
        continue

    return serialized


def _serialize_bin_cad_text_param(_bin):
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


def _serialize_bin_magic_param(_bin):
    serialized = []

    for entry in _bin.entries:
        entry_serialized = {}

        unknown_3 = entry.unknown_3
        unknown_25 = entry.unknown_25
        unknown_31 = entry.unknown_31
        unknown_34 = entry.unknown_34
        unknown_68 = entry.unknown_68
        unknown_72 = entry.unknown_72
        unknown_77 = entry.unknown_77

        if unknown_3 != b'\x00\x00\x00\x00\x00\x00\x00\x00':
            print('Unexpected data!')
            breakpoint()
            return
        elif unknown_25 != b'\x00\x00\x00\x00':
            print('Unexpected data!')
            breakpoint()
            return
        elif unknown_31 != b'\x00\x00\x00\x00':
            print('Unexpected data!')
            breakpoint()
            return
        elif unknown_34 != b'\x00\x00\x00\x00\x00\x00\x00\x00':
            print('Unexpected data!')
            breakpoint()
            return
        elif unknown_68 != b'\x00\x00\x00\x00':
            print('Unexpected data!')
            breakpoint()
            return
        elif unknown_72 != b'\x00\x00\x00\x00\x00\x00\x00\x00':
            print('Unexpected data!')
            breakpoint()
            return
        elif unknown_77 != b'\x00\x00\x00\x00\x00\x00\x00\x00':
            print('Unexpected data!')
            breakpoint()
            return

        entry_serialized.update({'index': entry.index})
        entry_serialized.update({'sub_index_1': entry.sub_index_1})
        entry_serialized.update({'sub_index_2': entry.sub_index_2})
        entry_serialized.update({'text': entry.text})
        entry_serialized.update({'title': entry.title})

        entry_serialized.update({'unknown_1': entry.unknown_1})
        entry_serialized.update({'unknown_2': entry.unknown_2})
        # entry_serialized.update({'unknown_3': entry.unknown_3})  # Zeros padding
        entry_serialized.update({'unknown_4': entry.unknown_4})
        entry_serialized.update({'unknown_5': entry.unknown_5})
        entry_serialized.update({'unknown_6': entry.unknown_6})
        entry_serialized.update({'unknown_7': entry.unknown_7})
        entry_serialized.update({'unknown_8': entry.unknown_8})
        entry_serialized.update({'unknown_9': entry.unknown_9})
        entry_serialized.update({'unknown_10': entry.unknown_10})
        entry_serialized.update({'unknown_11': entry.unknown_11})
        entry_serialized.update({'unknown_12': entry.unknown_12})
        entry_serialized.update({'unknown_13': entry.unknown_13})
        entry_serialized.update({'unknown_14': entry.unknown_14})
        entry_serialized.update({'unknown_15': entry.unknown_15})
        entry_serialized.update({'unknown_16': entry.unknown_16})
        entry_serialized.update({'unknown_17': entry.unknown_17})
        entry_serialized.update({'unknown_18': entry.unknown_18})
        entry_serialized.update({'unknown_19': entry.unknown_19})
        entry_serialized.update({'unknown_20': entry.unknown_20})
        entry_serialized.update({'unknown_21': entry.unknown_21})
        entry_serialized.update({'unknown_22': entry.unknown_22})
        entry_serialized.update({'unknown_23': entry.unknown_23})
        entry_serialized.update({'unknown_24': entry.unknown_24})
        # entry_serialized.update({'unknown_25': entry.unknown_25})  # Zeros padding
        entry_serialized.update({'unknown_26': entry.unknown_26})
        entry_serialized.update({'unknown_27': entry.unknown_27})
        entry_serialized.update({'unknown_28': entry.unknown_28})
        entry_serialized.update({'unknown_29': entry.unknown_29})
        entry_serialized.update({'unknown_30': entry.unknown_30})
        # entry_serialized.update({'unknown_31': entry.unknown_31})  # Zeros padding
        entry_serialized.update({'unknown_32': entry.unknown_32})
        entry_serialized.update({'unknown_33': entry.unknown_33})
        # entry_serialized.update({'unknown_34': entry.unknown_34})  # Zeros padding
        entry_serialized.update({'unknown_35': entry.unknown_35})
        entry_serialized.update({'unknown_36': entry.unknown_36})
        entry_serialized.update({'unknown_37': entry.unknown_37})
        entry_serialized.update({'unknown_38': entry.unknown_38})
        entry_serialized.update({'unknown_39': entry.unknown_39})
        entry_serialized.update({'unknown_40': entry.unknown_40})
        entry_serialized.update({'unknown_41': entry.unknown_41})
        entry_serialized.update({'unknown_42': entry.unknown_42})
        entry_serialized.update({'unknown_43': entry.unknown_43})
        entry_serialized.update({'unknown_44': entry.unknown_44})
        entry_serialized.update({'unknown_45': entry.unknown_45})
        entry_serialized.update({'unknown_46': entry.unknown_46})
        entry_serialized.update({'unknown_47': entry.unknown_47})
        entry_serialized.update({'unknown_48': entry.unknown_48})
        entry_serialized.update({'unknown_49': entry.unknown_49})
        entry_serialized.update({'unknown_50': entry.unknown_50})
        entry_serialized.update({'unknown_51': entry.unknown_51})
        entry_serialized.update({'unknown_52': entry.unknown_52})
        entry_serialized.update({'unknown_53': entry.unknown_53})
        entry_serialized.update({'unknown_54': entry.unknown_54})
        entry_serialized.update({'unknown_55': entry.unknown_55})
        entry_serialized.update({'unknown_56': entry.unknown_56})
        entry_serialized.update({'unknown_57': entry.unknown_57})
        entry_serialized.update({'unknown_58': entry.unknown_58})
        entry_serialized.update({'unknown_59': entry.unknown_59})
        entry_serialized.update({'unknown_60': entry.unknown_60})
        entry_serialized.update({'unknown_61': entry.unknown_61})
        entry_serialized.update({'unknown_62': entry.unknown_62})
        entry_serialized.update({'unknown_63': entry.unknown_63})
        entry_serialized.update({'unknown_64': entry.unknown_64})
        entry_serialized.update({'unknown_65': entry.unknown_65})
        entry_serialized.update({'unknown_66': entry.unknown_66})
        entry_serialized.update({'unknown_67': entry.unknown_67})
        # entry_serialized.update({'unknown_68': entry.unknown_68})  # Zeros padding
        entry_serialized.update({'unknown_69': entry.unknown_69})
        entry_serialized.update({'unknown_70': entry.unknown_70})
        entry_serialized.update({'unknown_71': entry.unknown_71})
        # entry_serialized.update({'unknown_72': entry.unknown_72})  # Zeros padding
        entry_serialized.update({'unknown_73': entry.unknown_73})
        entry_serialized.update({'unknown_74': entry.unknown_74})
        entry_serialized.update({'unknown_75': entry.unknown_75})
        entry_serialized.update({'unknown_76': entry.unknown_76})
        # entry_serialized.update({'unknown_77': entry.unknown_77})  # Zeros padding
        entry_serialized.update({'unknown_78': entry.unknown_78})
        entry_serialized.update({'unknown_79': entry.unknown_79})
        entry_serialized.update({'unknown_80': entry.unknown_80})
        entry_serialized.update({'unknown_81': entry.unknown_81})
        entry_serialized.update({'unknown_82': entry.unknown_82})

        serialized.append(entry_serialized)
        continue

    return serialized


def _serialize_bin_tutorial_list(_bin):
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


def _serialize_bin_tuning_list(_bin: imh_tuning_list_x_xx.ImhTuningListXXx):  # IMH_Tuning_List_X_XX.bin
    blocks = []

    for entry in _bin.entries:
        block_map = {}

        _id = entry.id
        entries = []

        for text_block in entry.text_blocks:
            text_block_map = {}

            title = text_block.title

            try:
                text = text_block.text.decode('utf-8', errors='backslashreplace')
            except UnicodeDecodeError:
                print('Failed to decode trimmed text... not decoding...')
                text = text_block.text.hex()
                pass

            text_block_map.update({'title': title})
            text_block_map.update({'text': text})
            entries.append(text_block_map)
            continue

        block_map.update({'id': _id})
        block_map.update({'entries': entries})

        blocks.append(block_map)
        continue

    return blocks
