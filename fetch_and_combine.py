#!/usr/bin/env python3
"""
TV Playlist Fetcher & Combiner
Fetches M3U playlists from multiple GitHub repos, filters by category,
removes duplicates, maps categories, and generates a combined master playlist.
"""

import requests
import re
import os
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse
import time
from collections import OrderedDict, Counter

# ── CONFIGURATION ──────────────────────────────────────────────────────────

SOURCE_URLS = [
    "https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u",
    "https://raw.githubusercontent.com/nuttle-nuttterr/Ds2/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/nuttle-nuttterr/tv-by-Gemini/main/master_playlist.m3u",
    "https://raw.githubusercontent.com/nuttle-nuttterr/tv-by-deepseek/main/master_playlist.m3u",
    "https://raw.githubusercontent.com/nuttle-nuttterr/Tv-by-Claude/main/master_playlist.m3u",
]

# Categories to REMOVE entirely (case-insensitive)
REMOVE_CATEGORIES = {
    "tamil spiritual",
    "tamil spiritual & devotional",
    "tamil movies",
    "tamil - movies",
    "english infotainment",
    "english - infotainment",
    "english national news",
    "english - news",
    "english business news",
    "english kids",
    "english - kids",
    "english international news",
    "english - international news",
}

# Categories to map into "Tamil Local Channels" (case-insensitive)
LOCAL_CATEGORY_ALIASES = {
    "tamil - local",
    "local channels",
    "tamil local channels",
    "tamil local",
}

# Categories to map into "Tamil Channels" (case-insensitive)
TAMIL_CATEGORY_ALIASES = {
    "tamil gec",
    "tamil - general entertainment (gec)",
    "tamil news",
    "tamil - news",
    "tamil comedy",
    "tamil iptv channels",
    "tamil infotainment",
    "tamil kids",
    "tamil - kids",
    "tamil music",
    "tamil - music",
    "tamil iptv channels",
    "tamil iptv",
}

# Headers for requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/plain,application/vnd.apple.mpegurl,*/*",
}

REQUEST_TIMEOUT = 30


def normalize_category(cat):
    """Normalize category name for comparison."""
    if not cat:
        return ""
    return cat.lower().strip()


def map_category(raw_category):
    """Map raw category to unified category name."""
    norm = normalize_category(raw_category)

    # Check removal list first
    if norm in REMOVE_CATEGORIES:
        return None

    # Map to Tamil Local Channels
    if norm in LOCAL_CATEGORY_ALIASES:
        return "Tamil Local Channels"

    # Map to Tamil Channels
    if norm in TAMIL_CATEGORY_ALIASES:
        return "Tamil Channels"

    # Keep other categories as-is (Sports, English Movies, English GEC, etc.)
    return raw_category.strip()


def fetch_playlist(url, retries=2):
    """Fetch an M3U playlist from URL with retries."""
    for attempt in range(retries + 1):
        try:
            print(f"  Fetching: {url}")
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            print(f"    Success ({len(resp.text)} chars)")
            return resp.text
        except Exception as e:
            print(f"    Attempt {attempt + 1} failed: {e}")
            if attempt < retries:
                time.sleep(2 ** attempt)
            else:
                print(f"    All retries exhausted for {url}")
    return None


def parse_m3u(content, source_name="unknown"):
    """Parse M3U content into channel entries with category info."""
    if not content:
        return []

    channels = []
    lines = content.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith('#EXTINF'):
            extinf = line

            # Extract channel name after the last comma
            if ',' in extinf:
                name = extinf.rsplit(',', 1)[-1].strip()
            else:
                name = "Unknown"

            # Extract tvg-name if present
            tvg_name_match = re.search(r'tvg-name="([^"]*)"', extinf)
            if tvg_name_match and tvg_name_match.group(1).strip():
                name = tvg_name_match.group(1).strip()

            # Extract group-title
            group_match = re.search(r'group-title="([^"]*)"', extinf)
            raw_category = group_match.group(1).strip() if group_match else "Uncategorized"

            # Map category
            mapped_category = map_category(raw_category)

            # Skip if category is in removal list
            if mapped_category is None:
                i += 1
                continue

            # Get URL
            url = ""
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith('#'):
                    url = next_line
                    break
                j += 1

            if url:
                channels.append({
                    'extinf': extinf,
                    'name': name,
                    'url': url,
                    'source': source_name,
                    'raw_category': raw_category,
                    'category': mapped_category,
                })
            i = j + 1
        else:
            i += 1

    return channels


def deduplicate_channels(channels):
    """Remove duplicate channels, keeping the first occurrence."""
    seen = {}
    unique = []

    for ch in channels:
        # Deduplication key: normalized name + URL base
        norm_name = re.sub(r'\s+', ' ', ch['name'].lower().strip())
        url_key = ch['url'].split('?')[0].rstrip('/')
        key = f"{norm_name}|{url_key}"

        if key not in seen:
            seen[key] = True
            unique.append(ch)

    return unique


def generate_m3u(channels):
    """Generate M3U content from channel list, grouped by category."""
    lines = ['#EXTM3U']

    # Add generation metadata
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    lines.append(f'#EXTINF:-1 tvg-name="Playlist Info",Generated: {now} | Channels: {len(channels)}')
    lines.append('https://example.com/placeholder')
    lines.append('')

    # Group channels by category
    categories = OrderedDict()
    for ch in channels:
        cat = ch['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ch)

    # Define category order
    category_order = [
        "Tamil Channels",
        "Tamil Local Channels",
        "Sports",
        "English Movies",
        "English GEC",
        "English Lifestyle",
        "English Lifestyle & Travel",
    ]

    # Sort categories: preferred order first, then alphabetically
    sorted_cats = []
    for cat in category_order:
        if cat in categories:
            sorted_cats.append(cat)
    for cat in sorted(categories.keys()):
        if cat not in category_order:
            sorted_cats.append(cat)

    for cat in sorted_cats:
        lines.append(f"# --- {cat} ---")
        for ch in categories[cat]:
            # Update the group-title in the EXTINF line
            updated_extinf = re.sub(
                r'group-title="[^"]*"',
                f'group-title="{cat}"',
                ch['extinf']
            )
            # If no group-title exists, insert it before the channel name
            if 'group-title=' not in updated_extinf:
                updated_extinf = updated_extinf.replace(
                    f',{ch["name"]}',
                    f' group-title="{cat}",{ch["name"]}'
                )
            lines.append(updated_extinf)
            lines.append(ch['url'])
            lines.append('')

    return '\n'.join(lines)


def main():
    print("=" * 60)
    print("TV Playlist Fetcher & Combiner")
    print("=" * 60)

    all_channels = []
    failed_sources = []

    # Fetch all sources
    for url in SOURCE_URLS:
        source_name = urlparse(url).path.split('/')[-2]
        content = fetch_playlist(url)

        if content:
            channels = parse_m3u(content, source_name)
            print(f"    Parsed {len(channels)} channels from {source_name}")
            all_channels.extend(channels)
        else:
            failed_sources.append(url)

    print(f"\nTotal channels before dedup: {len(all_channels)}")

    # Deduplicate
    unique = deduplicate_channels(all_channels)
    print(f"Channels after deduplication: {len(unique)}")

    # Sort: first by category, then by name
    unique.sort(key=lambda x: (x['category'].lower(), x['name'].lower()))

    # Generate output
    output = generate_m3u(unique)

    # Write to file
    output_file = 'master_playlist.m3u'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"\nOutput written to: {output_file}")
    print(f"  Total channels: {len(unique)}")

    print(f"\n  Category breakdown:")
    cat_counter = Counter(ch['category'] for ch in unique)
    for cat, count in cat_counter.most_common():
        print(f"    {cat}: {count}")

    if failed_sources:
        print(f"\nWarning: Failed sources ({len(failed_sources)}):")
        for fs in failed_sources:
            print(f"  - {fs}")

    # Write summary
    with open('update_summary.txt', 'w', encoding='utf-8') as f:
        f.write(f"Update: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write(f"Total sources: {len(SOURCE_URLS)}\n")
        f.write(f"Successful: {len(SOURCE_URLS) - len(failed_sources)}\n")
        f.write(f"Failed: {len(failed_sources)}\n")
        f.write(f"Total channels: {len(unique)}\n")
        f.write(f"\nCategory breakdown:\n")
        for cat, count in cat_counter.most_common():
            f.write(f"  {cat}: {count}\n")
        f.write("\nChannel list:\n")
        for ch in unique:
            f.write(f"  [{ch['category']}] {ch['name']} ({ch['source']})\n")

    print("Summary written to: update_summary.txt")
    return len(unique)


if __name__ == '__main__':
    main()
