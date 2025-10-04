"""Define the GenreTerm classes."""

from __future__ import annotations

__all__ = ("GenreTerm", "data")

from types import MappingProxyType

from vg_stub.termologies._term import Term
from vg_stub.utils import hant


class GenreTerm(Term):
    """Represents a video game genre term with MediaWiki formatting.

    GenreTerm extends the base Term class to specifically handle video
    game genre terminology.

    Genre names are defined in Traditional Chinese without the '遊戲'
    suffix. If a Simplified Chinese argument is provided, it will be
    automatically converted.

    The class includes methods for generating MediaWiki-formatted links,
    category tags, and stub templates. The names of article, category,
    and stub tag should correspond to their actual page titles on the
    Chinese Wikipedia.

    Examples:
        >>> rpg = GenreTerm(
        ...     "角色扮演",
        ...     article="電子角色扮演遊戲",
        ...     cat="角色扮演遊戲",
        ...     stub="rpg-videogame-stub",
        ... )
        >>> rpg.name
        '角色扮演遊戲'
        >>> rpg.text()
        '角色扮演遊戲'
        >>> rpg.text(link=True)
        '[[電子角色扮演遊戲|角色扮演遊戲]]'
        >>> rpg.cat_link()
        '[[Category:角色扮演遊戲]]'
        >>> rpg.stub_tag()
        '{{rpg-videogame-stub}}'
    """

    def __init__(
        self,
        genre: str,
        *,
        article: str | None = None,
        cat: str | None = None,
        stub: str | None = None,
    ) -> None:
        """Initialize a GenreTerm instance.

        The genre name is automatically converted to Traditional Chinese
        and combined with '遊戲' to form the complete term name.

        Args:
            genre: The genre name without the '遊戲' suffix. Can be in
                either Simplified or Traditional Chinese; it will be
                automatically converted to Traditional Chinese.
            article: Optional main article title for the genre. Used as
                the link target when generating wikilinks. If None, the
                term will not be linkable.
            cat: Optional main category name for the genre. Used when
                generating category tags. If None, no category tag can
                be generated.
            stub: Optional stub template name for the genre (e.g.,
                'rpg-videogame-stub'). Used when generating stub tags.
                If None, no stub tag can be generated.

        Examples:
            >>> action = GenreTerm("动作", article="動作遊戲")
            >>> strategy = GenreTerm(
            ...     "策略",
            ...     article="策略遊戲",
            ...     cat="策略遊戲",
            ...     stub="strategy-videogame-stub",
            ... )
        """
        super().__init__(
            hant(genre),
            "遊戲",
            article=article,
            cat=cat,
            stub=stub,
        )


data = MappingProxyType({
    "rpg": GenreTerm(
        "角色扮演",
        article="電子角色扮演遊戲",
        cat="電子角色扮演遊戲",
        stub="rpg-videogame-stub",
    ),
})
