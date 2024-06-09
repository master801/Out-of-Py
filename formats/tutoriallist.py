# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Tutoriallist(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.length = self._io.read_u4le()
        self._raw_entries = []
        self.entries = []
        i = 0
        while not self._io.is_eof():
            self._raw_entries.append(self._io.read_bytes(668))
            _io__raw_entries = KaitaiStream(BytesIO(self._raw_entries[-1]))
            self.entries.append(Tutoriallist.Entry(_io__raw_entries, self, self._root))
            i += 1


    class Entry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.current_page_index = self._io.read_u4le()
            self.last_page_index = self._io.read_u4le()
            self.previous_page_index = self._io.read_u4le()
            self.next_page_index = self._io.read_u4le()
            self.unknown_1 = self._io.read_u4le()
            self.unknown_2 = self._io.read_u4le()
            self.unknown_3 = self._io.read_u4le()
            self.title = (KaitaiStream.bytes_terminate(self._io.read_bytes(128), 0, False)).decode(u"UTF-8")
            self.text = (KaitaiStream.bytes_terminate(self._io.read_bytes(512), 0, False)).decode(u"UTF-8")



