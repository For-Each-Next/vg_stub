"""A class representing and formatting multilingual names."""

from __future__ import annotations

__all__ = ("Name",)

import mwparserfromhell

from vg_stub.utils import pinyin, romaji

ITALIC_LANGS = frozenset(("en",))


class Name:
    """Container for multilingual game title names.

    Provides language-aware transliteration, sort keys, and generation
    of Wikipedia {{efn}} notes with nested {{langx}}. Currently supports
    English, Chinese, and Japanese. English names are italicized when
    formatted; Chinese names do not produce footnotes.

    Examples:
        >>> zh = Name("zh", "時空幻境")
        >>> zh.name
        '時空幻境'
        >>> zh.sortkey
        'Shi Kong Huan Jing'
        >>> en = Name("en", "Tales of Phantasia", lit="幻想传奇")
        >>> en.sortkey
        'Tales Of Phantasia'
        >>> en.efn
        '{{efn|{{langx|en|Tales of Phantasia|lit=幻想传奇|italic=yes}}}}'
        >>> ja = Name("ja", "テイルズ オブ ファンタジア")
        >>> ja.name
        'テイルズ オブ ファンタジア'
        >>> ja.translit
        'Teiruzu obu Fantajia'
        >>> ja.sortkey
        'Teiruzu Obu Fantajia'
        >>> ja2 = Name(
        ...     "ja", "キミのいる未来へ", translit="Kimi no Iru Mirai e"
        ... )
        >>> ja2.sortkey
        'Kimi Noiru Mirai E'
        >>> ja2.efn
        '{{efn|{{langx|ja|キミのいる未来へ|translit=Kimi no Iru Mirai e}}}}'
    """  # noqa: W505

    def __init__(
        self,
        lang: str,
        name: str,
        translit: str | None = None,
        sortkey: str | None = None,
        lit: str | None = None,
    ) -> None:
        """Initialize a Name with language-aware processing.

        Args:
            lang: ISO 639-1 language code (e.g., 'en', 'zh', 'ja').
            name: The name in its original script.
            translit: Optional explicit transliteration. If None is
                given, it is auto-generated for Chinese (Hanyu Pinyin)
                and Japanese (modified Hepburn).
            sortkey: Optional explicit sort key. If None, it is
                auto-generated according to language-specific rules.
            lit: Optional literal translation of the name, used for
                Wikitext {{efn}} notes appended to the main name.
        """
        self.lang = lang
        self.name = name
        self.translit = self._translit(translit)
        self.sortkey = self._sortkey(sortkey)
        self.lit = lit

    def _translit(self, value: str | None) -> str:
        """Return the transliteration for this name.

        If a value is provided, it is returned unchanged. Otherwise, a
        language-specific transliteration is generated:
            - Chinese (zh): Hanyu Pinyin with tone marks.
            - Japanese (ja): Modified Hepburn romanization.
            - Other languages: The original name is returned.

        Args:
            value: Optional explicit-transliteration value.

        Returns:
            Transliterated version of the name.
        """
        if value:
            return value
        if self.lang == "zh":
            return pinyin(self.name)
        if self.lang == "ja":
            return romaji(self.name)
        return self.name

    def _sortkey(self, value: str | None) -> str:
        """Return the sort key used for alphabetical ordering.

        If an explicit sort key is provided, it is returned unchanged.
        Otherwise, a language-specific key is generated:
        - Chinese (zh): Toneless Pinyin with each syllable capitalized.
        - Japanese (ja): Title-cased romanization.
        - Other languages: Title-cased transliteration.

        Args:
            value: Explicit sort key value, or None to auto-generate.

        Returns:
            Normalized string suitable for alphabetical sorting.
        """
        if value:
            return value
        if self.lang == "zh":
            return pinyin(self.name, tone=False)
        if self.lang == "ja":
            return romaji(self.name).title()
        return self.translit.title()

    @property
    def italic(self) -> bool:
        """Whether this name should be italicized when formatted.

        Returns:
            True if the language requires italics; otherwise False.
        """
        return self.lang in ITALIC_LANGS

    @property
    def efn(self) -> str | None:
        """Return a Wikipedia efn template embedding {{langx}}.

        Generates the {{efn}} footnote containing a nested {{langx}}.
        Returns None for Chinese names (no footnote is required).

        Returns:
            The efn template string, or None if no footnote is needed.
        """
        if self.lang == "zh":
            return None
        langx = mwparserfromhell.nodes.Template("langx")
        langx.add(1, self.lang, showkey=False)
        langx.add(2, self.name, showkey=False)
        if self.translit != self.name:
            langx.add("translit", self.translit)
        if self.lit:
            langx.add("lit", self.lit)
        if self.italic:
            langx.add("italic", "yes")
        return f"{{{{efn|{langx}}}}}"
