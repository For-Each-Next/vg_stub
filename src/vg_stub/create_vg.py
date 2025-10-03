"""Generation wikitext of a video game stub."""

from types import EllipsisType
from typing import TYPE_CHECKING, Literal

from vg_stub.utils import comma_join, semi_comma_join, tuplize

if TYPE_CHECKING:
    from collections.abc import Sequence


class Name:
    """..."""

    def __init__(self, lang: str, name: str, tsl: str) -> None:
        self.lang = lang
        self.name = name
        self.tsl = self._transliterate(tsl)

    def _transliterate(self, text) -> str:
        """

        Args:
            text:

        Returns:

        """
        if text is None:
            return self.name
        return self.name

    @property
    def sortkey(self) -> str:
        """

        Returns:

        """
        return self.tsl.title()


class Titles:
    """..."""

    def __init__(
        self,
        zh: str | None = None,
        en: str | None = None,
        original_lang: str | None = None,
        original: str | None = None,
    ):
        self.zh = zh
        self.en = en
        self.original_lang = original_lang
        self.original = original

    @property
    def title(self) -> str:
        """

        Returns:

        """
        if self.zh:
            return self.zh
        if self.original:
            pass
        if self.en:
            return self.en

    @property
    def prose(self) -> str:
        pass


class Year:
    """..."""

    def __init__(
        self,
        year: int | None,
        status: Literal["released", "future", "cancelled"] | None = None,
    ) -> None:
        """

        Args:
            year:
            status:
        """
        self.year = year
        self.status = status

    @property
    def prose(self) -> str | None:
        """..."""
        match self.status:
            case None:
                return f"{self.year}年" if self.year else None
            case "released":
                return f"{self.year}年" if self.year else "已面世"
            case "future":
                return f"預定於{self.year}" if self.year else "尚未發行"
            case "cancelled":
                return "取消發行"


class Companies:
    """..."""

    def __init__(
        self,
        developer: str | Sequence[str] | None = None,
        publisher: str | Sequence[str] | EllipsisType | None = None,
    ) -> None:
        """

        Args:
            developer:
            publisher:

        Returns:

        """
        self.developer = tuplize(developer)
        self.publisher = tuplize(publisher)

    def prose(self) -> str | None:
        """

        Returns:

        """
        if (self.publisher is ...) and self.developer:
            return f"由{semi_comma_join(self.developer)}開發及發行"
        developer_prose = semi_comma_join(self.developer, end="開發")
        publisher_prose = semi_comma_join(self.publisher, end="發行")
        return comma_join([developer_prose, publisher_prose], start="由")


if __name__ == "__main__":
    companies = Companies("Square", ...)
    print(companies.prose())
