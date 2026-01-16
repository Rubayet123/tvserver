#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import asyncio
from pathlib import Path
from typing import List, Tuple, Optional
from urllib.parse import urljoin
from collections import Counter

import aiohttp
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm_asyncio

# ----------------------------------------------------------------------
# CONFIGURATION
BASE_URL = "http://redforce.live/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/129.0.0.0 Safari/537.36"
    ),
    "Referer": BASE_URL,
}

MAX_CONCURRENCY = 10
MAX_RETRIES = 3
REQUEST_TIMEOUT = 15
RETRY_BACKOFF = 1.5
# ----------------------------------------------------------------------


# ---------------------- ASYNC HELPERS ----------------------------------

async def fetch_text(
    session: aiohttp.ClientSession,
    url: str,
    retries: int = MAX_RETRIES
) -> Optional[str]:
    timeout = ClientTimeout(total=REQUEST_TIMEOUT)

    for attempt in range(1, retries + 1):
        try:
            async with session.get(url, timeout=timeout) as resp:
                resp.raise_for_status()
                return await resp.text()

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if attempt == retries:
                print(f"[ERROR] {url} → {e}")
                return None

            await asyncio.sleep(RETRY_BACKOFF ** attempt)

    return None


# ---------------------- SCRAPING LOGIC ---------------------------------

async def get_main_page(session) -> BeautifulSoup:
    url = BASE_URL.rstrip("/") + "/"
    print(f"Fetching: {url}")
    html = await fetch_text(session, url)
    if not html:
        raise RuntimeError("Failed to fetch main page")
    return BeautifulSoup(html, "lxml")


def extract_channels(
    soup: BeautifulSoup
) -> List[Tuple[str, List[str], str, str]]:
    channels = []

    for li in soup.select("ul#vidlink li"):
        a = li.find("a", {"onclick": True})
        if not a:
            continue

        m = re.search(r"stream=(\d+)", a.get("onclick", ""))
        if not m:
            continue
        stream_id = m.group(1)

        img = a.find("img")
        if not img:
            continue

        name = img.get("alt", f"Channel {stream_id}").strip()
        logo_path = img.get("src", "")
        logo_url = urljoin(BASE_URL, logo_path)

        classes = li.get("class", [])
        categories = [c for c in classes if c and c != "All"]

        channels.append((name, categories, stream_id, logo_url))
        print(f"Found: {name} | ID: {stream_id}")

    return channels


async def resolve_stream(
    sem: asyncio.Semaphore,
    session: aiohttp.ClientSession,
    channel
) -> Optional[Tuple[str, List[str], str, str, str]]:
    name, cats, stream_id, logo_url = channel
    player_url = urljoin(BASE_URL, f"player.php?stream={stream_id}")

    async with sem:
        html = await fetch_text(session, player_url)
        if not html:
            return None

    patterns = [
        r'<iframe[^>]+src=["\']([^"\']*\.m3u8[^"\']*)["\']',
        r'<source[^>]+src=["\']([^"\']*\.m3u8[^"\']*)["\']',
        r'(https?://[^\s\'"]*\.m3u8[^\s\'"]*)',
    ]

    for p in patterns:
        m = re.search(p, html, re.I)
        if m:
            m3u = urljoin(player_url, m.group(1))
            return (name, cats, stream_id, logo_url, m3u)

    print(f"[WARN] No m3u8: {name}")
    return None


# ---------------------- OUTPUT -----------------------------------------

def build_m3u(channels) -> str:
    lines = ["#EXTM3U"]

    for name, cats, _, logo_url, m3u_url in channels:
        group = cats[0] if cats else "Uncategorized"
        clean = name.replace('"', "'").replace(",", " ")
        logo = f' tvg-logo="{logo_url}"' if logo_url else ""

        lines.append(
            f'#EXTINF:-1 tvg-name="{clean}"{logo} group-title="{group}",{clean}'
        )
        lines.append(m3u_url)
        lines.append("")

    return "\n".join(lines)


# ---------------------- MAIN -------------------------------------------

async def main():
    sem = asyncio.Semaphore(MAX_CONCURRENCY)

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        soup = await get_main_page(session)
        channels = extract_channels(soup)

        print(f"\nFound {len(channels)} channels")
        if not channels:
            return

        tasks = [
            resolve_stream(sem, session, ch)
            for ch in channels
        ]

        resolved = [
            r for r in await tqdm_asyncio.gather(
                *tasks, desc="Resolving", unit="ch"
            )
            if r
        ]

    print(f"\nResolved {len(resolved)} streams")

    if not resolved:
        print("No valid streams found")
        return

    m3u = build_m3u(resolved)
    out = Path("channels-rforce.m3u")
    out.write_text(m3u, encoding="utf-8")

    print(f"\nSaved: {out.absolute()}")

    cat_count = Counter(c[1][0] if c[1] else "Uncategorized" for c in resolved)
    print("\nCategory breakdown:")
    for k, v in sorted(cat_count.items()):
        print(f"  {k}: {v}")


# ---------------------- ENTRY ------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
