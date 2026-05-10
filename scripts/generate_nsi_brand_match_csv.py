"""
Generate a CSV recap matching NSI brand entries to images in xx/stores.

Sources are configured in nsi/sources.json.

Matching rule:
- Use tags.brand as the exact match input, slugified with Django-style behavior.
- Keep one output row per NSI item (no deduplication across entries).

Outputs:
- nsi/brand-match.csv
- nsi/brand-match-stats.md

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
OUTPUT_CSV = 'nsi/brand-match.csv'
STATS_MD = 'nsi/brand-match-stats.md'
SOURCES_JSON = 'nsi/sources.json'

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
    '| Date | NSI items | Images (svg/png) | Match svg | Match png | Overall match % |\n'
    '|------|-----------|------------------|----------:|----------:|----------------:|\n'
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


def match_status_from_formats(svg_filename, png_filename):
    if svg_filename and png_filename:
        return 'both'
    if svg_filename:
        return 'only_svg'
    if png_filename:
        return 'only_png'
    return 'no'


def load_sources(sources_path):
    if not os.path.exists(sources_path):
        raise RuntimeError(f'Missing sources file: {sources_path}')

    with open(sources_path, 'r', encoding='utf-8') as file_obj:
        data = json.load(file_obj)

    if not isinstance(data, list):
        raise RuntimeError(f'Invalid sources format in {sources_path}: expected a list')

    sources = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise RuntimeError(f'Invalid source at index {index} in {sources_path}: expected an object')

        source_category = str(item.get('source_category', '')).strip()
        url = str(item.get('url', '')).strip()

        if not source_category or not url:
            raise RuntimeError(
                f'Invalid source at index {index} in {sources_path}: source_category and url are required'
            )

        sources.append({'source_category': source_category, 'url': url})

    if not sources:
        raise RuntimeError(f'No sources configured in {sources_path}')

    return sources



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



def write_stats_md(
    input_count,
    image_count,
    ext_counts,
    svg_match_count,
    png_match_count,
    overall_match_count,
    source_count,
):
    today = datetime.date.today().strftime('%Y-%m-%d')
    svg_count = ext_counts.get('svg', 0)
    png_count = ext_counts.get('png', 0)
    overall_match_pct = (overall_match_count / input_count * 100) if input_count else 0
    new_row = (
        f'| {today} | {input_count} | {image_count} ({svg_count} svg / {png_count} png) '
        f'| {svg_match_count} | {png_match_count} | {overall_match_pct:.1f}% |\n'
    )

    intro = (
        '# NSI Brand Match Stats\n\n'
        'Every time we run the NSI brand match script, we update this file with the latest stats on how many NSI brands '
        'from configured source files match SVG/PNG images in `xx/stores`, plus the overall match rate.\n\n'
        f'Sources config: `{SOURCES_JSON}` ({source_count} URLs).\n\n'
    )

    if os.path.exists(STATS_MD):
        with open(STATS_MD, 'r', encoding='utf-8') as file_obj:
            content = file_obj.read()

        rows = []
        for line in content.splitlines():
            if not line.startswith('|') or line.startswith('| Date') or line.startswith('|---'):
                continue
            cells = [cell.strip() for cell in line.strip().split('|')[1:-1]]
            if len(cells) == 6:
                rows.append('| ' + ' | '.join(cells) + ' |\n')
        rows = [row for row in rows if not row.startswith(f'| {today} ')]
    else:
        rows = []

    rows.insert(0, new_row)

    with open(STATS_MD, 'w', encoding='utf-8') as file_obj:
        file_obj.write(intro + STATS_HEADER + ''.join(rows))



def main():
    print('Fetching NSI sources...')
    sources = load_sources(SOURCES_JSON)

    rows = []
    for source in sources:
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
            row['match_status'] = match_status_from_formats(matched_svg, matched_png)

    rows.sort(key=lambda row: (row['tags_brand'].lower(), row['nsi_id'].lower()))

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    svg_match_count = sum(1 for row in rows if row['match_status'] in ('both', 'only_svg'))
    png_match_count = sum(1 for row in rows if row['match_status'] in ('both', 'only_png'))
    overall_match_count = sum(1 for row in rows if row['match_status'] != 'no')
    source_count = len(sources)
    write_stats_md(
        len(rows),
        len(image_files),
        ext_counts,
        svg_match_count,
        png_match_count,
        overall_match_count,
        source_count,
    )

    print(f'Wrote {len(rows)} rows to {OUTPUT_CSV}')
    print(f'Match svg: {svg_match_count}')
    print(f'Match png: {png_match_count}')
    print(f'Overall matches: {overall_match_count}')
    print(f'Updated stats: {STATS_MD}')


if __name__ == '__main__':
    main()
