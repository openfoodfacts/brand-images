# Brand Images x Name Suggestion Index (NSI)

[https://nsi.guide](https://nsi.guide)

## Get the shop brands

Current sources:

- [supermarket.json](https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/supermarket.json)
- [convenience.json](https://raw.githubusercontent.com/osmlab/name-suggestion-index/main/data/brands/shop/convenience.json)

## Generate brand-image matches

```bash
python3 scripts/generate_nsi_brand_match_csv.py
```

## Matching status

- [NSI Brand Match Viewer](brand-match-viewer.md) — interactive table to explore the matched NSI brands and logos
- [NSI Brand Match Stats](brand-match-stats.md) — coverage stats updated every time the match script runs
