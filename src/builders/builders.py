#!/usr/bin/env python3
import types


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
                all_text_lines = '\'{0}\''.format(self.text_lines[0])
                if len(self.text_lines) > 1:
                    for text_line_index in range(1, len(self.text_lines)):
                        text_line = self.text_lines[text_line_index]
                        all_text_lines += ('..\n' + '\t\t' + '\'{0}\''.format(text_line))
                        continue
            elif type(self.text_lines) is str:
                all_text_lines = '\'{0}\''.format(self.text_lines)

        name_chunk = ''
        txt_chunk = ''
        voice_chunk = ''

        if self.name is not None:
            name_chunk = '\tname = \'{0}\',\r\n'.format(self.name)

        if all_text_lines:
            txt_chunk = '\ttxt = {0},\r\n'.format(all_text_lines)

        if self.voice is not None:
            voice_chunk = '\tvoice = \"{0}\"\r\n'.format(self.voice)

        return self.block_name + ' = {\r\n' + name_chunk + txt_chunk + voice_chunk + '}\r\n\r\n'
