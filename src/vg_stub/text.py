"""Build wikitext of the article."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vg_stub._name import Name


def build_names(
    chinese: Name | str | None = None,
    foreign: Name | None = None,
) -> str:
    """Build the title and foreign annoations for the first sentence.

    Args:
        chinese: The Chinese name, or a string that will be bolded
            and wrapped in the Chinese book-mark pair.
        foreign: The foreign language name, e.g., the Japanese title.

    Returns:
        A Wikitext string.

    Examples:
        >>> from vg_stub._name import Name
        >>>
        >>> title = "DRAGON QUEST"
        >>> zh = Name("zh", "勇者鬥惡龍")
        >>> ja = Name(
        ...     "ja", "ドラゴンクエスト", translit="Doragon Kuesuto"
        ... )
        >>> en = Name("en", "Dragon Quest")
        >>>
        >>> build_names(title, ja)
        "《'''DRAGON QUEST'''》（{{efn|{{langx|ja|ドラゴンクエスト|translit=Doragon Kuesuto}}}}）"
        >>> build_names(zh, ja)
        "《'''勇者鬥惡龍'''》（{{efn|{{langx|ja|ドラゴンクエスト|translit=Doragon Kuesuto}}}}）"
        >>> build_names(None, ja)
        "《'''Doragon Kuesuto'''》（{{efn|{{langx|ja|ドラゴンクエスト}}}}）"
        >>>
        >>> build_names(title, en)
        "《'''DRAGON QUEST'''》"
        >>> build_names(zh, en)
        "《'''勇者鬥惡龍'''》（{{efn|{{langx|en|Dragon Quest|italic=yes}}}}）"
        >>> build_names(None, en)
        "《'''Dragon Quest'''》"
        >>>
        >>> build_names(title)
        "《'''DRAGON QUEST'''》"
        >>> build_names(zh)
        "《'''勇者鬥惡龍'''》"
        >>> build_names()
        "《'''{{subst:PAGENAME}}'''》"
    """  # noqa: E501, RUF002, W505
    # The main name will be bolded and wrapped in the book-mark pair.
    if chinese:
        main_name = chinese if isinstance(chinese, str) else chinese.name
    elif foreign:
        main_name = foreign.translit or foreign.name
    else:
        main_name = "{{subst:PAGENAME}}"
    # Foreign annotations.
    main_name_title_cased = main_name.title()
    if foreign is None or foreign.name.title() == main_name_title_cased:
        efn = ""
    elif foreign.translit.title() == main_name_title_cased:
        efn = foreign.efn(translit=False)
    else:
        efn = foreign.efn()
    # Combine two parts.
    if efn:
        efn = f"（{efn}）"  # noqa: RUF001
    return f"《'''{main_name}'''》{efn}"
