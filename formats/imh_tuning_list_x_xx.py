# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class ImhTuningListXXx(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.entries = []
        i = 0
        while not self._io.is_eof():
            self.entries.append(ImhTuningListXXx.Entry(self._io, self, self._root))
            i += 1


    class Entry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u4le()
            self._raw_text_blocks = []
            self.text_blocks = []
            for i in range(self._root.entry_blocks_length):
                self._raw_text_blocks.append(self._io.read_bytes(320))
                _io__raw_text_blocks = KaitaiStream(BytesIO(self._raw_text_blocks[i]))
                self.text_blocks.append(ImhTuningListXXx.TextBlock(_io__raw_text_blocks, self, self._root))



    class TextBlock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.text = KaitaiStream.bytes_terminate(self._io.read_bytes(256), 0, False)
            self.title = (KaitaiStream.bytes_terminate(self._io.read_bytes(64), 0, False)).decode(u"UTF-8")


    @property
    def test_index_1(self):
        if hasattr(self, '_m_test_index_1'):
            return self._m_test_index_1

        _pos = self._io.pos()
        self._io.seek((320 * 24))
        self._m_test_index_1 = self._io.read_u4le()
        self._io.seek(_pos)
        return getattr(self, '_m_test_index_1', None)

    @property
    def test_index_2(self):
        if hasattr(self, '_m_test_index_2'):
            return self._m_test_index_2

        _pos = self._io.pos()
        self._io.seek(((320 * 24) + 4))
        self._m_test_index_2 = self._io.read_u4le()
        self._io.seek(_pos)
        return getattr(self, '_m_test_index_2', None)

    @property
    def is_j(self):
        if hasattr(self, '_m_is_j'):
            return self._m_is_j

        self._m_is_j =  ((self.test_index_1 == 0) and (self.test_index_2 == 2)) 
        return getattr(self, '_m_is_j', None)

    @property
    def entry_blocks_length(self):
        if hasattr(self, '_m_entry_blocks_length'):
            return self._m_entry_blocks_length

        self._m_entry_blocks_length = (24 if self.is_j else 20)
        return getattr(self, '_m_entry_blocks_length', None)


