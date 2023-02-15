# fw2odf
FinalWriter (Amiga word processor) to Open Document Format conversion

### Installation

    git clone https://github.com/hornc/fw2odf.git
    cd fw2odf
    pip install .

This will make the `fw2doc` command available.

    fw2doc sample.fw

Will produce an output file `sample.odf`.

### Current status

Very alpha, I am reverse engineering the Final Writer document format from scratch, based on some old personal documents I am trying to recover.

#### Implemented
 * IFF Chunk parsing
 * Text extraction (**all** text should be visible in the output doc)
 * Basic paragraph vs. span spacing
 * Font size from `ATTR`
 * Some Bold and Italics (based on font name)
 * [Symbol typeface](https://en.wikipedia.org/wiki/Symbol_(typeface)) to UTF-8 conversion.

#### TODO
 * Superscript (and subscript)
 * Proper endnotes (ideally with an option to convert to footnotes)
 * Title page and other section handling
 * Images?
 * Figure out and handle any differences between latin-1 / ISO-8859-1 and [Amiga-1251](https://www.iana.org/assignments/charset-reg/Amiga-1251) charset.
 * What else is encoded in `ATTR`?
 * Spacing and tabs etc? (`RULE`)
 * Heading styles
 * Refactor, structure more sensibly, and add more helpful debugging options and output

It is likely that the samples I am working from do not make use of all possible FinalWriter features.
A lot of my old documents use the Symbol typeface, for mathematical formulas _and_ for writing Classical and Modern Greek, which is why that is an early feature.

Recovering my own data is the main motivator behind this project, but I hope it may be more generally useful.

