"""
Generate a CSV recap matching NSI brand entries to images in xx/stores.

Sources:
- https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/supermarket.json
- https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/convenience.json

Matching rule:
- Use tags.brand as the exact match input, slugified with Django-style behavior.
- Keep one output row per NSI item (no deduplication across entries).

Outputs:
- docs/nsi/nsi-brand-match.csv
- docs/nsi/nsi-brand-match-stats.md

Usage: python scripts/generate_nsi_brand_match_csv.py
"""

import csv
import datetime
import json
import os
import re
import unicodedata
import urllib.error
import urllib.request

IMAGE_DIR = 'xx/stores'
OUTPUT_CSV = 'docs/nsi/nsi-brand-match.csv'
STATS_MD = 'docs/nsi/nsi-brand-match-stats.md'

NSI_SOURCES = [
    {
        'source_category': 'supermarket',
        'url': 'https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/supermarket.json',
    },
    {
        'source_category': 'convenience',
        'url': 'https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/convenience.json',
    },
]

CSV_COLUMNS = [
    'source_category',
    'nsi_id',
    'display_name',
    'tags_brand',
    'brand_wikidata',
    'location_include',
    'location_exclude',
    'match_names_count',
    'match_input_name',
    'match_slug',
    'match_status',
    'matched_image_svg',
    'matched_image_png',
]

STATS_HEADER = (
    '| Date | NSI items | Images (svg/png) | Exact matches | Match % |\n'
    '|------|-----------|------------------|---------------|---------|\n'
)


# Django-style slugify

def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii').lower()
    value = re.sub(r"'", '', value)
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = re.sub(r'-+', '-', value)
    return value.strip('-')


# Get all image filenames in xx/stores (all formats)

def get_image_files(image_dir):
    return [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]



def pick_formats(files):
    """Return (svg_filename, png_filename) from filenames for a given slug."""
    svg = next((f for f in files if f.lower().endswith('.svg')), '')
    png = next((f for f in files if f.lower().endswith('.png')), '')
    return svg, png



def fetch_json(url, timeout=30):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            payload = response.read().decode('utf-8')
        return json.loads(payload)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'Failed to download {url}: HTTP {exc.code}') from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f'Failed to download {url}: {exc.reason}') from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f'Failed to parse JSON from {url}: {exc}') from exc



def serialize_list(values):
    if not isinstance(values, list):
        return ''

    serialized = []
    for value in values:
        if isinstance(value, str):
            serialized.append(value)
        else:
            serialized.append(json.dumps(value, ensure_ascii=False, separators=(',', ':')))
    return '|'.join(serialized)



def extract_rows_from_source(source):
    category = source['source_category']
    url = source['url']
    data = fetch_json(url)

    if not isinstance(data, dict) or not isinstance(data.get('items'), list):
        raise RuntimeError(f'Unexpected NSI payload shape from {url}: missing list at key "items"')

    rows = []
    for item in data['items']:
        if not isinstance(item, dict):
            continue

        tags = item.get('tags') if isinstance(item.get('tags'), dict) else {}
        location_set = item.get('locationSet') if isinstance(item.get('locationSet'), dict) else {}
        match_names = item.get('matchNames') if isinstance(item.get('matchNames'), list) else []

        tags_brand = str(tags.get('brand', '')).strip()
        match_input_name = tags_brand
        match_slug = slugify(match_input_name) if match_input_name else ''

        rows.append(
            {
                'source_category': category,
                'nsi_id': str(item.get('id', '')).strip(),
                'display_name': str(item.get('displayName', '')).strip(),
                'tags_brand': tags_brand,
                'brand_wikidata': str(tags.get('brand:wikidata', '')).strip(),
                'location_include': serialize_list(location_set.get('include', [])),
                'location_exclude': serialize_list(location_set.get('exclude', [])),
                'match_names_count': str(len(match_names)),
                'match_input_name': match_input_name,
                'match_slug': match_slug,
                'match_status': 'no',
                'matched_image_svg': '',
                'matched_image_png': '',
            }
        )

    return rows



def write_stats_md(input_count, image_count, ext_counts, exact_count):
    today = datetime.date.today().strftime('%Y-%m-%d')
    svg_count = ext_counts.get('svg', 0)
    png_count = ext_counts.get('png', 0)
    match_pct = (exact_count / input_count * 100) if input_count else 0
    new_row = f'| {today} | {input_count} | {image_count} ({svg_count} svg / {png_count} png) | {exact_count} | {match_pct:.1f}% |\n'

    intro = (
        '# NSI Brand Match Stats\n\n'
        'Every time we run the NSI brand match script, we update this file with the latest stats on how many NSI brands '
        'from supermarket and convenience source files have exact slug matches in `xx/stores`.\n\n'
        'Sources:\n'
        '- https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/supermarket.json\n'
        '- https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/convenience.json\n\n'
    )

    if os.path.exists(STATS_MD):
        with open(STATS_MD, 'r', encoding='utf-8') as file_obj:
            content = file_obj.read()

        rows = []
        for line in content.splitlines():
            if not line.startswith('|') or line.startswith('| Date') or line.startswith('|---'):
                continue
            cells = [cell.strip() for cell in line.strip().split('|')[1:-1]]
            if len(cells) == 5:
                rows.append('| ' + ' | '.join(cells) + ' |\n')
        rows = [row for row in rows if not row.startswith(f'| {today} ')]
    else:
        rows = []

    rows.insert(0, new_row)

    with open(STATS_MD, 'w', encoding='utf-8') as file_obj:
        file_obj.write(intro + STATS_HEADER + ''.join(rows))



def main():
    print('Fetching NSI sources...')

    rows = []
    for source in NSI_SOURCES:
        source_rows = extract_rows_from_source(source)
        rows.extend(source_rows)
        print(f"Loaded {len(source_rows)} rows from {source['source_category']}")

    image_files = get_image_files(IMAGE_DIR)
    image_slugs = {}
    ext_counts = {}

    for filename in image_files:
        name, ext = os.path.splitext(filename)
        image_slugs.setdefault(name, []).append(filename)
        ext_key = ext.lower().lstrip('.')
        ext_counts[ext_key] = ext_counts.get(ext_key, 0) + 1

    print('Matching rows against image filenames...')
    for row in rows:
        match_slug = row['match_slug']
        if not match_slug:
            continue

        if match_slug in image_slugs:
            matched_svg, matched_png = pick_formats(image_slugs[match_slug])
            row['matched_image_svg'] = matched_svg
            row['matched_image_png'] = matched_png
            row['match_status'] = 'exact'

    rows.sort(key=lambda row: (row['tags_brand'].lower(), row['nsi_id'].lower()))

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    exact_count = sum(1 for row in rows if row['match_status'] == 'exact')
    write_stats_md(len(rows), len(image_files), ext_counts, exact_count)

    print(f'Wrote {len(rows)} rows to {OUTPUT_CSV}')
    print(f'Exact matches: {exact_count}')
    print(f'Updated stats: {STATS_MD}')


if __name__ == '__main__':
    main()
