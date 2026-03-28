"""
Generate a CSV recap matching brand names from open_prices_brand_names.csv to images in xx/stores.
Adds columns: match_status (exact/approx/no), matched_image, and top_100_by_price (yes for top 100 by price count).

How to run: python scripts/generate_brand_match_csv.py
"""
import csv
import os
import re
from unidecode import unidecode

INPUT_CSV = 'docs/open_prices_brand_names.csv'
OUTPUT_CSV = 'docs/open_prices_brand_match_recap.csv'
IMAGE_DIR = 'xx/stores'

# Django-style slugify
def slugify(value):
    value = str(value)
    value = unidecode(value).lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = re.sub(r'-+', '-', value)
    return value.strip('-')

# Get all image filenames in xx/stores (all formats)
def get_image_files(image_dir):
    return set(os.listdir(image_dir))

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
    if 'matched_image' in fieldnames:
        fieldnames.remove('matched_image')
    if 'match_status' in fieldnames:
        fieldnames.remove('match_status')
    if 'top_100_by_price' in fieldnames:
        fieldnames.remove('top_100_by_price')
    insert_at = orig_fields.index('brand_name') + 1
    fieldnames.insert(insert_at, 'match_status')
    fieldnames.insert(insert_at + 1, 'matched_image')
    fieldnames.append('top_100_by_price')

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            brand = row['brand_name']
            slug = slugify(brand)
            matched_image = ''
            match_status = 'no'
            # Exact match
            if slug in image_slugs:
                matched_image = image_slugs[slug][0]
                match_status = 'exact'
            else:
                # Approximate: allow one character difference (Levenshtein distance 1)
                for img_slug in image_slugs:
                    if abs(len(img_slug) - len(slug)) <= 1 and sum(a != b for a, b in zip(img_slug, slug)) <= 1:
                        matched_image = image_slugs[img_slug][0]
                        match_status = 'approx'
                        break
            row['match_status'] = match_status
            row['matched_image'] = matched_image
            row['top_100_by_price'] = 'yes' if row.get('price_count', '').isdigit() and int(row['price_count']) >= top_100_cutoff else ''
            writer.writerow(row)

if __name__ == '__main__':
    main()
