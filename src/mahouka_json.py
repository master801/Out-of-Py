#!/usr/bin/env python3

if not __debug__:  # Dev workspace
    from src import constants
else:
    import constants

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
    if _type == constants.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin TODO
        return serialize_bin_menu_param(_bin)
    elif _type == constants.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin
        return serialize_bin_cad_text_param(_bin)
    elif _type == constants.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        return serialize_bin_param(_bin)
    elif _type == constants.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        return serialize_bin_magic_text(_bin)
    elif _type == constants.TYPE_BIN_MAGIC_PARAM:
        return serialize_bin_magic_param(_bin)
    elif _type == constants.TYPE_BIN_TUTORIAL_LIST:  # TutorialList.bin
        return serialize_bin_list(_bin)
    elif _type == constants.TYPE_BIN_TUNING_LIST:  # IMH_Tuning_List_X_XX.bin
        return serialize_bin_tuning_list(_bin)


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


def serialize_bin_magic_text(_bin):
    serialized = []

    for block in _bin.blocks:
        block_serialized = {}

        block_serialized.update({'id_1': block.id_1})
        block_serialized.update({'id_2': block.id_2})
        block_serialized.update({'text': block.text})

        serialized.append(block_serialized)
        continue

    return serialized


def serialize_bin_magic_param(_bin):
    serialized = []

    for entry in _bin.entries:
        entry_serialized = {}

        index = entry.index
        sub_index_1 = entry.sub_index_1
        sub_index_2 = entry.sub_index_2
        text = entry.text
        title = entry.title
        unknown_1 = entry.unknown_1
        unknown_2 = entry.unknown_2
        unknown_3 = entry.unknown_3
        unknown_4 = entry.unknown_4
        unknown_5 = entry.unknown_5
        unknown_6 = entry.unknown_6
        unknown_7 = entry.unknown_7
        unknown_8 = entry.unknown_8
        unknown_9 = entry.unknown_9
        unknown_10 = entry.unknown_10
        unknown_11 = entry.unknown_11
        unknown_12 = entry.unknown_12
        unknown_13 = entry.unknown_13
        unknown_14 = entry.unknown_14
        unknown_15 = entry.unknown_15
        unknown_16 = entry.unknown_16
        unknown_17 = entry.unknown_17
        unknown_18 = entry.unknown_18
        unknown_19 = entry.unknown_19
        unknown_20 = entry.unknown_20
        unknown_21 = entry.unknown_21
        unknown_22 = entry.unknown_22
        unknown_23 = entry.unknown_23
        unknown_24 = entry.unknown_24
        unknown_25 = entry.unknown_25
        unknown_26 = entry.unknown_26
        unknown_27 = entry.unknown_27
        unknown_28 = entry.unknown_28
        unknown_29 = entry.unknown_29
        unknown_30 = entry.unknown_30
        unknown_31 = entry.unknown_31
        unknown_32 = entry.unknown_32
        unknown_33 = entry.unknown_33
        unknown_34 = entry.unknown_34
        unknown_35 = entry.unknown_35
        unknown_36 = entry.unknown_36
        unknown_37 = entry.unknown_37
        unknown_38 = entry.unknown_38
        unknown_39 = entry.unknown_39
        unknown_40 = entry.unknown_40
        unknown_41 = entry.unknown_41
        unknown_42 = entry.unknown_42
        unknown_43 = entry.unknown_43
        unknown_44 = entry.unknown_44
        unknown_45 = entry.unknown_45
        unknown_46 = entry.unknown_46
        unknown_47 = entry.unknown_47
        unknown_48 = entry.unknown_48
        unknown_49 = entry.unknown_49
        unknown_50 = entry.unknown_50
        unknown_51 = entry.unknown_51
        unknown_52 = entry.unknown_52
        unknown_53 = entry.unknown_53
        unknown_54 = entry.unknown_54
        unknown_55 = entry.unknown_55
        unknown_56 = entry.unknown_56
        unknown_57 = entry.unknown_57
        unknown_58 = entry.unknown_58
        unknown_59 = entry.unknown_59
        unknown_60 = entry.unknown_60
        unknown_61 = entry.unknown_61
        unknown_62 = entry.unknown_62
        unknown_63 = entry.unknown_63
        unknown_64 = entry.unknown_64
        unknown_65 = entry.unknown_65
        unknown_66 = entry.unknown_66
        unknown_67 = entry.unknown_67
        unknown_68 = entry.unknown_68
        unknown_69 = entry.unknown_69
        unknown_70 = entry.unknown_70
        unknown_71 = entry.unknown_71
        unknown_72 = entry.unknown_72
        unknown_73 = entry.unknown_73
        unknown_74 = entry.unknown_74
        unknown_75 = entry.unknown_75
        unknown_76 = entry.unknown_76
        unknown_77 = entry.unknown_77
        unknown_78 = entry.unknown_78
        unknown_79 = entry.unknown_79
        unknown_80 = entry.unknown_80
        unknown_81 = entry.unknown_81
        unknown_82 = entry.unknown_82

        if unknown_3 != b'\x00\x00\x00\x00\x00\x00\x00\x00':
            breakpoint()
        elif unknown_25 != b'\x00\x00\x00\x00':
            breakpoint()
        elif unknown_31 != b'\x00\x00\x00\x00':
            breakpoint()
        elif unknown_34 != b'\x00\x00\x00\x00\x00\x00\x00\x00':
            breakpoint()
        elif unknown_68 != b'\x00\x00\x00\x00':
            breakpoint()
        elif unknown_72 != b'\x00\x00\x00\x00\x00\x00\x00\x00':
            breakpoint()
        elif unknown_77 != b'\x00\x00\x00\x00\x00\x00\x00\x00':
            breakpoint()

        entry_serialized.update({'index': index})
        entry_serialized.update({'sub_index_1': sub_index_1})
        entry_serialized.update({'sub_index_2': sub_index_2})
        entry_serialized.update({'text': text})
        entry_serialized.update({'title': title})

        entry_serialized.update({'unknown_1': unknown_1})
        entry_serialized.update({'unknown_2': unknown_2})
        # entry_serialized.update({'unknown_3': unknown_3})  # Zeros padding
        entry_serialized.update({'unknown_4': unknown_4})
        entry_serialized.update({'unknown_5': unknown_5})
        entry_serialized.update({'unknown_6': unknown_6})
        entry_serialized.update({'unknown_7': unknown_7})
        entry_serialized.update({'unknown_8': unknown_8})
        entry_serialized.update({'unknown_9': unknown_9})
        entry_serialized.update({'unknown_10': unknown_10})
        entry_serialized.update({'unknown_11': unknown_11})
        entry_serialized.update({'unknown_12': unknown_12})
        entry_serialized.update({'unknown_13': unknown_13})
        entry_serialized.update({'unknown_14': unknown_14})
        entry_serialized.update({'unknown_15': unknown_15})
        entry_serialized.update({'unknown_16': unknown_16})
        entry_serialized.update({'unknown_17': unknown_17})
        entry_serialized.update({'unknown_18': unknown_18})
        entry_serialized.update({'unknown_19': unknown_19})
        entry_serialized.update({'unknown_20': unknown_20})
        entry_serialized.update({'unknown_21': unknown_21})
        entry_serialized.update({'unknown_22': unknown_22})
        entry_serialized.update({'unknown_23': unknown_23})
        entry_serialized.update({'unknown_24': unknown_24})
        # entry_serialized.update({'unknown_25': unknown_25})  # Zeros padding
        entry_serialized.update({'unknown_26': unknown_26})
        entry_serialized.update({'unknown_27': unknown_27})
        entry_serialized.update({'unknown_28': unknown_28})
        entry_serialized.update({'unknown_29': unknown_29})
        entry_serialized.update({'unknown_30': unknown_30})
        # entry_serialized.update({'unknown_31': unknown_31})  # Zeros padding
        entry_serialized.update({'unknown_32': unknown_32})
        entry_serialized.update({'unknown_33': unknown_33})
        # entry_serialized.update({'unknown_34': unknown_34})  # Zeros padding
        entry_serialized.update({'unknown_35': unknown_35})
        entry_serialized.update({'unknown_36': unknown_36})
        entry_serialized.update({'unknown_37': unknown_37})
        entry_serialized.update({'unknown_38': unknown_38})
        entry_serialized.update({'unknown_39': unknown_39})
        entry_serialized.update({'unknown_40': unknown_40})
        entry_serialized.update({'unknown_41': unknown_41})
        entry_serialized.update({'unknown_42': unknown_42})
        entry_serialized.update({'unknown_43': unknown_43})
        entry_serialized.update({'unknown_44': unknown_44})
        entry_serialized.update({'unknown_45': unknown_45})
        entry_serialized.update({'unknown_46': unknown_46})
        entry_serialized.update({'unknown_47': unknown_47})
        entry_serialized.update({'unknown_48': unknown_48})
        entry_serialized.update({'unknown_49': unknown_49})
        entry_serialized.update({'unknown_50': unknown_50})
        entry_serialized.update({'unknown_51': unknown_51})
        entry_serialized.update({'unknown_52': unknown_52})
        entry_serialized.update({'unknown_53': unknown_53})
        entry_serialized.update({'unknown_54': unknown_54})
        entry_serialized.update({'unknown_55': unknown_55})
        entry_serialized.update({'unknown_56': unknown_56})
        entry_serialized.update({'unknown_57': unknown_57})
        entry_serialized.update({'unknown_58': unknown_58})
        entry_serialized.update({'unknown_59': unknown_59})
        entry_serialized.update({'unknown_60': unknown_60})
        entry_serialized.update({'unknown_61': unknown_61})
        entry_serialized.update({'unknown_62': unknown_62})
        entry_serialized.update({'unknown_63': unknown_63})
        entry_serialized.update({'unknown_64': unknown_64})
        entry_serialized.update({'unknown_65': unknown_65})
        entry_serialized.update({'unknown_66': unknown_66})
        entry_serialized.update({'unknown_67': unknown_67})
        # entry_serialized.update({'unknown_68': unknown_68})  # Zeros padding
        entry_serialized.update({'unknown_69': unknown_69})
        entry_serialized.update({'unknown_70': unknown_70})
        entry_serialized.update({'unknown_71': unknown_71})
        # entry_serialized.update({'unknown_72': unknown_72})  # Zeros padding
        entry_serialized.update({'unknown_73': unknown_73})
        entry_serialized.update({'unknown_74': unknown_74})
        entry_serialized.update({'unknown_75': unknown_75})
        entry_serialized.update({'unknown_76': unknown_76})
        # entry_serialized.update({'unknown_77': unknown_77})  # Zeros padding
        entry_serialized.update({'unknown_78': unknown_78})
        entry_serialized.update({'unknown_79': unknown_79})
        entry_serialized.update({'unknown_80': unknown_80})
        entry_serialized.update({'unknown_81': unknown_81})
        entry_serialized.update({'unknown_82': unknown_82})

        serialized.append(entry_serialized)
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
