"""
Generate a CSV recap matching brand names from open_prices_brand_names.csv to images in xx/stores.
Adds columns: match_status (exact/approx/no), matched_image, and top_100_by_price (yes for top 100 by price count).

Also appends stats to docs/open_prices_brand_match_stats.md

Usage: python scripts/generate_open_prices_brand_match_csv.py
"""
import csv
import os
import re
import datetime
from unidecode import unidecode

INPUT_CSV = 'docs/open_prices_brand_names.csv'
OUTPUT_CSV = 'docs/open_prices_brand_match_recap.csv'
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
            else:
                # Approximate: allow one character difference (Levenshtein distance 1)
                for img_slug in image_slugs:
                    if abs(len(img_slug) - len(slug)) <= 1 and sum(a != b for a, b in zip(img_slug, slug)) <= 1:
                        matched_image_svg, matched_image_png = pick_formats(image_slugs[img_slug])
                        match_status = 'approx'
                        break
            row['match_status'] = match_status
            row['matched_image_svg'] = matched_image_svg
            row['matched_image_png'] = matched_image_png
            row['top_100_by_price'] = 'yes' if row.get('price_count', '').isdigit() and int(row['price_count']) >= top_100_cutoff else ''
            writer.writerow(row)

def write_stats_md(input_count, image_count, ext_counts, exact_count, approx_count, top100_exact_pct):
    stats_path = 'docs/open_prices_brand_match_stats.md'
    today = datetime.date.today().strftime('%Y-%m-%d')
    section = f"\n\n## {today}\n\n"
    section += f"- Input brands: {input_count}\n"
    # Format per-extension stats
    ext_stats = ', '.join(f"{ext}: {count}" for ext, count in sorted(ext_counts.items()))
    section += f"- Images in xx/stores: {image_count} ({ext_stats})\n"
    section += f"- Exact matches: {exact_count}\n"
    section += f"- Approx matches: {approx_count}\n"
    section += f"- % Exact matches in Top 100: {top100_exact_pct:.1f}%\n"
    # Read existing content
    if os.path.exists(stats_path):
        with open(stats_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = '# Open Prices Brand Match Stats\n\n'
    # Remove existing section for today
    import re
    content = re.sub(r'\n## ' + re.escape(today) + r'\n.*?(?=\n## |\Z)', '', content, flags=re.DOTALL)
    # Append new section
    content = content.rstrip() + section
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
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
    approx_count = sum(1 for r in out_rows if r['match_status'] == 'approx')
    top100 = [r for r in out_rows if r['top_100_by_price'] == 'yes']
    top100_exact = sum(1 for r in top100 if r['match_status'] == 'exact')
    top100_exact_pct = (top100_exact / len(top100) * 100) if top100 else 0
    write_stats_md(input_count, image_count, ext_counts, exact_count, approx_count, top100_exact_pct)
