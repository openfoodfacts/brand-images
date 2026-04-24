# Brand Images

Logo assets, with tooling.

## Open Prices

### Matching status

- [Brand Match Viewer](open-prices/brand-match-viewer.md) — interactive table to explore the matched brands and logos
- [Brand Match Stats](open-prices/brand-match-stats.md) — coverage stats updated every time the match script runs

### Updating the matches

```bash
python3 scripts/convert_images_to_png.py
python3 scripts/compress_png_images.py
python3 scripts/generate_open_prices_brand_match_csv.py
```

## Development

### Preview the docs locally

```bash
pip install mkdocs mkdocs-material
cp README.md docs/index.md
python -m mkdocs serve --dev-addr 127.0.0.1:8765
```

Open http://127.0.0.1:8765/ in your browser.
