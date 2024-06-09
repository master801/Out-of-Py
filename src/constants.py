#!/usr/bin/env python3

MODE_DECODE = 'DECODE'
MODE_ENCODE = 'ENCODE'

TYPE_LUA = 'Lua'

TYPE_BIN_CHAR_MENU_PARAM = 'CharMenuParam'
TYPE_BIN_CAD_TEXT_PARAM = 'CadTextParam'
TYPE_BIN_CAD_PARAM = 'CadParam'
TYPE_BIN_MAGIC_TEXT = 'MagicText'
TYPE_BIN_MAGIC_PARAM = 'MagicParam'
TYPE_BIN_TUTORIAL_LIST = 'TutorialList'
TYPE_BIN_TUNING_LIST = 'TuningList'

# File Name, Type
TYPES_BIN = [
    [
        'CharMenuParam',
        TYPE_BIN_CHAR_MENU_PARAM
    ],
    [
        'CadTextParam',
        TYPE_BIN_CAD_TEXT_PARAM
    ],
    [
        'CadParam',
        TYPE_BIN_CAD_PARAM
    ],
    [
        'MagicText',
        TYPE_BIN_MAGIC_TEXT
    ],
    [
        'MagicParam',
        TYPE_BIN_MAGIC_PARAM
    ],
    [
        'TutorialList',
        TYPE_BIN_TUTORIAL_LIST
    ],
    [
        'IMH_Tuning_List_',
        TYPE_BIN_TUNING_LIST
    ]
]

LENGTH_BIN_CHAR_MENU_PARAM_CHUNK = 0x264
LENGTH_BIN_CAD_PARAM_CHUNK = 0x164
LENGTH_BIN_CAD_TEXT_PARAM = 0x144
LENGTH_BIN_MAGIC_TEXT_CHUNK = 0x208
LENGTH_BIN_MAGIC_PARAM_CHUNK = 0x1FC
LENGTH_BIN_TUTORIAL_LIST_CHUNK = 0x29C
