"""Generate Wikipedia-style citations for web pages."""

from __future__ import annotations

__all__ = ("cite_web", "ref")

import datetime
from urllib.parse import urlparse

import mwparserfromhell.nodes
import requests
from bs4 import BeautifulSoup
from dateutil import parser


def get_soup(url: str) -> BeautifulSoup | None:
    """Fetch and parse HTML content from a URL.

    Args:
        url: The web page URL to fetch.

    Returns:
        Parsed HTML content of the given web page.

    Raises:
        RuntimeError: If no content is found at the given URL.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    text = response.text
    if not text.strip():
        msg = f"no content found at the given URL: {url}"
        raise RuntimeError(msg)
    return BeautifulSoup(text, "html.parser")


def get_meta_content(soup: BeautifulSoup, *names: str) -> str | None:
    """Return the first meta tag's content that matches given names.

    Args:
        soup: Parsed HTML document.
        *names: One or more meta-tag names to search for.

    Returns:
        The first matching meta content, or None if not found.
    """
    for name in names:
        for attr in ("name", "property", "itemprop"):
            tag = soup.find("meta", attrs={attr: name})
            if tag and tag.get("content"):
                return tag["content"].strip()
    return None


def extract_title(soup: BeautifulSoup) -> str | None:
    """Extract the page title from HTML or metadata.

    Args:
        soup: Parsed HTML document.

    Returns:
        str: The extracted page title, or None if missing.
    """
    title = get_meta_content(soup, "og:title", "dc.title", "title")
    if title:
        return title
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    if h1 := soup.find("h1"):
        return h1.get_text(strip=True)
    return None


def get_domain(url: str) -> str:
    """Extract the domain name from a URL.

    Args:
        url: The URL to extract the domain from.

    Returns:
        The domain name without of 'www.' prefix.
    """
    parsed = urlparse(url)
    return parsed.netloc.removeprefix("www.")


def extract_website(soup: BeautifulSoup, url: str) -> str:
    """Extract the website name from HTML metadata or URL.

    Args:
        soup: Parsed HTML document.
        url: The original web page URL.

    Returns:
        str: The detected website name or domain.
    """
    site_name = get_meta_content(soup, "og:site_name", "application-name")
    if site_name:
        return site_name
    return get_domain(url)


def extract_author(soup: BeautifulSoup) -> str | None:
    """Extract the author's name from the HTML metadata.

    Args:
        soup: Parsed HTML document.

    Returns:
        str: The author's name, or None if not found.
    """
    author = get_meta_content(
        soup,
        "author",
        "article:author",
        "dc.creator",
        "byline",
    )
    if author:
        return author
    return author


def extract_date(soup: BeautifulSoup) -> str | None:
    """Extract the publication date in ISO 8601 format.

    Args:
        soup: Parsed HTML document.

    Returns:
        str: Publication date as YYYY-MM-DD, or None if missing.
    """
    date_str = get_meta_content(
        soup,
        "article:published_time",
        "datePublished",
        "date",
        "DC.date.issued",
    )
    if not date_str:
        return None
    try:
        parsed_date = parser.parse(date_str)
        return parsed_date.date().isoformat()
    except (parser.ParserError, TypeError, ValueError):
        return None


def extract_language(soup: BeautifulSoup) -> str | None:
    """Extract the primary language of the web document.

    Args:
        soup: Parsed HTML document.

    Returns:
        str: The language code (e.g., 'en', 'ja'), or None.
    """
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        return html_tag["lang"].strip()
    lang = get_meta_content(soup, "language", "dc.language")
    return lang or None


def get_access_date() -> str:
    """Return the current UTC date as an access date.

    Returns:
        str: Current date in ISO format (YYYY-MM-DD).
    """
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")


def cite_web(url: str) -> str:
    """Generate a Wikipedia-style {{cite web}} template from a URL.

    Args:
        url: The web page URL to cite.

    Returns:
        A {{cite web}} template with metadata fields.
    """
    tl = mwparserfromhell.nodes.Template("Cite web")

    try:
        soup = get_soup(url)
    except (requests.RequestException, RuntimeError):
        args = {
            "title": url,
            "url": url,
            "website": get_domain(url),
            "access-date": get_access_date(),
        }
    else:
        args = {
            "title": extract_title(soup),
            "url": url,
            "website": extract_website(soup, url),
            "author": extract_author(soup),
            "date": extract_date(soup),
            "language": extract_language(soup),
            "access-date": get_access_date(),
        }
    for param, value in args.items():
        if value:
            tl.add(param, value)
    return str(tl)


def ref(url: str, name: str | None = None) -> str:
    """Generate a <ref> tag from a URL.

    Args:
        url: The web page URL to cite.
        name: If given, <ref name="..."> will be used.

    Returns:
        A <ref> within {{cite web}} template with metadata fields.
    """
    open_tag = f'<ref name="{name}">' if name else "<ref>"
    close_tag = "</ref>"
    return f"{open_tag}{cite_web(url)}{close_tag}"
