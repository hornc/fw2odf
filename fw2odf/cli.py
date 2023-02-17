import argparse
import sys

from pathlib import Path

from odf.opendocument import OpenDocumentText
from odf.style import Style, DefaultStyle, ParagraphProperties
from odf.text import P, Span, Tab

from fw2odf.finalwriter import FW, Rule
from fw2odf.symbol import from_symbol


"""
Amiga Final Writer to ODF conversion

"""


def main():
    fname = sys.argv[1]
    outfile = Path(fname).with_suffix('.odt') if fname.endswith('.fw') else Path(fname + '.odt')

    with open(fname, 'rb') as f:
        fwdoc = FW(f) 

    print('DEBUG:', fwdoc.raw)
    print('DEBUG:', fwdoc.raw.getsize())

    textdoc = OpenDocumentText()
    # Justified style
    justify = Style(name='justified', family='paragraph')
    justify.addElement(ParagraphProperties(
        attributes={'textalign': 'justify'}))
    # Default tab style
    deftabs = DefaultStyle(family='paragraph')
    deftabs.addElement(ParagraphProperties(
        attributes={'tabstopdistance': '0.5in'}))
    textdoc.styles.addElement(deftabs)
    textdoc.styles.addElement(justify)
    p = P()
    for t in fwdoc.text:
        if isinstance(t, Rule):
            textdoc.text.addElement(p)
            p = P()
            continue
        current_style = fwdoc.style_from_attr(t.attr)
        textdoc.automaticstyles.addElement(current_style)
        if 'symbol' in str(current_style.getAttribute('name').lower()):
            print(f'SYMBOL got "{t.text}" --> "{from_symbol(t.text)}"')
            text = Span(stylename=current_style, text=from_symbol(t.text))
        elif t.text == '\t':
            text = Tab()
        else:
            text = Span(stylename=current_style, text=t.text)
        p.addElement(text)

    textdoc.save(outfile.name)


if __name__ == '__main__':
    main()
