#!/usr/bin/env python3
# Created by Master on 4/3/2019

import io
import struct
import os
import pathlib
import csv
import json

import models
import constants

LENGTH_BIN_CHAR_MENU_PARAM_CHUNK = 0x264
LENGTH_BIN_CAD_PARAM_CHUNK = 0x164
LENGTH_BIN_CAD_TEXT_PARAM = 0x144
LENGTH_BIN_MAGIC_TEXT_CHUNK = 0x208
LENGTH_BIN_MAGIC_PARAM_CHUNK = 0x1FC
LENGTH_BIN_TUTORIAL_LIST_CHUNK = 0x29C


def _encode_utf8_text_to_hex(utf8_text: str) -> str:
    return ''.join(f'\\x{i:02X}' for i in utf8_text.encode('utf-8'))


def _encode_lua(deserialized: list[models.ModelEvtTxt]) -> bytes:
    build = []
    for i in deserialized:
        build.append(f'{i.id} = {{\r\n')
        build.append(f'\tname = \'{_encode_utf8_text_to_hex(i.name)}\',\r\n')
        if len(i.text) != 0:
            build.append(f'\ttxt = ')
            nl_split = i.text.splitlines(keepends=True)
            if len(nl_split) == 1:
                build.append(f'\'{_encode_utf8_text_to_hex(nl_split[0])}\',\r\n')
                pass
            else:
                build.append(f'\'{_encode_utf8_text_to_hex(nl_split[0])}\'..\r\n')
                for j in range(len(nl_split) - 2):
                    build.append(f'\t\t\'{_encode_utf8_text_to_hex(nl_split[j+1])}\'..\r\n')
                    del j
                    continue
                build.append(f'\t\t\'{_encode_utf8_text_to_hex(nl_split[-1])}\',\r\n')
                pass
            del nl_split
            pass
        build.append(f'\tvoice = \"{i.voice}\"\r\n')
        build.append('}\r\n\r\n')
        del i
        continue
    return ''.join(build).encode('utf-8')


def _encode_bin_char_menu_param(deserialized) -> bytearray:
    encoded_data = bytearray(LENGTH_BIN_CHAR_MENU_PARAM_CHUNK * len(deserialized))

    for entry_index in range(len(deserialized)):
        entry = deserialized[entry_index]

        encoded_entry_data = bytearray(LENGTH_BIN_CHAR_MENU_PARAM_CHUNK)

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

        start_offset = LENGTH_BIN_CHAR_MENU_PARAM_CHUNK * entry_index
        end_offset = LENGTH_BIN_CHAR_MENU_PARAM_CHUNK * (entry_index + 1)

        encoded_data[start_offset:end_offset] = encoded_entry_data
        continue

    return encoded_data


def _encode_bin_cad_text_param(deserialized: list[list[int, str, str]]) -> bytes:
    with io.BytesIO() as io_encode:
        for i in deserialized:
            io_encode.write(struct.pack('<I', int(i[0])))
            io_encode.write(i[2].encode('utf-8').ljust(0x40, b'\x00'))
            io_encode.write(i[1].encode('utf-8').ljust(0x100, b'\x00'))
            continue
        del i
        data = io_encode.getvalue()
        pass
    del io_encode
    return data


def _encode_bin_cad_param(deserialized: list[list[int, int, str, int, int, int, int, int, int, int, int, int, int, int]]) -> bytes:
    with io.BytesIO() as io_encode:
        for i in deserialized:
            io_encode.write(struct.pack('<I', int(i[0])))
            io_encode.write(i[2].encode('utf-8').ljust(0x100, b'\x00'))
            io_encode.write(struct.pack('<I', int(i[1])))
            io_encode.write(struct.pack('<I', int(i[3])))
            io_encode.write(struct.pack('>I', int(i[4])))
            io_encode.write(struct.pack('>I', int(i[5])))
            io_encode.write(struct.pack('>I', int(i[6])))
            io_encode.write(struct.pack('>I', int(i[7])))
            io_encode.write(struct.pack('>I', int(i[8])))
            io_encode.write(struct.pack('>I', int(i[9])))
            io_encode.write(struct.pack('>I', int(i[10])))
            io_encode.write(struct.pack('>I', int(i[11])))
            io_encode.write(struct.pack('>I', int(i[12])))
            io_encode.write(b'\x00' * 48)
            io_encode.write(struct.pack('<I', int(i[13])))
            del i
            continue
        data = io_encode.getvalue()
        pass
    del io_encode
    return data


def _encode_bin_magic_text(deserialized: list[list[int, int, str]]) -> bytes:
    with io.BytesIO() as io_encode:
        for i in deserialized:
            io_encode.write(struct.pack('<I', int(i[0])))
            io_encode.write(struct.pack('<I', int(i[1])))
            io_encode.write(i[2].encode('utf-8').ljust(0x200, b'\x00'))
            continue
        del i
        data = io_encode.getvalue()
        pass
    del io_encode
    return data


def _encode_bin_magic_param(deserialized) -> bytearray:
    encoded_data = bytearray(LENGTH_BIN_MAGIC_PARAM_CHUNK * len(deserialized))

    for entry_index in range(len(deserialized)):
        entry = deserialized[entry_index]

        entry_data = bytearray(LENGTH_BIN_MAGIC_PARAM_CHUNK)

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

        start_offset = LENGTH_BIN_MAGIC_PARAM_CHUNK * entry_index
        end_offset = LENGTH_BIN_MAGIC_PARAM_CHUNK * (entry_index + 1)

        encoded_data[start_offset:end_offset] = entry_data
        continue

    return encoded_data


def _encode_bin_tutorial_list(deserialized: list[list[int, int, int, int, int, int, int, str, str]]) -> bytes:
    with io.BytesIO() as io_encode:
        io_encode.write(struct.pack('<I', len(deserialized)))  # length
        for i in deserialized:
            io_encode.write(struct.pack('<I', int(i[0])))  # current_page_index
            io_encode.write(struct.pack('<I', int(i[1])))  # last_page_index
            io_encode.write(struct.pack('<I', int(i[2])))  # previous_page_index
            io_encode.write(struct.pack('<I', int(i[3])))  # next_page_index

            io_encode.write(struct.pack('<I', int(i[4])))  # unknown_1
            io_encode.write(struct.pack('<I', int(i[5])))  # unknown_2
            io_encode.write(struct.pack('<I', int(i[6])))  # unknown_3

            io_encode.write(i[7].encode('utf-8').ljust(0x80, b'\x00'))  # title
            io_encode.write(i[8].encode('utf-8').ljust(0x200, b'\x00'))  # text
            continue
        del i
        data = io_encode.getvalue()
        pass
    del io_encode
    return data


def _encode_bin_tuning_list(deserialized: list[dict]) -> bytes:
    with io.BytesIO() as io_decode:
        for _map in deserialized:
            io_decode.write(struct.pack('<I', _map['id']))
            for entry in _map['entries']:
                text_raw: bytearray = entry['text'].encode('utf-8')
                title_raw: bytearray = entry['title'].encode('utf-8')

                while b'\\x' in text_raw:
                    i = text_raw.index(b'\\x')
                    j = text_raw[i:i+4]
                    k = j.decode('unicode_escape')
                    l = k.encode('utf-8')[1:]
                    text_raw = text_raw.replace(j, l)
                    del l
                    del k
                    del j
                    del i
                    continue

                io_decode.write(text_raw.ljust(0x100, b'\x00'))
                io_decode.write(title_raw.ljust(0x40, b'\x00'))
                continue
            continue
        data = io_decode.getvalue()
        pass
    del io_decode
    return data


def write_encoded(path_out: pathlib.Path, deserialized_file, overwrite: bool):
    if path_out.exists() and path_out.is_file():
        if overwrite:
            mode = 'w+'
            pass
        else:
            print(f'File \"{path_out}\" already exists! Cannot overwrite!')
            return
        pass
    else:
        mode = 'x'
        pass

    if not path_out.parent.exists():
        print(f'Directory \"{path_out.parent}\" does not exist. Creating...')
        path_out.parent.mkdir(parents=True)
        pass

    with open(path_out, mode=f'{mode}b') as io_out:
        io_out.write(deserialized_file)
        pass
    del mode
    del io_out
    return


def _encode_file_data(_type: constants.Type, deserialized) -> (bytearray | bytes):
    if _type == constants.Type.TYPE_TXT_LUA:
        return _encode_lua(deserialized)
    elif _type == constants.Type.TYPE_BIN_CHAR_MENU_PARAM:  # CharMenuParam.bin
        return _encode_bin_char_menu_param(deserialized)
    elif _type == constants.Type.TYPE_BIN_CAD_TEXT_PARAM:  # CadTextParam.bin
        return _encode_bin_cad_text_param(deserialized)
    elif _type == constants.Type.TYPE_BIN_CAD_PARAM:  # CadParam.bin
        return _encode_bin_cad_param(deserialized)
    elif _type == constants.Type.TYPE_BIN_MAGIC_TEXT:  # MagicText.bin
        return _encode_bin_magic_text(deserialized)
    elif _type == constants.Type.TYPE_BIN_MAGIC_PARAM:  # MagicParam.bin
        return _encode_bin_magic_param(deserialized)
    elif _type == constants.Type.TYPE_BIN_TUTORIAL_LIST:  # TutorialList.bin
        return _encode_bin_tutorial_list(deserialized)
    elif _type == constants.Type.TYPE_BIN_TUNING_LIST:  # IMH_Tuning_List_X_XX.bin
        return _encode_bin_tuning_list(deserialized)


def encode_file(path_file: pathlib.Path, output_dir_path: pathlib.Path, _type: constants.Type, overwrite: bool):
    print(f'Encoding file \"{path_file}\"...')

    fp_output: pathlib.Path = pathlib.Path(os.path.join(output_dir_path, path_file.stem))
    if (fp_output.exists() and fp_output.is_file()) and not overwrite:
        print(f'File \"{fp_output}\" already exists! Not encoding...{os.linesep}')
        return
    
    newline = '' if _type.value.decode_ext == '.csv' else None
    with open(path_file, mode='rt', encoding='utf-8', newline=newline) as io_file:
        if _type.value.decode_ext == '.csv':
            csv_reader = csv.reader(io_file, quoting=csv.QUOTE_NONNUMERIC)

            deserialized = []
            header = False
            for i in csv_reader:
                if not header:
                    header = True
                    continue
                if _type == constants.Type.TYPE_TXT_LUA:
                    deserialized.append(
                        models.ModelEvtTxt(i[0], i[1], i[2], i[3])
                    )
                    pass
                else:
                    deserialized.append(i)
                    pass
                del i
                continue
            del header

            del csv_reader
            pass
        else:
            deserialized = json.load(io_file)
            pass
        pass
    del io_file
    del newline

    encoded_file_data: bytearray = _encode_file_data(_type, deserialized)
    if encoded_file_data is None:
        print('Failed to deserialize file?!')
        breakpoint()
        return

    write_encoded(fp_output, encoded_file_data, overwrite)

    print(f'Wrote encoded file \"{path_file}\" to \"{fp_output}\"{os.linesep}')
    return
