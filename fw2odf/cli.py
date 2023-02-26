import argparse

from pathlib import Path

from odf.text import P, Span, Tab

from fw2odf import __version__
from fw2odf.finalwriter import FW, Rule
from fw2odf.odf import OpenDocumentText
from fw2odf.symbol import from_symbol


DESC = """
Amiga FinalWriter to ODF conversion

"""


def main():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('source', help='Input FinalWriter file (.fw)', type=argparse.FileType('rb'))
    parser.add_argument('-d', '--debug', help='Debug', action='store_true')
    args = parser.parse_args()

    f = args.source
    outfile = Path(f.name).with_suffix('.odt') if f.name.endswith('.fw') else Path(f.name + '.odt')

    fwdoc = FW(f)

    if args.debug:
        print('DEBUG:', fwdoc.raw)
        print('DEBUG:', fwdoc.raw.getsize())

    textdoc = OpenDocumentText(source=f.name)

    p = P()
    for t in fwdoc.text:
        if isinstance(t, Rule):
            textdoc.text.addElement(p)
            p = P()
            continue
        current_style = fwdoc.style_from_attr(t.attr)
        textdoc.automaticstyles.addElement(current_style)
        if 'symbol' in str(current_style.getAttribute('name').lower()):
            if args.debug:
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
