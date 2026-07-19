#!/usr/bin/env python3
"""
TV Playlist Fetcher & Combiner
Fetches M3U playlists from multiple GitHub repos, filters working local channels,
removes duplicates, and generates a combined master playlist.
"""

import requests
import re
import os
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse
import time

# ── CONFIGURATION ──────────────────────────────────────────────────────────

SOURCE_URLS = [
    "https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u",
    "https://raw.githubusercontent.com/nuttle-nuttterr/Ds2/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/nuttle-nuttterr/tv-by-Gemini/main/master_playlist.m3u",
    "https://raw.githubusercontent.com/nuttle-nuttterr/tv-by-deepseek/main/master_playlist.m3u",
    "https://raw.githubusercontent.com/nuttle-nuttterr/Tv-by-Claude/main/master_playlist.m3u",
]

# Channels to KEEP (from your video — exact & normalized matching)
WANTED_CHANNELS = {
    # Exact names as they appear in playlists
    "apple tv", "apple tv klm", "apple tv nagercoil", "apple tv marthandam", "apple tv puducherry",
    "akash tv", "aps gold", "aps tv gold",
    "boys tv",
    "chithiram tv", "chithiram tv",
    "d tv", "dtv",
    "dark tv", "dark television",
    "dd tamil",
    "disney channel",
    "eesan tv", "eesan tv",
    "eet live", "eet tv",
    "eurosport",
    "hbo",
    "irattipaathai tv", "irattaipaathai", "irattaipaathai tv",
    "isaiaruvi", "isai saaral",
    "j movie",
    "jaya max", "jaya tv",
    "jc tv",
    "jcv musix", "jcv musix", "jcv tv",
    "jeyam tv", "jeyam television",
    "jeyson tv",
    "jj max",
    "kalaignar tv",
    "kcn tv",
    "king tv", "king tv ranipet", "king tv alangulam", "king 24/7",
    "ktv",
    "malai murasu",
    "mcn tv",
    "mnx", "mnx tv",
    "moon tv",
    "movies now",
    "murasu", "murasu tv",
    "news j",
    "news18 tamil nadu",
    "news7 tamil",
    "nickelodeon",
    "ntv", "ntv trichy", "ntc tv",
    "oscar tv",
    "polimer news", "polimer news (576p)",
    "polimer tv", "polimer tv (720p)", "polimer channel",
    "pr tv",
    "puthiya thalaimurai",
    "puthuyagam tv",
    "raj digital plus", "raj digital plus",
    "raj musix tamil",
    "raj news tamil",
    "raj tv",
    "riya tv",
    "roja tv",
    "romedy now",
    "sakthi tv", "shakthi channel", "sakthi tv nellai",
    "sana", "sana plus", "sana tv",
    "sathiyam tv", "sathiyam tv",
    "siripoli", "sirippoli",
    "smcv tv",
    "sony pix",
    "sony sports ten 2",
    "sony sports ten 5",
    "star movies",
    "star sports 1", "star sports 2",
    "star sports select 1", "star sports select 2",
    "stn tv", "stn tv hd",
    "subin tv", "subin tv", "subi tv",
    "suriyan tv", "sooriyan tv", "sooriyan tv cinema",
    "surya tv", "surya tv", "suryaa tv",
    "thalaa tv tam", "thalaa tv",
    "thanthi tv", "thanthi tv (576p)",
    "thendral tv", "thendral tv madurai", "thendral tv chennai", "thendral tv nellai", "thendral tv alangulam",
    "thirai tv", "thirai tamil tv", "thirai music", "thirai isai",
    "udhayam tv", "udhayam tv",
    "utv", "utv coimbatore",
    "vendhar tv",
    "vidyal tv", "vidiyal tv",
    "wb", "we baduga tv",
    "win news", "win vision tv",
    "yet tv", "yet max",
    "zee tamil",
    # Additional local Tamil channels from your M3U that should be included
    "7 green", "7 green 4k", "7star music", "7star television", "7star tv",
    "a1 media news", "a1 tv ariyalur",
    "aadhavan tv", "aadhavan colours",
    "aadvik tv",
    "aarthi tv",
    "aaryaa tv",
    "aasai tv",
    "aathi tv",
    "acn tv",
    "acp classic", "acp isai oli", "acp tv",
    "actionhollywood",
    "adhisayam tv",
    "agaram tv",
    "aha tv",
    "ajk movie", "ajk tv",
    "akilam tv",
    "amma tv", "amma tv nagercoil", "amma vision", "amman tv",
    "analai express", "analai express cinema", "analai express replay", "analai music",
    "anandam abi tv", "anandam tv", "anandam tv madurai", "anandam utv",
    "anandham tv",
    "anbu tv",
    "anjai tv",
    "annai tv",
    "appu tv",
    "aramm tv",
    "arasu tv",
    "arighni tv",
    "ark tv", "ark tv [ktisma]",
    "arputhar yesu tv", "arputhar yesu tv [livebox]",
    "arul tv",
    "aruljothi tv",
    "arun tv",
    "asoka tv",
    "atn",
    "auro tv",
    "avs tv",
    "ayya tv", "ayya agilathirattu tv",
    "azhagi tv",
    "banyan tv",
    "bhagavath tv",
    "bhairava tv",
    "bhakthi tv",
    "bharathi thirai ulagam",
    "bible tv",
    "blood of jesus tv",
    "bright simrose tv",
    "bw tv",
    "channel 316", "channel spice",
    "chola tv",
    "city tv", "city tv kanchipuram",
    "crayonz tv",
    "cross tv",
    "crs tv",
    "csk tv",
    "ctn conoor",
    "cuddalore voice tv",
    "d jeyam",
    "deavathai tv",
    "deebam tv",
    "deepam tv",
    "deiveega oli tv",
    "delta tv",
    "deva tv",
    "devi tv",
    "dharshan tv",
    "dharumai adeenam tv",
    "dheiveegam tv",
    "dina tharani",
    "dm tv",
    "dolphin tv", "dolphin tv sivakasi",
    "durai melodies", "durai tv",
    "duresh tv",
    "eagle tv", "eagle tv nagercoil",
    "emperor tv",
    "events",
    "eye tamil", "eye tamil comedy", "eye tamil music",
    "ezhil tv",
    "ezra tv",
    "family channel",
    "fashion",
    "fort channels",
    "g max",
    "ganesh tv",
    "garudan tv",
    "gem tv",
    "gjv tv",
    "go revival tv",
    "good news time",
    "gospel tv",
    "grace tv",
    "gsjk tv",
    "hai tv",
    "harin tv",
    "heaven tv",
    "hello tamil tv",
    "hitech tv",
    "holy land tv",
    "horror movies",
    "idhayam kids", "idhayam tv",
    "imai tv",
    "isai tv",
    "islamic channel",
    "ithazh tv",
    "j king tv",
    "j jeyam",
    "jay tv",
    "jawahar channel", "jawahar channel hd",
    "jayaam tv",
    "jayam tv", "jayam tv namakkal", "jayam tv karur", "jayam tv polur", "jayam tv sivakasi", "jayam tv tenkasi", "jayam tv trichy",
    "jeeva oli tv", "jeeva tv",
    "jeevaneerodai tv",
    "jeiyan tv",
    "jenifer tv",
    "jesus tv",
    "jeyam plus", "jeyasubbu tv",
    "jhp tv",
    "jith tv",
    "jj news tamil",
    "jos tv",
    "jose tv",
    "joshua praise tv", "joshua tv",
    "joy goodnews tv", "joy tv", "joy tv hd",
    "jrp tv",
    "jtk tv",
    "kaalai tv",
    "k channel",
    "kanchi media", "kanchi tv",
    "karthick tv",
    "kavin tv",
    "kc music", "kc tv",
    "kings tv",
    "km television", "35 km television",
    "koodal tv",
    "krish tv",
    "krn tv",
    "ksr tv",
    "kumari kathir tv", "kumari tv",
    "leo tv",
    "life tv",
    "lion tv",
    "lourdes tv",
    "love joy tv",
    "lucky tv", "lucky tv tenkasi",
    "m television",
    "m&m tv",
    "maa tv",
    "madura tv",
    "madurai arasi tv",
    "magalir tv",
    "mahimai tv",
    "maisha tv", "manisha tv",
    "makkalpani tv",
    "malar tv surandai",
    "mallai tv",
    "manasu tv",
    "mangalam tv",
    "maniway tv",
    "mariya annai tv", "mariya matha tv",
    "maruthi tv",
    "matha tv",
    "mathan tv",
    "mathi tv",
    "max movies",
    "mayil tv",
    "mdn tv",
    "me24 tamil",
    "media",
    "mei alai tv",
    "meiveli tv",
    "minnal tv",
    "miyami 1", "miyami 2", "miyami tv",
    "mn tv",
    "models",
    "montamil",
    "mullai tv",
    "my faith tv",
    "my jesus tv",
    "namathu sangamam tv",
    "namma gobi tv",
    "nanjil natham tv",
    "national geo",
    "naveen tv",
    "nijam tv",
    "nisha tv",
    "nrj tv",
    "ntn tv",
    "ohm tv",
    "oli tv",
    "om sakthi tv", "om tv",
    "omm tv nagercoil",
    "orange tv",
    "params tv", "1 params tv",
    "pcn channel", "pcn tv",
    "peniel tv",
    "pg tv",
    "pj tv",
    "pn tv",
    "pothigai prime", "pothigai thendral",
    "praise tv",
    "prime music",
    "prince tv",
    "pugal tv",
    "punnagai desam tv",
    "r tv",
    "raagam friends tv", "raga tv",
    "raghul tv",
    "ragam tv",
    "rainbow tv", "rainbow tv gandarvakottai",
    "ramya tv",
    "ratchagar tv",
    "retro music",
    "ridsys tv",
    "right tv", "46 right tv",
    "rj tamil",
    "rk tv",
    "rock tv",
    "roja movies",
    "royal tv", "royal tv guduvancheri", "royal tv nellai",
    "rs tv",
    "ruby digital tv",
    "rudhram tv",
    "ruhasha tv",
    "s media puducherry",
    "s tv", "s tv madurai",
    "sabari tv aruppukottai",
    "sahara tv",
    "sai tv madurai", "sai tv tenkasi",
    "sailam tv",
    "sakthi tv nellai",
    "salaam tv",
    "salvation tv",
    "samugam media",
    "sar tv",
    "sarvik tv",
    "sasi tv",
    "sd media",
    "selfie tv",
    "selva tamil tv",
    "senthur tv",
    "sha tv",
    "shakthi channel",
    "shalwin tv",
    "shark tv",
    "sharon tv",
    "shekinah tv",
    "siddhar isai", "siddhar tv",
    "silver sat media",
    "singam tv",
    "sirustigar tv",
    "siva tv",
    "sk music", "sk tv karur",
    "sky tv karur", "sky tv sathankulam",
    "smart sri", "smart sri tv",
    "snr tv",
    "sr musix", "sr tv",
    "sree saravanaa tv",
    "sri arjun tv",
    "sri krishna tv",
    "sri sai tv",
    "sri tv",
    "sri varahi tv",
    "sri velavan tv",
    "sri vinayaga movies", "sri vinayaga music", "sri vinayaga tv",
    "ss music", "ss tv", "ss tv nagercoil",
    "star media",
    "subash tv tenkasi",
    "subi tv",
    "succes tv tamil",
    "sun smart tv",
    "super tv dindigul",
    "superstar tv",
    "swastik tv",
    "tamil magan tv",
    "tamil oli tv",
    "tamil star tv",
    "tamil tv", "tamil tv christian",
    "tamil vision international",
    "telemax tamil",
    "thangam tv",
    "tharun movies",
    "thendral tv alangulam",
    "thirai isai", "thirai music",
    "thirumalai tv", "thirumalai tv vadipatti",
    "thoma tv",
    "thuthi tv",
    "time tv",
    "tiruppur voice tv",
    "tnse",
    "top tv thuraiyur",
    "ttn tv",
    "twoc tv",
    "urchagam tv",
    "uthamiyae tv",
    "v tamil", "v tamizh",
    "vac tv",
    "vajra tv", "23 vajra tv",
    "vani tv",
    "vasantham tv",
    "vds tv",
    "veera tv",
    "vetri tv",
    "vimal tv",
    "vinayaga tv", "vinayaka tv", "79 vinayaga tv",
    "vinmeen music",
    "vip tv virudhunagar",
    "visaka tv",
    "vishil tv 2",
    "vision tv",
    "vtv trichy",
    "we baduga tv",
    "win vision tv",
    "yatra tv",
    "yet max",
    "yours tv",
    "0 info tv", "0 info tv",
    "11 om tv",
    "117 king 24/7",
    "118 queens tv",
    "126 shakthi channel",
    "186 jet tv",
    "194 coimbatore",
    "203 thirai tv",
    "204 thirai music",
    "209 himalaya tv",
    "219 rohith tv",
    "2 ashoka tv",
    "4 vaagai tv",
    "50 citi channel",
    "501 ಅಶೋಕ info tv",
    "52 voice tv",
    "600 km news bengaluru",
    "602 music beats",
    "603 kadamba",
    "604 nam city1",
    "605 rr tv 1",
    "606 rr tv 2",
    "607 sne",
    "608 siri",
    "609 sity",
    "610 amogha",
    "611 kalki",
    "612 swastik",
    "613 metro",
    "615 akashtv",
    "61 jeeva tv",
    "70 hansitha tv",
    "77 mtntv",
    "80 devi tv",
    "81 esan tv",
    "83 chola rv",
    "84 hitech tv",
    "88 km music",
    "90 aalaya magimai tv",
    "902 atn samachar",
    "908 wild tv",
    "909 media 9",
    "910 voice of maharashtra",
    "911 ten news",
    "912 soochnaindia tv",
    "913 satyam satya",
    "92 deivega oil",
    "920 tv hindustan national",
    "921 nation bharat tv",
    "922 vii media",
}

# Headers for requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/plain,application/vnd.apple.mpegurl,*/*",
}

REQUEST_TIMEOUT = 30


def normalize_name(name):
    """Normalize channel name for comparison."""
    if not name:
        return ""
    # Lowercase, remove extra spaces, common suffixes/prefixes
    n = name.lower().strip()
    n = re.sub(r'\s+', ' ', n)
    n = re.sub(r'\[.*?\]', '', n)  # Remove [tags]
    n = re.sub(r'\(.*?\)', '', n)  # Remove (quality tags)
    n = re.sub(r'\s+', ' ', n).strip()
    return n


def fetch_playlist(url, retries=2):
    """Fetch an M3U playlist from URL with retries."""
    for attempt in range(retries + 1):
        try:
            print(f"  Fetching: {url}")
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            print(f"    ✓ Success ({len(resp.text)} chars)")
            return resp.text
        except Exception as e:
            print(f"    ✗ Attempt {attempt + 1} failed: {e}")
            if attempt < retries:
                time.sleep(2 ** attempt)
            else:
                print(f"    ✗ All retries exhausted for {url}")
    return None


def parse_m3u(content, source_name="unknown"):
    """Parse M3U content into channel entries."""
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

            # Extract tvg-name if present (more reliable)
            tvg_name_match = re.search(r'tvg-name="([^"]*)"', extinf)
            if tvg_name_match and tvg_name_match.group(1).strip():
                name = tvg_name_match.group(1).strip()

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
                    'norm': normalize_name(name),
                })
            i = j + 1
        else:
            i += 1

    return channels


def is_wanted(channel):
    """Check if a channel is in the wanted list."""
    norm = channel['norm']

    # Direct match
    if norm in WANTED_CHANNELS:
        return True

    # Check if any wanted channel is a substring (for partial matches)
    for wanted in WANTED_CHANNELS:
        if wanted in norm or norm in wanted:
            # Avoid false positives with very short names
            if len(wanted) >= 4 or len(norm) >= 4:
                return True

    return False


def deduplicate_channels(channels):
    """Remove duplicate channels, keeping the first occurrence."""
    seen = {}
    unique = []

    for ch in channels:
        # Create a deduplication key from normalized name
        key = ch['norm']

        # Also check URL-based dedup
        url_key = ch['url'].split('?')[0].rstrip('/')

        if key not in seen and url_key not in seen:
            seen[key] = True
            seen[url_key] = True
            unique.append(ch)

    return unique


def validate_url(url):
    """Basic URL validation."""
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https') and parsed.netloc


def generate_m3u(channels):
    """Generate M3U content from channel list."""
    lines = ['#EXTM3U']

    # Add generation metadata
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    lines.append(f'#EXTINF:-1 tvg-name="Playlist Info",Generated: {now} | Channels: {len(channels)}')
    lines.append('https://example.com/placeholder')
    lines.append('')

    for ch in channels:
        lines.append(ch['extinf'])
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
        source_name = urlparse(url).path.split('/')[-2]  # repo name
        content = fetch_playlist(url)

        if content:
            channels = parse_m3u(content, source_name)
            print(f"    Parsed {len(channels)} channels from {source_name}")
            all_channels.extend(channels)
        else:
            failed_sources.append(url)

    print(f"\nTotal channels before filtering: {len(all_channels)}")

    # Filter wanted channels
    wanted = [ch for ch in all_channels if is_wanted(ch)]
    print(f"Wanted channels after filtering: {len(wanted)}")

    # Deduplicate
    unique = deduplicate_channels(wanted)
    print(f"Channels after deduplication: {len(unique)}")

    # Sort alphabetically by name
    unique.sort(key=lambda x: x['name'].lower())

    # Generate output
    output = generate_m3u(unique)

    # Write to file
    output_file = 'master_playlist.m3u'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"\n✓ Output written to: {output_file}")
    print(f"  Total channels: {len(unique)}")

    if failed_sources:
        print(f"\n⚠ Failed sources ({len(failed_sources)}):")
        for fs in failed_sources:
            print(f"  - {fs}")

    # Write summary
    with open('update_summary.txt', 'w', encoding='utf-8') as f:
        f.write(f"Update: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write(f"Total sources: {len(SOURCE_URLS)}\n")
        f.write(f"Successful: {len(SOURCE_URLS) - len(failed_sources)}\n")
        f.write(f"Failed: {len(failed_sources)}\n")
        f.write(f"Total channels: {len(unique)}\n")
        f.write("\nChannel list:\n")
        for ch in unique:
            f.write(f"  - {ch['name']} ({ch['source']})\n")

    print("✓ Summary written to: update_summary.txt")
    return len(unique)


if __name__ == '__main__':
    main()
