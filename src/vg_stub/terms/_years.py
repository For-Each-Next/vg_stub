"""Define the GenreTerm classes."""

from __future__ import annotations

__all__ = ("YearTerm", "years")


from vg_stub._utils import hant
from vg_stub.terms._term import Term


class YearTerm(Term):
    """Represents a year term with MediaWiki formatting.

    YearTerm extends the base Term class to specifically handle
    year-related stuff. Year terms are defined in strings with the '年'
    (or '年代') suffix.

    The class includes methods for generating MediaWiki-formatted links,
    and category tags. The names of article and category should
    correspond to their actual page titles on the Chinese Wikipedia.

    Examples:
        >>> y1983 = YearTerm(
        ...     "1983年",
        ...     article="1983年電子遊戲界",
        ...     cat="1983年电子游戏",
        ... )
        >>> y1983.modifier
        '1983年'
        >>> y1983.name
        '1983年遊戲'
        >>> y1983.text()
        '1983年遊戲'
        >>> y1983.text(link=True)
        '[[1983年電子遊戲界|1983年遊戲]]'
        >>> y1983.cat_link()
        '[[Category:1983年电子游戏]]'
        >>> future = YearTerm("尚未發行的", cat="未来电子游戏")
        >>> future.text(link=True)
        '尚未發行的遊戲'
        >>> cancel = YearTerm("製作中止的", cat="製作中止的電子遊戲")
        >>> cancel.text(link=True)
        '製作中止的遊戲'
        >>> cancel.cat_link()
        '[[Category:製作中止的電子遊戲]]'
    """

    def __init__(
        self,
        year: str,
        *,
        article: str | None = None,
        cat: str | None = None,
    ) -> None:
        """Initialize a YearTerm instance.

        The genre name is automatically converted to Traditional Chinese
        and combined with '遊戲' to form the complete term name.

        Args:
            year: The year with a suffix of '年' or '年代'. Special
                staus can be used like '尚未發行的', '中止製作的', etc.
                Either Simplified or Traditional Chinese can be passed,
                though it will be automatically converted to Traditional
                Chinese.
            article: Optional main article title for the year. Used as
                the link target when generating wikilinks. If None, the
                term will not be linkable.
            cat: Optional main category name for the year. Used when
                generating category tags. If None, no category tag can
                be generated.

        Examples:
            >>> y83 = YearTerm("1983", article="1983年电子游戏")
            >>> y80s = YearTerm("1980年代", article="1980年代电子游戏")
            >>> future = YearTerm("尚未發行的")
            >>> cancelled = YearTerm("製作中止的")
        """
        super().__init__(
            hant(year),
            "遊戲",
            article=article,
            cat=cat,
        )


years = {
    "1983": YearTerm(
        "1983年",
        article="1983年電子遊戲界",
        cat="1983年电子游戏",
    ),
}
