# Brand Images

Logo assets, with tooling.

## Utilities

```bash
python3 scripts/convert_images_to_png.py
python3 scripts/compress_png_images.py
```

## Open Prices

### Get the shop brands

see https://github.com/openfoodfacts/open-prices/wiki/Stats#top-location-brand-names

### Generate brand-image matches

```bash
python3 scripts/generate_open_prices_brand_match_csv.py
```

### Matching status

- [Brand Match Viewer](open-prices/brand-match-viewer.md) — interactive table to explore the matched brands and logos
- [Brand Match Stats](open-prices/brand-match-stats.md) — coverage stats updated every time the match script runs

### Updating the matches

```bash
python3 scripts/generate_open_prices_brand_match_csv.py
```

## Name Suggestion Index (NSI)

### NSI sources

- https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/supermarket.json
- https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/convenience.json

The NSI dataset is provided by the name-suggestion-index project under the BSD-3-Clause license.

### Generate NSI brand-image matches

```bash
python3 scripts/generate_nsi_brand_match_csv.py
```

### Matching status

- [NSI Brand Match Viewer](nsi/brand-match-viewer.md) — interactive table to explore the matched NSI brands and logos
- [NSI Brand Match Stats](nsi/brand-match-stats.md) — coverage stats updated every time the match script runs

## Development

### Preview the docs locally

```bash
pip install mkdocs mkdocs-material
cp README.md docs/index.md
python -m mkdocs serve --dev-addr 127.0.0.1:8765
```

Open http://127.0.0.1:8765/ in your browser.
