import argparse

from pathlib import Path

from odf import dc, meta
from odf.element import Element
from odf.namespaces import DCNS
from odf.office import Meta
from odf.opendocument import OpenDocumentText
from odf.style import Style, DefaultStyle, ParagraphProperties
from odf.text import P, Span, Tab

from fw2odf.finalwriter import FW, Rule
from fw2odf.symbol import from_symbol
from fw2odf import __version__


DESC = """
Amiga FinalWriter to ODF conversion

"""


FW2ODF = f'fw2odf/v{__version__}'


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

    textdoc = OpenDocumentText()
    # Prevent odfpy from overwriting our generator metadata
    # TODO: make our own OpenDocument class...
    textdoc._OpenDocument__replaceGenerator = lambda: None

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
            if args.debug:
                print(f'SYMBOL got "{t.text}" --> "{from_symbol(t.text)}"')
            text = Span(stylename=current_style, text=from_symbol(t.text))
        elif t.text == '\t':
            text = Tab()
        else:
            text = Span(stylename=current_style, text=t.text)
        p.addElement(text)

    textdoc.meta = Meta()
    textdoc.meta.addElement(meta.Generator(text=FW2ODF))
    textdoc.meta.addElement(dc.Date(text='now'))
    textdoc.meta.addElement(meta.UserDefined(name='source', text=f.name))
    #textdoc.meta.addElement(Element(qname=(DCNS, 'source'), text=f.name, check_grammar=False))
    #textdoc.meta.addElement(dc.Source(text=f.name))
    #textdoc.meta.addElement(meta.InitialCreator(text='Original Author'))
    textdoc.meta.addElement(meta.CreationDate(text='then'))
    print('DEBUG:', textdoc.meta)
    textdoc.save(outfile.name)


if __name__ == '__main__':
    main()
