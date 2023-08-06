from os import path

from rinoh.font import Typeface
from rinoh.font.style import REGULAR, ITALIC, BOLD
from rinoh.font.opentype import OpenTypeFont


__all__ = ['typeface']


# font files were downloaded from https://fontlibrary.org/en/font/carlito


def otf(style):
    filename = 'Carlito-{}.ttf'.format(style)
    return path.join(path.dirname(__file__), filename)


typeface = Typeface('Carlito',
                    OpenTypeFont(otf('Regular'), weight=REGULAR),
                    OpenTypeFont(otf('Italic'), weight=REGULAR, slant=ITALIC),
                    OpenTypeFont(otf('Bold'), weight=BOLD),
                    OpenTypeFont(otf('BoldItalic'), weight=BOLD, slant=ITALIC))
