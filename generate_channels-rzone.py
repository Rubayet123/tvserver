import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, Any

# ────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────

BASE = "https://tv.roarzone.info/api/android"
CHANNELS_API = f"{BASE}/channels.php"
STREAM_API = f"{BASE}/stream.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

OUT_FILE = "channels-rzone.m3u"

MAX_WORKERS = 5           # ← tune this: 8–20 usually good for ~90 channels
REQUEST_TIMEOUT = 10      # seconds
SLEEP_AFTER_FAIL = 1.2    # small backoff when request fails

# ────────────────────────────────────────────────

def get_channels() -> list[dict]:
    try:
        r = requests.get(CHANNELS_API, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        if data.get("success"):
            print(f"Found {len(data['channels'])} channels")
            return data["channels"]
        print("Channels API did not return success")
        return []
    except Exception as e:
        print(f"Failed to get channel list: {e}")
        return []


def get_stream_url(stream_name: str) -> Optional[str]:
    try:
        r = requests.get(
            STREAM_API,
            params={"channel": stream_name},
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )
        r.raise_for_status()
        data: Dict[str, Any] = r.json()

        if data.get("success") and "url" in data:
            return data["url"]

        print(f"  ✗ {stream_name:<28} → no success / no url")
        return None

    except requests.exceptions.RequestException as e:
        print(f"  ✗ {stream_name:<28} → {e.__class__.__name__}")
        time.sleep(SLEEP_AFTER_FAIL)
        return None


def main():
    channels = get_channels()
    if not channels:
        print("No channels loaded → exiting")
        return

    print(f"\nStarting to fetch stream URLs (max {MAX_WORKERS} concurrent)...\n")

    start_time = time.time()

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")

        # We'll collect results as they complete
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_channel = {
                executor.submit(get_stream_url, ch["stream_name"]): ch
                for ch in channels
            }

            done_count = 0
            total = len(channels)

            for future in as_completed(future_to_channel):
                ch = future_to_channel[future]
                done_count += 1

                try:
                    url = future.result()
                    if url:
                        title = ch["title"]
                        logo = ch["logo"]
                        group = ch["category"]

                        f.write(
                            f'#EXTINF:-1 tvg-name="{title}" '
                            f'tvg-logo="{logo}" '
                            f'group-title="{group}",{title}\n'
                        )
                        f.write(f"{url}\n")

                        print(f"  ✓ {title} ({done_count}/{total})")
                    else:
                        print(f"  - {ch['title']} skipped ({done_count}/{total})")

                except Exception as e:
                    print(f"Unexpected error for {ch['title']}: {e}")

    elapsed = time.time() - start_time
    print(f"\nDone! Playlist written: {OUT_FILE}")
    print(f"Time taken: {elapsed:.1f} seconds")


if __name__ == "__main__":
    main()