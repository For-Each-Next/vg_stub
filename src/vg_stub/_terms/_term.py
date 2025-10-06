"""Utilities for building MediaWiki-style link for _terms."""

from __future__ import annotations

__all__ = ("Term",)

from vg_stub._utils import wikilink


class Term:
    """Represents a term with MediaWiki formatting capabilities.

    A Term combines a modifier and head to form complete term names
    and provides methods to generate MediaWiki-formatted links,
    categories, and stub tags.

    It tracks link usage to prevent overlinking (linking the same term
    multiple times).

    Examples:
        >>> rpg = Term(
        ...     "角色扮演",
        ...     "遊戲",
        ...     article="電子角色扮演遊戲",
        ...     cat="電子角色扮演遊戲",
        ...     stub="rpg-videogame-stub",
        ... )
        >>> rpg.name
        '角色扮演遊戲'
        >>> rpg.text(link=False)
        '角色扮演遊戲'
        >>> rpg.text(link=True)  # First time calling with linking
        '[[電子角色扮演遊戲|角色扮演遊戲]]'
        >>> rpg.text(link=True)  # Second calling, without overlinks
        '角色扮演遊戲'
        >>> rpg.cat_link()
        '[[Category:電子角色扮演遊戲]]'
        >>> rpg.cat_link("*")
        '[[Category:電子角色扮演遊戲|*]]'
        >>> rpg.stub_tag()
        '{{rpg-videogame-stub}}'
    """

    def __init__(
        self,
        modifier: str,
        head: str,
        *,
        article: str | None = None,
        cat: str | None = None,
        stub: str | None = None,
    ) -> None:
        """Initialize the instance.

        Args:
            modifier: The modifying part of the term name.
            head: The head (base) part of the term name.
            article: Optional target article title for linking.
            cat: Optional category name for categorization.
            stub: Optional stub template name.
        """
        self.modifier = modifier
        self.head = head
        self.article = article
        self.cat = cat
        self.stub = stub
        self._linked = False

    @property
    def name(self) -> str:
        """Return the name combining the parts of modifier and head.

        Returns:
            The string of full name.
        """
        return f"{self.modifier}{self.head}"

    def text(self, *, full: bool = True, link: bool = False) -> str:
        """Return a formatted representation of the term.

        Args:
            full: If True, then return the full name, i.e., the name
                combaining the parts of modifier and head.
                If False, return only the modifier part.
            link: If True, and an `article` is defined, return a
                MediaWiki link on the first call.
                On later calls, returns plain text to avoid overlinking.
                If False, return the plain text.
        Returns:
            The term as plain text or as a MediaWiki link, depending
            on arguments.

        Examples:
            >>> t = Term("角色扮演", "遊戲", article="電子角色扮演遊戲")
            >>> t.text(link=False)
            '角色扮演遊戲'
            >>> t.text(link=False, full=False)
            '角色扮演'
            >>> t.text(link=True)
            '[[電子角色扮演遊戲|角色扮演遊戲]]'
            >>> t.text(link=True)
            '角色扮演遊戲'
        """
        display = self.name if full else self.modifier
        if not link:
            return display
        if self.article is None:
            return display
        if self._linked:
            return display
        self._linked = True
        return wikilink(self.article, display)

    def cat_link(self, sort: str | None = None) -> str | None:
        """Return the MediaWiki category string for the term.

        Args:
            sort: Optional sort key for the category. If provided, the
                category entry will be formatted as
                ``[[Category:Name|Sort]]``.

        Returns:
            The MediaWiki category string, or None if `cat_name` is not
            set.

        Examples:
            >>> t = Term("動作", "遊戲", cat="動作遊戲")
            >>> t.cat_link()
            '[[Category:動作遊戲]]'
            >>> t.cat_link(sort="*")
            '[[Category:動作遊戲|*]]'
        """
        if self.cat is None:
            return None
        return wikilink(f"Category:{self.cat}", sort)

    def stub_tag(self) -> str | None:
        """Return the wikitext of the stub template for the term.

        Returns:
            A stub tag string of the form ``{{topic-name--stub}}``, or
            None if `stub_tag_name` is not set.

        Examples:
            >>> t = Term("角色扮演", "遊戲", stub="rpg-videogame-stub")
            >>> t.stub_tag()
            '{{rpg-videogame-stub}}'
        """
        if self.stub is None:
            return None
        return f"{{{{{self.stub}}}}}"

    def __str__(self) -> str:
        """Return the plain term name as its string representation.

        Returns:
            A string. Equivalent to accessing `self.name`.

        Example:
            >>> str(Term("角色扮演", "遊戲"))
            '角色扮演遊戲'
        """
        return self.name
