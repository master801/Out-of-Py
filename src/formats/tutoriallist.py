# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Tutoriallist(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.entries = self._io.read_u4le()
        self._raw_blocks = []
        self.blocks = []
        i = 0
        while not self._io.is_eof():
            self._raw_blocks.append(self._io.read_bytes(668))
            io = KaitaiStream(BytesIO(self._raw_blocks[-1]))
            self.blocks.append(self._root.Block(io, self, self._root))
            i += 1


    class Block(KaitaiStruct):
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



