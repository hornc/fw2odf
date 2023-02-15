"""
Amiga Final Writer to ODF conversion

"""
import struct

from chunk import Chunk
from odf.style import Style, TextProperties


CHARSET = 'iso-8859-1'  # close to Amiga-1251


class Chars:
    def __init__(self, chrs, attr):
        self.text = chrs
        self.attr = attr
     # ATTR:
     # 0: char count
     # 1: FDTA font
     # 2: ?
     # 3: fontsize
     # 4: ?
     # 5: emphasis? / style
     # 6: ?
     # 7: 17 superscript endnote  , 1 super? (or sub?)
     # 8: number of endnote if 7=17


class Rule:
    def __init__(self, rule=None):
        self.rule = rule


class Font:
    def __init__(self, raw):
        self.name = raw[:raw.find(0)].decode(CHARSET)


class FW:
    def __init__(self, f):
        self.raw = Chunk(f)
        self.index = []
        self.text = []
        self.fonts = []
        self.build_index()

    def read_tag(self):
        return self.raw.read(4).decode()

    def show_index(self):
        for v in self.index:
            print(f'{v[0]}: {hex(v[1])} {v[2]}')

    def build_index(self):
        tag = self.read_tag()
        assert tag == 'SWRT'  # FinalWriter IFF chunk id
        while 1:
            tag = self.read_tag()
            if not tag:
                break
            b = self.raw.read(4)
            size = int.from_bytes(b, 'big')
            pos = self.raw.tell()
            self.index.append((tag, pos, size))
            if tag not in ('ATTR', 'CHRS'):
                print(f'  size {tag} : {size}')
            if tag == 'ATTR':
                assert size == 22
                content = self.raw.read(size)
                attr = struct.unpack('>IHBBBBBBIIBB', content)
                print('ATTR', attr)
                tag = self.read_tag()  # read CHRS
                assert tag == 'CHRS', f'Expected CHRS, got "{tag}".'
                b = self.raw.read(4)
                size = int.from_bytes(b, 'big')
                assert attr[0] == size, f'Expected {attr[0]} == {size}'  # first attr is size of CHRS
                t = self.raw.read(size).decode(CHARSET)
                self.text.append(Chars(t, attr))
                print(t)
                size = 1 if size & 1 else 0
            elif tag == 'RULE':
                assert size == 24
                self.text.append(Rule())
            elif tag == 'FDTA':
                content = self.raw.read(size)
                self.fonts.append(Font(content))
                size = 0
            if size:
                if size != 1 and size & 1:
                    size = size + 1
                self.raw.seek(size, 1)
            #print('INDEX:', self.index)
        print('FONTS:', self.fonts)
        for i, f in enumerate(self.fonts):
            print(f'{len(self.fonts) - i - 1}: {f.name}')

        #self.show_index()
        #print(self.text)

    def style_from_attr(self, attr):
        """Creates an odf style from a FW ATTR."""
        fontsize = f'{attr[3]}pt'
        font = attr[1]
        fn = 'default'
        if font != 0:
            n = len(self.fonts) - font - 1
            fn = self.fonts[n].name
            print(f'FONT FOUND: {font} -- {fn}')
        #print('FONTSIZE', fontsize)
        fweight = 'normal'
        fstyle = 'normal'
        if 'Italic' in fn:
            fstyle = 'italic'
        elif 'Bold' in fn:
            fweight = 'bold'
        name = f'{fontsize}_{fn}'
        style = Style(name=name, family='text')
        style.addElement(TextProperties(fontsize=fontsize, fontweight=fweight, fontstyle=fstyle))
        return style
