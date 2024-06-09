#!/usr/bin/env python3

import struct

if not __debug__:  # Dev workspace
    from src import mahouka_json, constants
    from src.builders import builders
else:
    import mahouka_json, constants
    from builders import builders


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


    import os
    if os.path.isfile(output_dir_path + '/' + deserialized_file_path):
        if not __debug__:
            os.remove(output_dir_path + '/' + deserialized_file_path)  # Remove file if in dev environment
        else:
            print('File {0} already exists! Not decoding...'.format(deserialized_file_path))  # Only show when in user environment
            return

    write_encoded(deserialized_file_path, output_dir_path, _type, encoded_file_data)

    print('Wrote deserialized file \"{0}\" to \"{1}\"\n'.format(input_file_path, output_dir_path + '/' + deserialized_file_path))


def encode_file_data(_type, deserialized):
    if _type == constants.TYPE_LUA:
        return encode_lua(deserialized)
    elif _type == constants.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin
        return encode_bin_char_menu_param(deserialized)
    elif _type == constants.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin
        return encode_bin_cad_text_param(deserialized)
    elif _type == constants.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        return encode_bin_cad_param(deserialized)
    elif _type == constants.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        return encode_bin_magic_text(deserialized)
    elif _type == constants.TYPE_BIN_MAGIC_PARAM:  # MagicParam.bin
        return encode_bin_magic_param(deserialized)
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

        start_offset = len(data)
        end_offset = len(encoded_bytes)

        data[start_offset:end_offset] = encoded_bytes
        continue

    return data


def encode_bin_char_menu_param(deserialized):
    encoded_data = bytearray(constants.LENGTH_BIN_CHAR_MENU_PARAM_CHUNK * len(deserialized))

    for entry_index in range(len(deserialized)):
        entry = deserialized[entry_index]

        encoded_entry_data = bytearray(constants.LENGTH_BIN_CHAR_MENU_PARAM_CHUNK)

        encoded_entry_data[0x00:0x04] = struct.pack('<L', entry['index'])
        encoded_entry_data[0x04:0x08] = struct.pack('<L', entry['id'])
        encoded_entry_data[0x08:0x48] = entry['title'].encode('utf-8').ljust(0x40, b'\x00')
        encoded_entry_data[0x48:0x148] = entry['text_1'].encode('utf-8').ljust(0x100, b'\x00')
        encoded_entry_data[0x148:0x14C] = struct.pack('<L', entry['unknown_1'])
        encoded_entry_data[0x14C:0x150] = struct.pack('<L', entry['unknown_2'])
        encoded_entry_data[0x150:0x1D0] = entry['text_2'].encode('utf-8').ljust(0x80, b'\x00')
        encoded_entry_data[0x1D0:0x1D4] = struct.pack('<L', entry['unknown_3'])
        encoded_entry_data[0x1D4:0x1D8] = struct.pack('<L', entry['unknown_4'])
        encoded_entry_data[0x1D8:0x1DC] = struct.pack('<L', entry['unknown_5'])
        encoded_entry_data[0x1DC:0x1E0] = struct.pack('<L', entry['unknown_6'])
        encoded_entry_data[0x1E0:0x1E4] = struct.pack('<L', entry['unknown_7'])
        encoded_entry_data[0x1E4:0x1E8] = struct.pack('<L', entry['unknown_8'])
        encoded_entry_data[0x1E8:0x1EC] = struct.pack('<L', entry['unknown_9'])
        encoded_entry_data[0x1EC:0x1F0] = struct.pack('<L', entry['unknown_10'])
        encoded_entry_data[0x1F0:0x1F4] = struct.pack('<L', entry['unknown_11'])
        encoded_entry_data[0x1F4:0x1F8] = struct.pack('<L', entry['unknown_12'])
        encoded_entry_data[0x1F8:0x1FC] = struct.pack('<L', entry['unknown_13'])
        encoded_entry_data[0x1FC:0x200] = struct.pack('<L', entry['unknown_14'])
        # encoded_entry_data[0x200:0x204] = entry['unknown_15']  # Zeros
        encoded_entry_data[0x204:0x208] = struct.pack('<L', entry['unknown_16'])
        encoded_entry_data[0x208:0x20C] = struct.pack('<L', entry['unknown_17'])
        encoded_entry_data[0x20C:0x210] = struct.pack('<L', entry['unknown_18'])
        encoded_entry_data[0x210:0x214] = struct.pack('<L', entry['unknown_19'])
        encoded_entry_data[0x214:0x218] = struct.pack('<L', entry['unknown_20'])
        encoded_entry_data[0x218:0x21C] = struct.pack('<L', entry['unknown_21'])
        encoded_entry_data[0x21C:0x220] = struct.pack('<L', entry['unknown_22'])
        encoded_entry_data[0x220:0x224] = struct.pack('<L', entry['unknown_23'])
        encoded_entry_data[0x224:0x228] = struct.pack('<L', entry['unknown_24'])
        # encoded_entry_data[0x228:0x22C] = entry['unknown_25']  # Zeros
        encoded_entry_data[0x22C:0x230] = struct.pack('<L', entry['unknown_26'])
        # encoded_entry_data[0x230:0x238] = entry['unknown_27']  # Zeros
        # encoded_entry_data[0x238:0x23C] = entry['unknown_28']  # Zeros
        encoded_entry_data[0x23C:0x240] = struct.pack('<L', entry['unknown_29'])
        encoded_entry_data[0x240:0x244] = struct.pack('<L', entry['unknown_30'])
        encoded_entry_data[0x244:0x248] = struct.pack('<L', entry['unknown_31'])
        encoded_entry_data[0x248:0x24C] = struct.pack('<L', entry['unknown_32'])
        encoded_entry_data[0x24C:0x250] = struct.pack('<L', entry['unknown_33'])
        encoded_entry_data[0x250:0x254] = struct.pack('<L', entry['unknown_34'])
        encoded_entry_data[0x254:0x258] = struct.pack('<L', entry['unknown_35'])
        encoded_entry_data[0x258:0x25C] = struct.pack('<L', entry['unknown_36'])
        encoded_entry_data[0x25C:0x260] = struct.pack('<L', entry['unknown_37'])
        encoded_entry_data[0x260:0x264] = struct.pack('<L', entry['unknown_38'])

        start_offset = constants.LENGTH_BIN_CHAR_MENU_PARAM_CHUNK * entry_index
        end_offset = constants.LENGTH_BIN_CHAR_MENU_PARAM_CHUNK * (entry_index + 1)

        encoded_data[start_offset:end_offset] = encoded_entry_data
        continue

    return encoded_data


def encode_bin_cad_text_param(deserialized):
    encoded_data = bytearray(constants.LENGTH_BIN_CAD_TEXT_PARAM * len(deserialized))

    for entry_index in range(len(deserialized)):
        entry = deserialized[entry_index]

        encoded_entry_data = bytearray(constants.LENGTH_BIN_CAD_TEXT_PARAM)

        encoded_entry_data[0x00:0x04] = struct.pack('<L', entry['index'])
        encoded_entry_data[0x04:0x44] = entry['title'].encode('utf-8').ljust(0x40, b'\x00')
        encoded_entry_data[0x44:0x144] = entry['text'].encode('utf-8').ljust(0x100, b'\x00')

        start_offset = constants.LENGTH_BIN_CAD_TEXT_PARAM * entry_index
        end_offset = constants.LENGTH_BIN_CAD_TEXT_PARAM * (entry_index + 1)

        encoded_data[start_offset:end_offset] = encoded_entry_data
        continue

    return encoded_data


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
        param_data_block[0x04:0x104] = text.encode('utf-8').ljust(0x100, b'\x00')
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

        start_offset = constants.LENGTH_BIN_CAD_PARAM_CHUNK * param_index
        end_offset = constants.LENGTH_BIN_CAD_PARAM_CHUNK * (param_index + 1)

        data_block[start_offset:end_offset] = param_data_block
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


def encode_bin_magic_param(deserialized):
    encoded_data = bytearray(constants.LENGTH_BIN_MAGIC_PARAM_CHUNK * len(deserialized))

    for entry_index in range(len(deserialized)):
        entry = deserialized[entry_index]

        entry_data = bytearray(constants.LENGTH_BIN_MAGIC_PARAM_CHUNK)

        entry_data[0x00:0x04] = struct.pack('<L', entry['index'])
        entry_data[0x04:0x08] = struct.pack('<L', entry['sub_index_1'])
        entry_data[0x08:0x0C] = struct.pack('<L', entry['sub_index_2'])
        entry_data[0x0C:0x4C] = entry['title'].encode('utf-8').ljust(0x40, b'\x00')
        entry_data[0x4C:0x8C] = entry['text'].encode('utf-8').ljust(0x40, b'\x00')
        entry_data[0x8C:0x90] = struct.pack('<L', entry['unknown_1'])
        entry_data[0x90:0x94] = struct.pack('<L', entry['unknown_2'])
        # entry_data[0x94:0x98] = entry['unknown_3']  # Zeroes
        entry_data[0x9C:0xA0] = struct.pack('>L', entry['unknown_4'])
        entry_data[0xA0:0xA4] = struct.pack('<L', entry['unknown_5'])
        entry_data[0xA4:0xA8] = struct.pack('>L', entry['unknown_6'])
        entry_data[0xA8:0xAC] = struct.pack('<L', entry['unknown_7'])
        entry_data[0xAC:0xB0] = struct.pack('<L', entry['unknown_8'])
        entry_data[0xB0:0xB4] = struct.pack('<L', entry['unknown_9'])
        entry_data[0xB4:0xB8] = struct.pack('<L', entry['unknown_10'])
        entry_data[0xB8:0xBC] = struct.pack('<L', entry['unknown_11'])
        entry_data[0xBC:0xC0] = struct.pack('<L', entry['unknown_12'])
        entry_data[0xC0:0xC4] = struct.pack('<L', entry['unknown_13'])
        entry_data[0xC4:0xC8] = struct.pack('<L', entry['unknown_14'])
        entry_data[0xC8:0xCC] = struct.pack('<L', entry['unknown_15'])
        entry_data[0xCC:0xD0] = struct.pack('<L', entry['unknown_16'])
        entry_data[0xD0:0xD4] = struct.pack('<L', entry['unknown_17'])
        entry_data[0xD4:0xD8] = struct.pack('<L', entry['unknown_18'])
        entry_data[0xD8:0xDC] = struct.pack('<L', entry['unknown_19'])
        entry_data[0xDC:0xE0] = struct.pack('<L', entry['unknown_20'])
        entry_data[0xE0:0xE4] = struct.pack('<L', entry['unknown_21'])
        entry_data[0xE4:0xE8] = struct.pack('<L', entry['unknown_22'])
        entry_data[0xE8:0xEC] = struct.pack('<L', entry['unknown_23'])
        entry_data[0xEC:0xF0] = struct.pack('<L', entry['unknown_24'])
        # entry_data[0xF0:0xF4] = entry['unknown_25']  # Zeroes
        entry_data[0xF4:0xF8] = struct.pack('>L', entry['unknown_26'])
        entry_data[0xF8:0xFC] = struct.pack('>L', entry['unknown_27'])
        entry_data[0xFC:0x100] = struct.pack('<L', entry['unknown_28'])
        entry_data[0x100:0x104] = struct.pack('>L', entry['unknown_29'])
        entry_data[0x104:0x108] = struct.pack('>L', entry['unknown_30'])
        # entry_data[0x108:0x10C] = entry['unknown_31']  # Zeroes
        entry_data[0x10C:0x110] = struct.pack('<L', entry['unknown_32'])
        entry_data[0x110:0x114] = struct.pack('>L', entry['unknown_33'])
        # entry_data[0x114:0x11C] = entry['unknown_34']  # Zeroes
        entry_data[0x11C:0x120] = struct.pack('<L', entry['unknown_35'])
        entry_data[0x120:0x124] = struct.pack('<L', entry['unknown_36'])
        entry_data[0x124:0x128] = struct.pack('<L', entry['unknown_37'])
        entry_data[0x128:0x12C] = struct.pack('<L', entry['unknown_38'])
        entry_data[0x12C:0x130] = struct.pack('>L', entry['unknown_39'])
        entry_data[0x130:0x134] = struct.pack('>L', entry['unknown_40'])
        entry_data[0x134:0x138] = struct.pack('>L', entry['unknown_41'])
        entry_data[0x138:0x13C] = struct.pack('>L', entry['unknown_42'])
        entry_data[0x13C:0x140] = struct.pack('<L', entry['unknown_43'])
        entry_data[0x140:0x144] = struct.pack('>L', entry['unknown_44'])
        entry_data[0x144:0x148] = struct.pack('<L', entry['unknown_45'])
        entry_data[0x148:0x14C] = struct.pack('>L', entry['unknown_46'])
        entry_data[0x14C:0x150] = struct.pack('<L', entry['unknown_47'])
        entry_data[0x150:0x154] = struct.pack('>L', entry['unknown_48'])
        entry_data[0x154:0x158] = struct.pack('>L', entry['unknown_49'])
        entry_data[0x158:0x15C] = struct.pack('<L', entry['unknown_50'])
        entry_data[0x15C:0x160] = struct.pack('>L', entry['unknown_51'])
        entry_data[0x160:0x164] = struct.pack('>L', entry['unknown_52'])
        entry_data[0x164:0x168] = struct.pack('<L', entry['unknown_53'])
        entry_data[0x168:0x16C] = struct.pack('<L', entry['unknown_54'])
        entry_data[0x16C:0x170] = struct.pack('<L', entry['unknown_55'])
        entry_data[0x170:0x174] = struct.pack('<L', entry['unknown_56'])
        entry_data[0x174:0x178] = struct.pack('<L', entry['unknown_57'])
        entry_data[0x178:0x17C] = struct.pack('<L', entry['unknown_58'])
        entry_data[0x17C:0x180] = struct.pack('<L', entry['unknown_59'])
        entry_data[0x180:0x184] = struct.pack('<L', entry['unknown_60'])
        entry_data[0x184:0x188] = struct.pack('>L', entry['unknown_61'])
        entry_data[0x188:0x18C] = struct.pack('<L', entry['unknown_62'])
        entry_data[0x18C:0x190] = struct.pack('<L', entry['unknown_63'])
        entry_data[0x190:0x194] = struct.pack('<L', entry['unknown_64'])
        entry_data[0x194:0x198] = struct.pack('<L', entry['unknown_65'])
        entry_data[0x198:0x19C] = struct.pack('<L', entry['unknown_66'])
        entry_data[0x19C:0x1A0] = struct.pack('<L', entry['unknown_67'])
        # entry_data[0x1A0:0x1A4] = entry['unknown_68']  # Zeroes
        entry_data[0x1A4:0x1A8] = struct.pack('<L', entry['unknown_69'])
        entry_data[0x1A8:0x1AC] = struct.pack('<L', entry['unknown_70'])
        entry_data[0x1AC:0x1B0] = struct.pack('>L', entry['unknown_71'])
        # entry_data[0x1B0:0x1B8] = entry['unknown_72']  # Zeroes
        entry_data[0x1B8:0x1BC] = struct.pack('<L', entry['unknown_73'])
        entry_data[0x1BC:0x1C0] = struct.pack('<L', entry['unknown_74'])
        entry_data[0x1C0:0x1C4] = struct.pack('<L', entry['unknown_75'])
        entry_data[0x1C4:0x1C8] = struct.pack('<L', entry['unknown_76'])
        # entry_data[0x1C8:0x1D0] = entry['unknown_77']  # Zeroes
        entry_data[0x1E8:0x1EC] = struct.pack('<L', entry['unknown_78'])
        entry_data[0x1EC:0x1F0] = struct.pack('<L', entry['unknown_79'])
        entry_data[0x1F0:0x1F4] = struct.pack('<L', entry['unknown_80'])
        entry_data[0x1F4:0x1F8] = struct.pack('<L', entry['unknown_81'])
        entry_data[0x1F8:0x1FC] = struct.pack('<L', entry['unknown_82'])

        start_offset = constants.LENGTH_BIN_MAGIC_PARAM_CHUNK * entry_index
        end_offset = constants.LENGTH_BIN_MAGIC_PARAM_CHUNK * (entry_index + 1)

        encoded_data[start_offset:end_offset] = entry_data
        continue

    return encoded_data


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
        _map = deserialized[map_index]
        sub_data_block = bytearray()

        _id = _map['id']
        entries = _map['entries']

        sub_data_block[0x00:0x04] = struct.pack('<L', _id)

        for entry_index in range(len(entries)):
            entry = entries[entry_index]

            text_data_block = bytearray(0x140)

            title = entry['title']
            text = entry['text']

            text_data = text.encode('utf-8').ljust(0x100, b'\x00')
            title_data = title.encode('utf-8').ljust(0x40, b'\x00')

            text_data_block[0x00:0x100] = text_data
            text_data_block[0x100:0x140] = title_data

            start_offset = 0x04 + (0x140 * entry_index)
            end_offset = 0x04 + (0x140 * (entry_index + 1))

            sub_data_block[start_offset:end_offset] = text_data_block
            continue

        start_index = (0x04 + (0x04 + (0x140 * len(entries)))) * map_index
        end_index = (0x04 + (0x140 * len(entries))) * (map_index + 1)
        data_block[start_index:end_index] = sub_data_block
        continue
    return data_block


def write_encoded(output_file_path, output_dir, _type, deserialized_file):
    output_file_dir = output_dir + '/' + output_file_path[:output_file_path.rindex('/')]

    import os
    if not os.path.isdir(output_file_dir):
        print('Directory {0} does not exist. Creating...'.format(output_file_dir))
        os.makedirs(output_file_dir, 0o775, True)
        pass

    output_file_complete_path = output_dir + '/' + output_file_path
    output_file = open(output_file_complete_path, mode='x+b')
    try:
        output_file.write(deserialized_file)
    finally:
        output_file.close()
