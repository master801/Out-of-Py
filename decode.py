#!/usr/bin/env python3
# Created by Master on 4/3/2019

import os
import typing
import pathlib
import csv
import codecs

from luaparser import ast, astnodes

import constants
import mahouka_data
import models
from formats import cadparam, cadtextparam, charmenuparam, imh_tuning_list_x_xx, magictext, magicparam, tutoriallist

BIN_FROM_IO: dict[constants.Type: typing.Callable] = {
    constants.Type.TYPE_BIN_CHAR_MENU_PARAM: charmenuparam.Charmenuparam.from_io,  # CharMenuParam.bin
    constants.Type.TYPE_BIN_CAD_TEXT_PARAM: cadtextparam.Cadtextparam.from_io,  # CadTextParam.bin
    constants.Type.TYPE_BIN_CAD_PARAM: cadparam.Cadparam.from_io,  # CadParam.bin
    constants.Type.TYPE_BIN_MAGIC_TEXT: magictext.Magictext.from_io,  # MagicText.bin
    constants.Type.TYPE_BIN_MAGIC_PARAM: magicparam.Magicparam.from_io,  # MagicParam.bin
    constants.Type.TYPE_BIN_TUTORIAL_LIST: tutoriallist.Tutoriallist.from_io,  # TutorialList.bin
    constants.Type.TYPE_BIN_TUNING_LIST: imh_tuning_list_x_xx.ImhTuningListXXx.from_io  # IMH_Tuning_List_X_XX.bin
}


def decode_hex_utf8_string(encoded_hex_utf8_string: str) -> str:
    # Empty string
    if len(encoded_hex_utf8_string) < 1 or not encoded_hex_utf8_string.startswith('\\x'):
        return encoded_hex_utf8_string
    decoded_bytes = codecs.decode(encoded_hex_utf8_string, 'unicode_escape').encode('latin1')
    try:
        decoded = decoded_bytes.decode('utf-8', errors='backslashreplace')
    except UnicodeDecodeError:
        print('Failed to decode string!')
        print(f'String: \'{encoded_hex_utf8_string}\'')
        return encoded_hex_utf8_string
    return decoded


def decode_lua(io_lua: typing.TextIO) -> list[models.ModelEvtTxt]:
    print(f'Parsing file \"{io_lua.name}\"...')
    tree = ast.parse(io_lua.read())

    # DEBUG
    # print('DUMP LUA')
    # print(ast.to_pretty_str(tree))
    # print()

    texts: list[models.ModelEvtTxt] = []
    for node_assign in tree.body.body:
        if isinstance(node_assign, astnodes.Assign):
            node_name_id = node_assign.targets[0]
            if isinstance(node_name_id, astnodes.Name):
                _id = node_name_id.id
                pass
            else:
                print('Could not find id!')
                continue

            node_table = node_assign.values[0]
            if isinstance(node_table, astnodes.Table):
                if len(node_table.fields) == 3:
                    node_field_name = node_table.fields[0]
                    node_field_txt = node_table.fields[1]
                    node_field_voice = node_table.fields[2]

                    if isinstance(node_field_name.value, astnodes.String):
                        name = node_field_name.value.s
                        pass
                    else:
                        print('Unexpected type for \"name\"?!')
                        print(node_field_name.value.__class__)
                        continue

                    if isinstance(node_field_txt.value, astnodes.Concat):
                        text_build: list[str] = []

                        tmp = node_field_txt.value
                        while isinstance(tmp, astnodes.Concat):
                            if isinstance(tmp.left, astnodes.String):
                                text_build.append(tmp.left.s)
                                pass

                            if isinstance(tmp.right, astnodes.String):
                                text_build.append(tmp.right.s)
                                pass
                            else:
                                print('Unexpected node!')
                                break
                            tmp = tmp.left
                            continue
                        del tmp

                        if len(text_build) == 3:
                            text_build.insert(2, text_build.pop(0))
                            pass
                        elif len(text_build) == 1 or len(text_build) == 2:
                            # NOOP
                            pass
                        else:
                            print('Unexpected \"txt\" lines!')
                            continue

                        text = decode_hex_utf8_string(''.join(text_build))
                        del text_build
                        pass
                    elif isinstance(node_field_txt.value, astnodes.String):
                        text = node_field_txt.value.s
                        pass
                    else:
                        print(node_field_txt.value.__class__)
                        print('Unexpected type for \"txt\"?!')
                        continue

                    if isinstance(node_field_voice.value, astnodes.String):
                        voice = node_field_voice.value.s
                        pass
                    else:
                        print(node_field_voice.value.__class__)
                        print('Unexpected type for \"voice\"?!')
                        continue

                    texts.append(
                        models.ModelEvtTxt(
                            _id,
                            decode_hex_utf8_string(name),
                            decode_hex_utf8_string(text),
                            voice
                        )
                    )
                    pass
                elif len(node_table.fields) == 0:  # empty block
                    texts.append(
                        models.ModelEvtTxt(_id)
                    )
                    pass
                pass
            pass
        continue
    return texts


# noinspection PyUnboundLocalVariable,PyArgumentList
def decode_file(path_file: pathlib.Path, out_file: pathlib.Path, _type: constants.Type, overwrite: bool):
    if path_file.suffix == '.lua':
        with open(path_file, 'rt', encoding='utf-8') as io_lua:
            decoded_csv = decode_lua(io_lua)
            pass
        del io_lua
        pass
    else:
        with open(path_file, 'rb') as io_bin:
            parsed_bin_callable: typing.Callable[[typing.BinaryIO], any] = BIN_FROM_IO[_type]
            parsed_bin = parsed_bin_callable(io_bin)
            del parsed_bin_callable
            pass
        del io_bin

        if parsed_bin is None:
            print(f'Failed to parse bin file \"{path_file}\"!')
            return

        if _type.value.decode_ext == '.json':
            serialized_json = mahouka_data.serialize_bin(_type, parsed_bin)
            pass
        pass

    if out_file.exists() and overwrite:
        mode = 'w+'
        pass
    else:
        mode = 'x'
        pass

    if _type.value.decode_ext == '.csv':
        with open(out_file, mode=f'{mode}t', encoding='utf-8', newline='') as io_text_csv:
            csv_writer = csv.writer(io_text_csv, quoting=csv.QUOTE_NONNUMERIC)

            if _type == constants.Type.TYPE_TXT_LUA:
                csv_writer.writerow(['id', 'name', 'text', 'voice'])
                for text in decoded_csv:
                    csv_writer.writerow([text.id, text.name, text.text, text.voice])
                    continue
                pass
            elif _type == constants.Type.TYPE_BIN_CAD_PARAM and isinstance(parsed_bin, cadparam.Cadparam):
                csv_writer.writerow([
                    'index', 'sub_index', 'text', 'unknown_1', 'unknown_2', 'unknown_3', 'unknown_4',
                    'unknown_5', 'unknown_6', 'unknown_7', 'unknown_8', 'unknown_9', 'unknown_10', 'unknown_12'
                ])

                for i in parsed_bin.params:
                    csv_writer.writerow([
                        i.index, i.sub_index, i.text, i.unknown_1, i.unknown_2, i.unknown_3, i.unknown_4,
                        i.unknown_5, i.unknown_6, i.unknown_7, i.unknown_8, i.unknown_9, i.unknown_10, i.unknown_12
                    ])
                    continue
                del i
                pass
            elif _type == constants.Type.TYPE_BIN_CAD_TEXT_PARAM and isinstance(parsed_bin, cadtextparam.Cadtextparam):
                csv_writer.writerow(['index', 'text', 'title'])

                for i in parsed_bin.blocks:
                    csv_writer.writerow([i.index, i.text.decode('utf-8'), i.title.decode('utf-8')])
                    continue
                del i
                pass
            elif _type == constants.Type.TYPE_BIN_MAGIC_TEXT and isinstance(parsed_bin, magictext.Magictext):
                csv_writer.writerow(['id_1', 'id_2', 'text'])

                for i in parsed_bin.blocks:
                    csv_writer.writerow([i.id_1, i.id_2, i.text])
                    continue
                del i
                pass
            elif _type == constants.Type.TYPE_BIN_TUTORIAL_LIST and isinstance(parsed_bin, tutoriallist.Tutoriallist):
                csv_writer.writerow([
                    'current_page_index', 'last_page_index', 'previous_page_index', 'next_page_index',
                    'unknown_1', 'unknown_2', 'unknown_3', 'title', 'text'
                ])

                for i in parsed_bin.entries:
                    csv_writer.writerow([
                        i.current_page_index, i.last_page_index, i.previous_page_index, i.next_page_index,
                        i.unknown_1, i.unknown_2, i.unknown_3, i.title, i.text
                    ])
                    continue
                del i
                pass
            else:
                print(f'Could not parse csv file \"{path_file}\" for type \"{_type}\"!')
                breakpoint()
                pass

            del csv_writer
            pass
        del io_text_csv
        pass
    else:
        with open(out_file, mode=f'{mode}t', encoding='utf-8') as io_of:
            io_of.write(serialized_json)
            pass
        del mode
        del io_of
        pass
    print(f'Wrote file \"{out_file}\"{os.linesep}')
    return
