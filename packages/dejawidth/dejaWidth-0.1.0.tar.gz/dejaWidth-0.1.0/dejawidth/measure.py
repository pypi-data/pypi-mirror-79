import io
import json
import pkg_resources
from typing import cast, Mapping, TextIO, Type


class Measure:
    """Measures the width of a string using a precalculated set of tables."""

    _default_cache = None

    def __init__(self, default_character_width: float,
                 char_to_width: Mapping[str, float],
                 pair_to_kern: Mapping[str, float]):
        """Initializer for PrecalculatedTextMeasurer.

        Args:
            default_character_width: the average width, in pixels, of a
                character in DejaVu Sans 110pt.
            char_to_width: a mapping between a character and it's width,
                in pixels, in DejaVu Sans 110pt.
            pair_to_kern: a mapping between pairs of characters and the kerning
                distance between them e.g. width("IJ") =>
                    (char_to_width["I"] + char_to_width["J"]
                    - pair_to_kern.get("IJ", 0))
        """
        self._default_character_width = default_character_width
        self._char_to_width = char_to_width
        self._pair_to_kern = pair_to_kern

    def width(self, text: str) -> float:
        """Returns the width, in pixels, of a string in DejaVu Sans 110pt."""
        width = 0
        for index, c in enumerate(text):
            width += self._char_to_width.get(c, self._default_character_width)
            width -= self._pair_to_kern.get(text[index:index + 2], 0)

        return width

    @staticmethod
    def from_json(f: TextIO) -> 'PrecalculatedTextMeasurer':
        """Return a PrecalculatedTextMeasurer given a JSON stream.

        See precalculate_text.py for details on the required format.
        """
        o = json.load(f)
        return Measure(o['mean-character-length'],
                                         o['character-lengths'],
                                         o['kerning-pairs'])

    @classmethod
    def default(cls) -> 'PrecalculatedTextMeasurer':
        """Returns a reasonable default PrecalculatedTextMeasurer."""
        if cls._default_cache is not None:
            return cls._default_cache

        if pkg_resources.resource_exists(__name__, 'default-widths.json.xz'):
            import lzma
            with pkg_resources.resource_stream(__name__,
                                               'default-widths.json.xz') as f:
                with lzma.open(f, "rt") as g:
                    cls._default_cache = Measure.from_json(
                        cast(TextIO, g))
                    return cls._default_cache
        elif pkg_resources.resource_exists(__name__, 'default-widths.json'):
            with pkg_resources.resource_stream(__name__,
                                               'default-widths.json') as f:
                cls._default_cache = Measure.from_json(
                    io.TextIOWrapper(f, encoding='utf-8'))
                return cls._default_cache
        else:
            raise ValueError('could not load default-widths.json')

