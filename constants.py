#!/usr/bin/env python3
# Created by Master on 7/15/2019

import dataclasses
import enum
import re


MODE_DECODE = 'DECODE'
MODE_ENCODE = 'ENCODE'


@dataclasses.dataclass
class FileType:

    regex: re.Pattern

    decode_ext: str
    encode_ext: str

    pass


# noinspection PyTypeChecker
class Type(enum.Enum):

    TYPE_TXT_LUA = FileType(
        re.compile(r'evt\d{6}_Txt\.lua'),

        '.csv',
        '.lua'
    )

    TYPE_BIN_CHAR_MENU_PARAM = FileType(
        re.compile(r'CharMenuParam\.bin'),

        '.json',
        '.bin'
    )

    TYPE_BIN_CAD_PARAM = FileType(
        re.compile(r'CadParam\.bin'),

        '.csv',
        '.bin'
    )

    TYPE_BIN_CAD_TEXT_PARAM = FileType(
        re.compile(r'CadTextParam\.bin'),

        '.csv',
        '.bin'
    )

    TYPE_BIN_MAGIC_TEXT = FileType(
        re.compile(r'MagicText\.bin'),

        '.csv',
        '.bin'
    )

    TYPE_BIN_MAGIC_PARAM = FileType(
        re.compile(r'MagicParam\.bin'),

        '.json',
        '.bin'
    )

    TYPE_BIN_TUTORIAL_LIST = FileType(
        re.compile(r'TutorialList\.bin'),

        '.csv',
        '.bin'
    )

    TYPE_BIN_TUNING_LIST = FileType(
        re.compile(r'IMH_Tuning_List_[TJ]_\d{2}\.bin'),

        '.json',
        '.bin'
    )

    pass
