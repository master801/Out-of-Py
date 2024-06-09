# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Charmenuparam(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_blocks = []
        self.blocks = []
        i = 0
        while not self._io.is_eof():
            self._raw_blocks.append(self._io.read_bytes(612))
            _io__raw_blocks = KaitaiStream(BytesIO(self._raw_blocks[-1]))
            self.blocks.append(Charmenuparam.Block(_io__raw_blocks, self, self._root))
            i += 1


    class Block(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.index = self._io.read_u4le()
            self.id = self._io.read_u4le()
            self.title = (KaitaiStream.bytes_terminate(self._io.read_bytes(64), 0, False)).decode(u"UTF-8")
            self.text_1 = (KaitaiStream.bytes_terminate(self._io.read_bytes(256), 0, False)).decode(u"UTF-8")
            self.unknown_1 = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.text_2 = (KaitaiStream.bytes_terminate(self._io.read_bytes(128), 0, False)).decode(u"UTF-8")
            self.unknown_3 = self._io.read_u4le()
            self.unknown_4 = self._io.read_u4le()
            self.unknown_5 = self._io.read_u4le()
            self.unknown_6 = self._io.read_u4le()
            self.unknown_7 = self._io.read_u4le()
            self.unknown_8 = self._io.read_u4le()
            self.unknown_9 = self._io.read_u4le()
            self.unknown_10 = self._io.read_u4le()
            self.unknown_11 = self._io.read_u4le()
            self.unknown_12 = self._io.read_u4le()
            self.unknown_13 = self._io.read_u4le()
            self.unknown_14 = self._io.read_u4le()
            self.unknown_15 = self._io.read_bytes(4)
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
            self.unknown_26 = self._io.read_u4le()
            self.unknown_27 = self._io.read_bytes(8)
            self.unknown_28 = self._io.read_bytes(4)
            self.unknown_29 = self._io.read_u4le()
            self.unknown_30 = self._io.read_u4le()
            self.unknown_31 = self._io.read_u4le()
            self.unknown_32 = self._io.read_u4le()
            self.unknown_33 = self._io.read_u4le()
            self.unknown_34 = self._io.read_u4le()
            self.unknown_35 = self._io.read_u4le()
            self.unknown_36 = self._io.read_u4le()
            self.unknown_37 = self._io.read_u4le()
            self.unknown_38 = self._io.read_u4le()



