#!/usr/bin/env python3
# Created by Master on 5/7/2018


class BlockBuilder:
    """
    I got lazy and created a builder instead of using the luaparser library. It's less complex and in turn, less time consuming
    """

    block_name = None
    name = None
    text_lines = None
    voice = None

    def __init__(self, block_name, name, text_lines, voice):
        self.block_name = block_name
        self.name = name
        self.text_lines = text_lines
        self.voice = voice
        pass

    def to_source(self):
        all_text_lines = ''
        if self.text_lines is not None:
            if type(self.text_lines) is list:
                all_text_lines = f'\'{self.text_lines[0]}\''
                if len(self.text_lines) > 1:
                    for text_line_index in range(1, len(self.text_lines)):
                        text_line = self.text_lines[text_line_index]
                        all_text_lines += f'..\n\t\t\'{text_line}\''
                        continue
                    pass
                pass
            elif type(self.text_lines) is str:
                all_text_lines = f'\'{self.text_lines}\''
                pass
            pass
        pass

        name_chunk = ''
        txt_chunk = ''
        voice_chunk = ''

        if self.name is not None:
            name_chunk = f'\tname = \'{self.name}\',\r\n'
            pass

        if all_text_lines:
            txt_chunk = f'\ttxt = {all_text_lines},\r\n'
            pass

        if self.voice is not None:
            voice_chunk = f'\tvoice = \"{self.voice}\"\r\n'
            pass

        return self.block_name + ' = {\r\n' + name_chunk + txt_chunk + voice_chunk + '}\r\n\r\n'
