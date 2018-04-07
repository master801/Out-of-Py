import json
import struct


def serialize_lua(file_name, block):
    wrapped_block = {}
    wrapped_block.update({'type':'lua_text'})
    wrapped_block.update({'name':file_name})
    wrapped_block.update({'blocks':block})
    return json.dumps(wrapped_block, indent=2, ensure_ascii=False)


def serialize_bin(file_name, _type, _bin):
    blocks = serialize_bin_type(_type, _bin)

    wrapped_block = {}
    wrapped_block.update({'type':_type})
    wrapped_block.update({'name':file_name})
    wrapped_block.update({'blocks':blocks})
    return json.dumps(wrapped_block, indent=2, ensure_ascii=False)


def serialize_bin_type(_type, _bin):
    if _type == 'BattleParam':  # Not yet supported TODO
        return serialize_bin_battle_param(_bin)
    elif _type == 'MenuParam':  # CharMenuParam.bin TODO
        return serialize_bin_menu_param(_bin)
    elif _type == 'TextParam':  # CadTextParam.bin TODO
        return serialize_bin_text_param(_bin)
    elif _type == 'Param':  # CadParam.bin
        return serialize_bin_param(_bin)
    elif _type == 'Text':  # MagicText.bin
        return serialize_bin_text(_bin)
    elif _type == 'List':
        return serialize_bin_list(_bin)
    elif _type == 'Page':
        return serialize_bin_page(_bin)


def serialize_bin_battle_param(_bin):
    return None  # TODO


def serialize_bin_menu_param(_bin):
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

        block.append({'index':_index})
        block.append({'title':title})
        block.append({'text':text})

        block_chain.append(block)
        continue
    return block_chain


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

        block.append({'id':_id})
        block.append({'text':text})
        block.append({'index':index})
        block.append({'unknown_1':unknown_1})
        # block.append({'unknown_2':unknown_2})  # Empty zeros - no need to serialize
        block.append({'unknown_3':unknown_3})
        block.append({'unknown_4':unknown_4})
        block.append({'unknown_5':unknown_5})
        block.append({'unknown_6':unknown_6})
        block.append({'unknown_7':unknown_7})
        block.append({'unknown_8':unknown_8})
        # block.append({'unknown_9':unknown_9})  # Empty zeros - no need to serialize
        block.append({'unknown_10':unknown_10})

        block_chain.append(block)
        continue
    return block_chain


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
        block.append({'text':text})

        block_chain.append(block)
        continue
    return block_chain


def serialize_bin_list(_bin):
    block_chain = []
    for bin_block in _bin:
        block = []

        current_page_index = struct.unpack('<L', bin_block[0])[0]
        last_page_index = struct.unpack('<L', bin_block[1])[0]
        previous_page_index = struct.unpack('<L', bin_block[2])[0]

        next_page_index = struct.unpack('<L', bin_block[3])[0]
        if next_page_index == 4294967295:
            next_page_index = -1

        unknown_1 = struct.unpack('<L', bin_block[4])[0]  # Should we even put this in?
        if unknown_1 == 4294967295:
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

        block.append({'current_page_index':current_page_index})
        block.append({'last_page_index':last_page_index})
        block.append({'previous_page_index':previous_page_index})
        block.append({'next_page_index':next_page_index})
        block.append({'current_page_index':current_page_index})
        block.append({'unknown_1':unknown_1})
        block.append({'unknown_2':unknown_2})
        block.append({'unknown_3':unknown_3})
        block.append({'title':title})
        block.append({'text':text})

        block_chain.append(block)
        continue
    return block_chain


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
                import binascii
                text = text_bytes_trimmed.hex()

            title_bytes = sub_block[1]
            title_bytes_trim_index = title_bytes.find(b'\x00')
            if title_bytes_trim_index != -1:
                title_bytes_trimmed = title_bytes[:title_bytes_trim_index]
            else:
                title_bytes_trimmed = title_bytes
            title = title_bytes_trimmed.decode('utf-8')

            line_block.append({'index':_bin_block_index})
            line_block.append({'text':text})
            line_block.append({'name':title})

            lines.append(line_block)
            continue

        block.append({'id':_id})
        block.append({'lines':lines})

        block_chain.append(block)
        continue
    return block_chain
