import os

from datetime import datetime

from odf import dc, meta
from odf.office import Text, Meta
from odf.opendocument import OpenDocument

#from odf.element import Element
#from odf.namespaces import DCNS

from odf.style import Style, DefaultStyle, ParagraphProperties
from odf.text import P, Span, Tab

from fw2odf import __version__


FW2ODF = f'fw2odf/v{__version__}'
ODT_MIMETYPE = 'application/vnd.oasis.opendocument.text'
URL = 'https://github.com/hornc/fw2odf'


class OpenDocumentText(OpenDocument):
    def __init__(self, source):
        super().__init__(ODT_MIMETYPE)
        self.source = source
        self.meta = Meta()
        self.text = Text()
        self.body.addElement(self.text)
        self.add_metadata()
        self.add_styles()

    def add_metadata(self):
        now = datetime.now()
        then = datetime.fromtimestamp(os.path.getmtime(self.source))
        description = (
            f'Converted from Amiga FinalWriter document "{self.source}"\n'
            f'using {FW2ODF} ({URL}), at {now.strftime("%Y-%m-%d %H:%M:%S")}.'
        )
        self.meta.addElement(meta.Generator(text=FW2ODF))
        self.meta.addElement(meta.CreationDate(text=then.isoformat()))
        self.meta.addElement(dc.Date(text=now.isoformat()))
        self.meta.addElement(dc.Title(text=self.source))
        self.meta.addElement(meta.UserDefined(name='source', text=self.source))
        self.meta.addElement(dc.Description(text=description))
        # self.meta.addElement(Element(qname=(DCNS, 'source'), text=self.source, check_grammar=False))
        # self.meta.addElement(dc.Source(text=self.source))
        # self.meta.addElement(meta.InitialCreator(text='Original Author'))

    def add_styles(self):
        # Justified style
        justify = Style(name='justified', family='paragraph')
        justify.addElement(ParagraphProperties(
            attributes={'textalign': 'justify'}))
        # Default tab style
        deftabs = DefaultStyle(family='paragraph')
        deftabs.addElement(ParagraphProperties(
            attributes={'tabstopdistance': '0.5in'}))
        self.styles.addElement(deftabs)
        self.styles.addElement(justify)

    def _OpenDocument__replaceGenerator(self):
        """
        Prevent odfpy from overwriting our generator metadata.
        """
        pass
