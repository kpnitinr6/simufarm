#!/usr/bin/env python3
"""Collect up to 100 article URLs from a homepage and its linked archives."""

import argparse
import re
import sys
from collections import deque
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
POST_LIMIT = 100
PAGE_LIMIT = 20


def site_host(url):
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname or parts.username is not None:
        raise ValueError("Expected an HTTP(S) URL without embedded credentials")
    return parts.hostname.removeprefix("www."), parts.port


def fetch_page(session, url, host):
    for _ in range(6):
        if site_host(url) != host:
            raise ValueError("Page redirected outside the starting site")
        with session.get(url, timeout=(5, 15), allow_redirects=False) as response:
            if response.is_redirect:
                url = urljoin(url, response.headers["Location"])
                continue
            response.raise_for_status()
            if "html" not in response.headers.get("Content-Type", "").lower():
                raise ValueError("Expected an HTML page")
            return response.url, BeautifulSoup(response.content, "html.parser")
    raise ValueError("Too many redirects")


def wordpress_posts(session, page_url, soup, host):
    api_link = soup.select_one('link[rel="https://api.w.org/"][href]')
    if api_link is None:
        return []
    api_root = urljoin(page_url, api_link["href"])
    endpoint = urljoin(api_root.rstrip("/") + "/", "wp/v2/posts")
    try:
        if site_host(endpoint) != host:
            return []
        with session.get(
            endpoint,
            params={"per_page": POST_LIMIT, "_fields": "link"},
            timeout=(5, 15),
            allow_redirects=False,
        ) as response:
            response.raise_for_status()
            entries = response.json()
        if not isinstance(entries, list):
            raise TypeError("Expected a WordPress post list")
        return [
            entry["link"]
            for entry in entries
            if isinstance(entry, dict) and isinstance(entry.get("link"), str)
        ]
    except (TypeError, ValueError, requests.RequestException) as exc:
        print(
            f"WordPress post listing unavailable; scanning HTML archives ({exc})", file=sys.stderr
        )
        return []


def add_post(posts, parts, origin):
    post_id = parse_qs(parts.query).get("p", [""])[0]
    query = urlencode({"p": post_id}) if post_id.isdecimal() else ""
    path = parts.path or "/"
    canonical = urlunsplit((origin.scheme, origin.netloc, path, query, ""))
    posts.setdefault((path.rstrip("/") or "/", query), canonical)


def collect(start_url, session):
    host = site_host(start_url)
    pending = deque([start_url])
    seen_pages = {start_url}
    posts = {}
    for page_index in range(PAGE_LIMIT):
        if not pending or len(posts) >= POST_LIMIT:
            break
        page_url, soup = fetch_page(session, pending.popleft(), host)
        origin = urlsplit(page_url)
        title_links = {
            id(link)
            for link in soup.select("article h1 a, article h2 a, article h3 a, a[rel~=bookmark]")
        }
        for link in soup.select("a[href]"):
            href = link["href"].strip()
            if not href or href.startswith("#"):
                continue
            try:
                parts = urlsplit(urljoin(page_url, href))
                if site_host(parts.geturl()) != host:
                    continue
            except ValueError:
                continue
            path = parts.path.rstrip("/") or "/"
            query = parse_qs(parts.query)
            post_id = query.get("p", [""])[0]
            page_number = query.get("paged", [""])[0]
            archive = (
                path in ("/blog", "/posts")
                or path.startswith(("/category/", "/tag/"))
                or re.search(r"/page/\d+$", path)
                or "next" in link.get("rel", [])
                or page_number.isdecimal()
            )
            if archive:
                page = urlunsplit(
                    (
                        origin.scheme,
                        origin.netloc,
                        parts.path or "/",
                        urlencode({"paged": page_number}) if page_number.isdecimal() else "",
                        "",
                    )
                )
                if page not in seen_pages:
                    seen_pages.add(page)
                    pending.append(page)
                continue
            if path.startswith(("/wp-", "/author/")):
                continue
            if (
                post_id.isdecimal()
                or (path != "/" and id(link) in title_links)
                or path.startswith(("/post/", "/posts/", "/blog/"))
                or re.fullmatch(r"/[^/]+/\d+", path)
            ):
                add_post(posts, parts, origin)
                if len(posts) == POST_LIMIT:
                    break
        if page_index == 0 and len(posts) < POST_LIMIT:
            for href in wordpress_posts(session, page_url, soup, host):
                try:
                    parts = urlsplit(urljoin(page_url, href))
                    if site_host(parts.geturl()) != host:
                        continue
                except ValueError:
                    continue
                add_post(posts, parts, origin)
                if len(posts) == POST_LIMIT:
                    break
    return list(posts.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Starting homepage URL")
    parser.add_argument("--output", type=Path, default=ROOT / "data/target_urls.txt")
    args = parser.parse_args()
    try:
        with requests.Session() as session:
            urls = collect(args.url, session)
        if not urls:
            raise ValueError("No article URLs found")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("\n".join(urls) + "\n", encoding="utf-8")
    except (ValueError, OSError, requests.RequestException) as exc:
        parser.exit(1, f"Collection failed: {exc}\n")
    print(f"Wrote {len(urls)} unique article URLs to {args.output}")


if __name__ == "__main__":
    main()
