#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
from pathlib import Path
from typing import List, Tuple, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# ----------------------------------------------------------------------
# CONFIGURATION ---------------------------------------------------------
BASE_URL = "http://redforce.live/"          # CHANGE TO YOUR SITE!
# Example: "https://your-live-tv-site.com/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/129.0.0.0 Safari/537.36"
    ),
    "Referer": BASE_URL,
}
REQUEST_DELAY = 0.8
TIMEOUT = 15
# ----------------------------------------------------------------------


def get_page(session: requests.Session) -> BeautifulSoup:
    url = BASE_URL.rstrip("/") + "/"
    print(f"Fetching: {url}")
    r = session.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")


def extract_channels(soup: BeautifulSoup) -> List[Tuple[str, List[str], str, str]]:
    """
    Yield: (name, categories, stream_id, logo_url)
    """
    channels = []

    for li in soup.select("ul#vidlink li"):
        a = li.find("a", {"onclick": True})
        if not a:
            continue

        onclick = a.get("onclick", "")
        m = re.search(r"stream=(\d+)", onclick)
        if not m:
            continue
        stream_id = m.group(1)

        img = a.find("img")
        if not img:
            continue

        name = img.get("alt", f"Channel {stream_id}").strip()
        logo_path = img.get("src")
        logo_url = urljoin(BASE_URL, logo_path) if logo_path else ""

        classes = li.get("class", [])
        categories = [c for c in classes if c and c != "All"]

        channels.append((name, categories, stream_id, logo_url))
        print(f"Found: {name} | ID: {stream_id} | Logo: {logo_url}")

    return channels


def resolve_stream_url(session: requests.Session, stream_id: str) -> Optional[str]:
    player_url = urljoin(BASE_URL, f"player.php?stream={stream_id}")
    try:
        r = session.get(player_url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"  [ERROR] {e}")
        return None

    text = r.text

    # Try multiple patterns
    patterns = [
        r'<iframe[^>]+src=["\']([^"\']*\.m3u8?[^"\']*)["\']',
        r'<source[^>]+src=["\']([^"\']*\.m3u8?[^"\']*)["\']',
        r'src\s*[:=]\s*["\']([^"\']*\.m3u8?[^"\']*)["\']',
        r'(https?://[^\s\'"]*\.m3u8[^\s\'"]*)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            url = match.group(1).strip()
            return urljoin(player_url, url)

    if ".m3u8" in r.url:
        return r.url

    print(f"  [WARN] No m3u8 found in player page (stream={stream_id})")
    return None


def build_m3u(channels: List[Tuple[str, List[str], str, str, str]]) -> str:
    lines = ["#EXTM3U"]
    #lines.append('#EXT-X-VERSION:3')

    for name, cats, stream_id, logo_url, m3u_url in channels:
        group = cats[0] if cats else "Uncategorized"
        clean_name = name.replace('"', "'").replace(",", " ")

        # tvg-logo = channel thumbnail
        logo_part = f' tvg-logo="{logo_url}"' if logo_url else ""

        extinf = f'#EXTINF:-1 tvg-name="{clean_name}"{logo_part} group-title="{group}",{clean_name}'
        lines.append(extinf)
        lines.append(m3u_url)
        lines.append("")

    return "\n".join(lines)


def main():
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        print("Downloading main page...")
        soup = get_page(session)

        print("Extracting channels with logos...")
        raw_channels = extract_channels(soup)
        print(f"Found {len(raw_channels)} channels.")

        if not raw_channels:
            print("No channels found. Check BASE_URL.")
            return

        print("\nResolving stream URLs...")
        resolved = []
        for name, cats, stream_id, logo_url in tqdm(raw_channels, desc="Resolving", unit="ch"):
            m3u_url = resolve_stream_url(session, stream_id)
            time.sleep(REQUEST_DELAY)
            if m3u_url:
                resolved.append((name, cats, stream_id, logo_url, m3u_url))
            else:
                print(f"  Failed: {name}")

        print(f"\nResolved {len(resolved)} streams.")

        if resolved:
            m3u_content = build_m3u(resolved)
            out_file = Path("channels.m3u")
            out_file.write_text(m3u_content, encoding="utf-8")
            print(f"\nM3U saved: {out_file.absolute()}")
            print(f"Channels with logos: {len(resolved)}")

            # Category summary
            from collections import Counter
            cat_count = Counter(cats[0] if cats else "Uncategorized" for _, cats, _, _, _ in resolved)
            print("\nCategory breakdown:")
            for cat, cnt in sorted(cat_count.items()):
                print(f"  {cat}: {cnt}")
        else:
            print("No valid streams found.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    import sys
    if sys.version_info < (3, 6):
        print("Python 3.6+ required.")
        sys.exit(1)
    main()
