# Changelog

## [0.2.0](https://github.com/openfoodfacts/brand-images/compare/v0.1.0...v0.2.0) (2026-05-12)


### Features

* script to compress PNG (optimize & max 400x400). Run on stores ([#12](https://github.com/openfoodfacts/brand-images/issues/12)) ([01d8c30](https://github.com/openfoodfacts/brand-images/commit/01d8c30beecf3f19971687f18c44c909c7c41fae))
* script to convert webp, jpg, jpeg to png ([#10](https://github.com/openfoodfacts/brand-images/issues/10)) ([fcae93a](https://github.com/openfoodfacts/brand-images/commit/fcae93a17e058787cfb0bea92c9fa781604d4a86))
* **Stores:** add many many more stores (from NSI convenience & supermarket JSONs) ([#29](https://github.com/openfoodfacts/brand-images/issues/29)) ([830e7ce](https://github.com/openfoodfacts/brand-images/commit/830e7ce08bb41375fb21f4c63c205aa7917ed7e7))
* **Stores:** add many more stores ([#28](https://github.com/openfoodfacts/brand-images/issues/28)) ([c7d10f4](https://github.com/openfoodfacts/brand-images/commit/c7d10f41c632440856874e1d0b8a66a47eb66f8e))
* **Stores:** add some missing "big" shops (in letters A & B) ([#11](https://github.com/openfoodfacts/brand-images/issues/11)) ([7161be5](https://github.com/openfoodfacts/brand-images/commit/7161be5b9cebf918826871e84a5d51156777ee1b))
* **Stores:** add some missing "big" shops (letters B, C, D, E) ([#14](https://github.com/openfoodfacts/brand-images/issues/14)) ([b975b38](https://github.com/openfoodfacts/brand-images/commit/b975b38f0a59a38c9929890b8c78357aed53c532))
* **Stores:** add some missing big shops (top 100) ([#25](https://github.com/openfoodfacts/brand-images/issues/25)) ([27fa383](https://github.com/openfoodfacts/brand-images/commit/27fa38360d7cd3691492b83c46bf27258abd1e5d))
* **Stores:** compare with OpenStreetMap NSI database (convenience & supermarket) ([#27](https://github.com/openfoodfacts/brand-images/issues/27)) ([99a3042](https://github.com/openfoodfacts/brand-images/commit/99a30420ff1598427ba213eb1d4aaf5efd08a11a))
* **Stores:** get missing PNGs (from existing stores) ([#36](https://github.com/openfoodfacts/brand-images/issues/36)) ([9967e47](https://github.com/openfoodfacts/brand-images/commit/9967e476c7dea1842ea8efcc9665d76da4b48ea6))
* **Stores:** NSI: fetch stores from more food JSONs ([#37](https://github.com/openfoodfacts/brand-images/issues/37)) ([8795378](https://github.com/openfoodfacts/brand-images/commit/87953786e7c8e69dc8614dc6912c2b0d64dc9a48))
* **Stores:** NSI: fetch stores from more non-food JSONs ([#38](https://github.com/openfoodfacts/brand-images/issues/38)) ([35362b9](https://github.com/openfoodfacts/brand-images/commit/35362b9dd6fbbd3be6f141d5bef68321131f8789))


### Technical

* add a new page to display the Open Prices matching table ([#23](https://github.com/openfoodfacts/brand-images/issues/23)) ([8754679](https://github.com/openfoodfacts/brand-images/commit/8754679da3cfca0c26e6c85744922578418f4bcd))
* add auto-assign Github Action ([#17](https://github.com/openfoodfacts/brand-images/issues/17)) ([ffee678](https://github.com/openfoodfacts/brand-images/commit/ffee678afbbd4147d29365a318c60febc572bb04))
* add explicit permissions on 2 Github Action workflows ([#34](https://github.com/openfoodfacts/brand-images/issues/34)) ([5d7b182](https://github.com/openfoodfacts/brand-images/commit/5d7b1826bcb1a68a3c98941d25b55d7eb56843bd))
* add global stats per xx/ folder content ([#31](https://github.com/openfoodfacts/brand-images/issues/31)) ([808c8da](https://github.com/openfoodfacts/brand-images/commit/808c8daf72d576880fb51d798cf020e085fe83b5))
* Add release manifest file with version 0.1 ([3606be9](https://github.com/openfoodfacts/brand-images/commit/3606be9bd8497d721a438dfe7315debdd28ffdb0))
* add release-please Github Action ([#19](https://github.com/openfoodfacts/brand-images/issues/19)) ([d81281d](https://github.com/openfoodfacts/brand-images/commit/d81281d652554db4e6b324d7265b67a903da3e12))
* add semantic-pr check Github Action ([#18](https://github.com/openfoodfacts/brand-images/issues/18)) ([a6e7ed6](https://github.com/openfoodfacts/brand-images/commit/a6e7ed62eed3edeeb1fd864ca7a7ee8bd11ed94b))
* Change token from RELEASE_PLEASE_TOKEN to GITHUB_TOKEN ([#40](https://github.com/openfoodfacts/brand-images/issues/40)) ([4cbc9ac](https://github.com/openfoodfacts/brand-images/commit/4cbc9acc111d013d3b8ddcd448ca63cb0f20c739))
* force mkdocs deploy (to avoid errors) ([#24](https://github.com/openfoodfacts/brand-images/issues/24)) ([a6e4b82](https://github.com/openfoodfacts/brand-images/commit/a6e4b82c8d0eac14e933dadcb0e0bb54cd6c50ca))
* Modify GitHub Actions permissions for release workflow ([badbde4](https://github.com/openfoodfacts/brand-images/commit/badbde4c16bc876b370e2acb4e8a4fb70ab491bb))
* **README:** add Content section explaining the 3 `xx/` folders ([#32](https://github.com/openfoodfacts/brand-images/issues/32)) ([70615f1](https://github.com/openfoodfacts/brand-images/commit/70615f10e3038fc5977e67a521397061a486a5d5))
* **README:** merge Context & Stats sections together ([#33](https://github.com/openfoodfacts/brand-images/issues/33)) ([45c8d63](https://github.com/openfoodfacts/brand-images/commit/45c8d6382ac0580351b3c07ab18fb96fa2621f0b))
* remove subfolders. move everything to the folders xx/stores, xx/brands & xx/agencies ([#4](https://github.com/openfoodfacts/brand-images/issues/4)) ([0708d20](https://github.com/openfoodfacts/brand-images/commit/0708d20491bbc9684b20568d36bd8fc16eabef3e))
* rename Open Prices related files. drop the approx matching. ([#22](https://github.com/openfoodfacts/brand-images/issues/22)) ([d6fef20](https://github.com/openfoodfacts/brand-images/commit/d6fef20d445802bba461e80d2b2d06d120e60c11))
* setup mkdocs. link the Open Prices stats recap table ([#21](https://github.com/openfoodfacts/brand-images/issues/21)) ([7957d8a](https://github.com/openfoodfacts/brand-images/commit/7957d8a606ef13b6e401ec28ad77af352fdc7a3b))
* **Stores:** convert non-svg images to png (~80 stores) ([#8](https://github.com/openfoodfacts/brand-images/issues/8)) ([eb20209](https://github.com/openfoodfacts/brand-images/commit/eb20209373e9346dd5331b5997d64333ecd165df))
* **Stores:** in the script that compares with OP, seperate svg & png matching ([#20](https://github.com/openfoodfacts/brand-images/issues/20)) ([c78a6e7](https://github.com/openfoodfacts/brand-images/commit/c78a6e7b30ee43735ed37bab5d40ae45bdd16ecc))
* **Stores:** rename all files (slugify). compare with Open Prices osm_brand stats ([#6](https://github.com/openfoodfacts/brand-images/issues/6)) ([183b254](https://github.com/openfoodfacts/brand-images/commit/183b254eb35e832641a5c26a9c0ab2e25778dec4))
* update README. add CONTRIBUTING. move nsi & open-prices outside of the docs folder & own README ([#30](https://github.com/openfoodfacts/brand-images/issues/30)) ([0e598b8](https://github.com/openfoodfacts/brand-images/commit/0e598b8845bed14deaa8adadb065f67f433f6571))
* update stuff following recent changes (new statuses, new NSI source categories) ([#39](https://github.com/openfoodfacts/brand-images/issues/39)) ([9ef7c61](https://github.com/openfoodfacts/brand-images/commit/9ef7c6117242592b37d067880c2bb705e19580ff))
* Update version format to include patch number ([54da210](https://github.com/openfoodfacts/brand-images/commit/54da2106cdbf152d359b049f101a95c449da999e))
* use relative urls for local display. allow sorting by price_count ([#26](https://github.com/openfoodfacts/brand-images/issues/26)) ([f980ce5](https://github.com/openfoodfacts/brand-images/commit/f980ce5f48382f18d7ed093ce3b59d5478cae34e))
