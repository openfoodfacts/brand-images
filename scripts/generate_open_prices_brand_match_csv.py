"""
Generate a CSV recap matching brand names from 20260328-brand-names.csv to images in xx/stores.
Adds columns: match_status (exact/no), matched_image, and top_100_by_price (yes for top 100 by price count).

Also appends stats to open-prices/brand-match-stats.md

Usage: python scripts/generate_open_prices_brand_match_csv.py
"""
import csv
import os
import re
import datetime
from unidecode import unidecode

INPUT_CSV = 'open-prices/20260328-brand-names.csv'
OUTPUT_CSV = 'open-prices/brand-match.csv'
IMAGE_DIR = 'xx/stores'

# Django-style slugify
def slugify(value):
    value = str(value)
    value = unidecode(value).lower()
    value = re.sub(r"'", '', value)  # Remove apostrophes like Django
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = re.sub(r'-+', '-', value)
    return value.strip('-')

# Get all image filenames in xx/stores (all formats)
def get_image_files(image_dir):
    return set(os.listdir(image_dir))

def pick_formats(files):
    """Return (svg_filename, png_filename) from a list of filenames for a given slug."""
    svg = next((f for f in files if f.lower().endswith('.svg')), '')
    png = next((f for f in files if f.lower().endswith('.png')), '')
    return svg, png

def main():
    image_files = get_image_files(IMAGE_DIR)
    image_slugs = {}
    for fname in image_files:
        name, ext = os.path.splitext(fname)
        image_slugs.setdefault(name, []).append(fname)

    # Read CSV and collect price counts
    with open(INPUT_CSV, newline='', encoding='utf-8') as f:
        reader = [row for row in csv.DictReader(f) if row['brand_name'] != 'None']
    price_counts = [int(row['price_count']) for row in reader if row.get('price_count', '').isdigit()]
    top_100_cutoff = sorted(price_counts, reverse=True)[99] if len(price_counts) >= 100 else 0

    # Sort by brand_name alphabetically
    reader.sort(key=lambda r: r['brand_name'].lower())

    # Prepare output
    orig_fields = list(reader[0].keys())
    fieldnames = orig_fields[:]
    # Insert match_status before matched_image, then matched_image, then top_100_by_price at end
    for col in ('matched_image', 'matched_image_svg', 'matched_image_png', 'match_status', 'top_100_by_price'):
        if col in fieldnames:
            fieldnames.remove(col)
    insert_at = orig_fields.index('brand_name') + 1
    fieldnames.insert(insert_at, 'match_status')
    fieldnames.insert(insert_at + 1, 'matched_image_svg')
    fieldnames.insert(insert_at + 2, 'matched_image_png')
    fieldnames.append('top_100_by_price')

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            brand = row['brand_name']
            slug = slugify(brand)
            matched_image_svg = ''
            matched_image_png = ''
            match_status = 'no'
            # Exact match
            if slug in image_slugs:
                matched_image_svg, matched_image_png = pick_formats(image_slugs[slug])
                match_status = 'exact'
            row['match_status'] = match_status
            row['matched_image_svg'] = matched_image_svg
            row['matched_image_png'] = matched_image_png
            row['top_100_by_price'] = 'yes' if row.get('price_count', '').isdigit() and int(row['price_count']) >= top_100_cutoff else ''
            writer.writerow(row)

STATS_HEADER = '| Date | Input brands | Images (svg/png) | Exact matches | Match % | Match (top 100) % |\n|------|-------------|-----------------|---------------|---------|------------------|\n'

def write_stats_md(input_count, image_count, ext_counts, exact_count, top100_exact_pct):
    stats_path = 'open-prices/brand-match-stats.md'
    today = datetime.date.today().strftime('%Y-%m-%d')
    svg_count = ext_counts.get('svg', 0)
    png_count = ext_counts.get('png', 0)
    match_pct = (exact_count / input_count * 100) if input_count else 0
    new_row = f'| {today} | {input_count} | {image_count} ({svg_count} svg / {png_count} png) | {exact_count} | {match_pct:.1f}% | {top100_exact_pct:.1f}% |\n'

    intro = (
        '# Open Prices Brand Match Stats\n\n'
        'Every time we run the brand match script, we update this file with the latest stats on how many brands from '
        '`20260328-brand-names.csv` have exact matches in the `xx/stores` images.\n\n'
    )

    if os.path.exists(stats_path):
        with open(stats_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Extract existing table rows (skip header and separator lines), normalize legacy shapes.
        rows = []
        for line in content.splitlines():
            if not line.startswith('|') or line.startswith('| Date') or line.startswith('|---'):
                continue
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            # Current shape: Date, Input, Images, Exact, Match%, Top100%
            if len(cells) == 6:
                rows.append('| ' + ' | '.join(cells) + ' |\n')
                continue
            # Older shape: Date, Input, Images, Exact, Top100%
            if len(cells) == 5:
                input_val = cells[1]
                exact_val = cells[3]
                if input_val.isdigit() and exact_val.isdigit() and int(input_val) > 0:
                    legacy_match_pct = f"{(int(exact_val) / int(input_val) * 100):.1f}%"
                else:
                    legacy_match_pct = ''
                upgraded = [cells[0], cells[1], cells[2], cells[3], legacy_match_pct, cells[4]]
                rows.append('| ' + ' | '.join(upgraded) + ' |\n')
                continue
            # Legacy shape: Date, Input, Images, Exact, Approx, Top100%
            if len(cells) == 7:
                upgraded = [cells[0], cells[1], cells[2], cells[3], cells[5], cells[6]]
                rows.append('| ' + ' | '.join(upgraded) + ' |\n')
        # Remove today's row if it already exists (re-run same day)
        rows = [r for r in rows if not r.startswith(f'| {today} ')]
    else:
        rows = []

    # Most recent first: prepend new row
    rows.insert(0, new_row)

    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write(intro + STATS_HEADER + ''.join(rows))

if __name__ == '__main__':
    print("Generating brand match CSV and updating stats...")
    # Count input brands
    with open(INPUT_CSV, newline='', encoding='utf-8') as f:
        reader = [row for row in csv.DictReader(f) if row['brand_name'] != 'None']
    input_count = len(reader)
    # Count images and per-extension stats
    image_files = os.listdir(IMAGE_DIR)
    image_count = len(image_files)
    ext_counts = {}
    for fname in image_files:
        ext = os.path.splitext(fname)[1].lower().lstrip('.')
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
    # Run main to generate CSV and collect match stats
    main()
    # Read output for stats
    with open(OUTPUT_CSV, newline='', encoding='utf-8') as f:
        out_rows = list(csv.DictReader(f))
    exact_count = sum(1 for r in out_rows if r['match_status'] == 'exact')
    top100 = [r for r in out_rows if r['top_100_by_price'] == 'yes']
    top100_exact = sum(1 for r in top100 if r['match_status'] == 'exact')
    top100_exact_pct = (top100_exact / len(top100) * 100) if top100 else 0
    write_stats_md(input_count, image_count, ext_counts, exact_count, top100_exact_pct)
    print("Done.")
