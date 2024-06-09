# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Cadparam(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_params = []
        self.params = []
        i = 0
        while not self._io.is_eof():
            self._raw_params.append(self._io.read_bytes(356))
            _io__raw_params = KaitaiStream(BytesIO(self._raw_params[-1]))
            self.params.append(Cadparam.Param(_io__raw_params, self, self._root))
            i += 1


    class Param(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.index = self._io.read_u4le()
            self.text = (KaitaiStream.bytes_terminate(self._io.read_bytes(256), 0, False)).decode(u"UTF-8")
            self.sub_index = self._io.read_u4le()
            self.unknown_1 = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4be()
            self.unknown_3 = self._io.read_u4be()
            self.unknown_4 = self._io.read_u4be()
            self.unknown_5 = self._io.read_u4be()
            self.unknown_6 = self._io.read_u4be()
            self.unknown_7 = self._io.read_u4be()
            self.unknown_8 = self._io.read_u4be()
            self.unknown_9 = self._io.read_u4be()
            self.unknown_10 = self._io.read_u4be()
            self.unknown_11 = self._io.read_bytes(48)
            self.unknown_12 = self._io.read_u4le()



