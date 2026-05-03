# Brand Images

Logo assets, with tooling.

## Utilities

```bash
python3 scripts/convert_images_to_png.py
python3 scripts/compress_png_images.py
```

## Open Prices

### Get the shop brands

see [openfoodfacts/open-prices/wiki/Stats](https://github.com/openfoodfacts/open-prices/wiki/Stats#top-location-brand-names)

### Generate brand-image matches

```bash
python3 scripts/generate_open_prices_brand_match_csv.py
```

### Matching status

- [Brand Match Viewer](open-prices/brand-match-viewer.md) — interactive table to explore the matched brands and logos
- [Brand Match Stats](open-prices/brand-match-stats.md) — coverage stats updated every time the match script runs

## Name Suggestion Index (NSI)

### NSI sources

- [supermarket.json](https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/supermarket.json)
- [convenience.json](https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/convenience.json)

The NSI dataset is provided by the name-suggestion-index project under the BSD-3-Clause license.

### Generate NSI brand-image matches

```bash
python3 scripts/generate_nsi_brand_match_csv.py
```

### Matching status

- [NSI Brand Match Viewer](nsi/brand-match-viewer.md) — interactive table to explore the matched NSI brands and logos
- [NSI Brand Match Stats](nsi/brand-match-stats.md) — coverage stats updated every time the match script runs

## Contribute

see [CONTRIBUTING.md](CONTRIBUTING.md)

## Contributors

<a href="https://github.com/openfoodfacts/brand-images/graphs/contributors">
  <img alt="List of contributors to this repository" src="https://contrib.rocks/image?repo=openfoodfacts/brand-images" />
</a>
