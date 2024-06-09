# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Magicparam(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_entries = []
        self.entries = []
        i = 0
        while not self._io.is_eof():
            self._raw_entries.append(self._io.read_bytes(508))
            _io__raw_entries = KaitaiStream(BytesIO(self._raw_entries[-1]))
            self.entries.append(Magicparam.Entry(_io__raw_entries, self, self._root))
            i += 1


    class Entry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.index = self._io.read_u4le()
            self.sub_index_1 = self._io.read_u4le()
            self.sub_index_2 = self._io.read_u4le()
            self.title = (KaitaiStream.bytes_terminate(self._io.read_bytes(64), 0, False)).decode(u"UTF-8")
            self.text = (KaitaiStream.bytes_terminate(self._io.read_bytes(64), 0, False)).decode(u"UTF-8")
            self.unknown_1 = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.unknown_3 = self._io.read_bytes(8)
            self.unknown_4 = self._io.read_u4be()
            self.unknown_5 = self._io.read_u4le()
            self.unknown_6 = self._io.read_u4be()
            self.unknown_7 = self._io.read_u4le()
            self.unknown_8 = self._io.read_u4le()
            self.unknown_9 = self._io.read_u4le()
            self.unknown_10 = self._io.read_u4le()
            self.unknown_11 = self._io.read_u4le()
            self.unknown_12 = self._io.read_u4le()
            self.unknown_13 = self._io.read_u4le()
            self.unknown_14 = self._io.read_u4le()
            self.unknown_15 = self._io.read_u4le()
            self.unknown_16 = self._io.read_u4le()
            self.unknown_17 = self._io.read_u4le()
            self.unknown_18 = self._io.read_u4le()
            self.unknown_19 = self._io.read_u4le()
            self.unknown_20 = self._io.read_u4le()
            self.unknown_21 = self._io.read_u4le()
            self.unknown_22 = self._io.read_u4le()
            self.unknown_23 = self._io.read_u4le()
            self.unknown_24 = self._io.read_u4le()
            self.unknown_25 = self._io.read_bytes(4)
            self.unknown_26 = self._io.read_u4be()
            self.unknown_27 = self._io.read_u4be()
            self.unknown_28 = self._io.read_u4le()
            self.unknown_29 = self._io.read_u4be()
            self.unknown_30 = self._io.read_u4be()
            self.unknown_31 = self._io.read_bytes(4)
            self.unknown_32 = self._io.read_u4le()
            self.unknown_33 = self._io.read_u4be()
            self.unknown_34 = self._io.read_bytes(8)
            self.unknown_35 = self._io.read_u4le()
            self.unknown_36 = self._io.read_u4le()
            self.unknown_37 = self._io.read_u4le()
            self.unknown_38 = self._io.read_u4le()
            self.unknown_39 = self._io.read_u4be()
            self.unknown_40 = self._io.read_u4be()
            self.unknown_41 = self._io.read_u4be()
            self.unknown_42 = self._io.read_u4be()
            self.unknown_43 = self._io.read_u4le()
            self.unknown_44 = self._io.read_u4be()
            self.unknown_45 = self._io.read_u4le()
            self.unknown_46 = self._io.read_u4be()
            self.unknown_47 = self._io.read_u4le()
            self.unknown_48 = self._io.read_u4be()
            self.unknown_49 = self._io.read_u4be()
            self.unknown_50 = self._io.read_u4le()
            self.unknown_51 = self._io.read_u4be()
            self.unknown_52 = self._io.read_u4be()
            self.unknown_53 = self._io.read_u4le()
            self.unknown_54 = self._io.read_u4le()
            self.unknown_55 = self._io.read_u4le()
            self.unknown_56 = self._io.read_u4le()
            self.unknown_57 = self._io.read_u4le()
            self.unknown_58 = self._io.read_u4le()
            self.unknown_59 = self._io.read_u4le()
            self.unknown_60 = self._io.read_u4le()
            self.unknown_61 = self._io.read_u4be()
            self.unknown_62 = self._io.read_u4le()
            self.unknown_63 = self._io.read_u4le()
            self.unknown_64 = self._io.read_u4le()
            self.unknown_65 = self._io.read_u4le()
            self.unknown_66 = self._io.read_u4le()
            self.unknown_67 = self._io.read_u4le()
            self.unknown_68 = self._io.read_bytes(4)
            self.unknown_69 = self._io.read_u4le()
            self.unknown_70 = self._io.read_u4le()
            self.unknown_71 = self._io.read_u4be()
            self.unknown_72 = self._io.read_bytes(8)
            self.unknown_73 = self._io.read_u4le()
            self.unknown_74 = self._io.read_u4le()
            self.unknown_75 = self._io.read_u4le()
            self.unknown_76 = self._io.read_u4le()
            self.unknown_77 = self._io.read_bytes(8)
            self.unknown_77_1 = self._io.read_bytes(8)
            self.unknown_77_2 = self._io.read_bytes(8)
            self.unknown_77_3 = self._io.read_bytes(8)
            self.unknown_78 = self._io.read_u4le()
            self.unknown_79 = self._io.read_u4le()
            self.unknown_80 = self._io.read_u4le()
            self.unknown_81 = self._io.read_u4le()
            self.unknown_82 = self._io.read_u4le()



