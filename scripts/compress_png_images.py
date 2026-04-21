"""
Resize and compress all .png images in a directory to a maximum of 400x400px.
Aspect ratio is preserved. Files are overwritten in-place.
SVG files are not touched.

Usage: python scripts/compress_png_images.py [directory]
Default directory: xx/stores
"""
import os
import sys
from PIL import Image, PngImagePlugin

# Allow large text chunks in PNG metadata
PngImagePlugin.MAX_TEXT_CHUNK = 100 * (1024 ** 2)

MAX_SIZE = (400, 400)


def compress_png_images(image_dir):
    changed = 0
    unchanged = 0
    failed = 0

    for filename in os.listdir(image_dir):
        if not filename.lower().endswith('.png'):
            continue

        filepath = os.path.join(image_dir, filename)
        size_before = os.path.getsize(filepath)

        try:
            with Image.open(filepath) as img:
                original_dims = img.size
                img.thumbnail(MAX_SIZE)
                img.save(filepath, 'PNG', optimize=True)

            size_after = os.path.getsize(filepath)
            diff_kb = (size_after - size_before) / 1024
            pct = ((size_after - size_before) / size_before * 100) if size_before else 0
            if size_after == size_before:
                unchanged += 1
            else:
                print(
                    f'{filename}: {original_dims[0]}x{original_dims[1]} -> {img.size[0]}x{img.size[1]}, '
                    f'{size_before / 1024:.1f}KB -> {size_after / 1024:.1f}KB ({diff_kb:+.1f}KB, {pct:+.1f}%)'
                )
                changed += 1
        except Exception as e:
            print(f'Failed: {filename} ({e})')
            failed += 1

    total = changed + unchanged + failed
    print(f'\nDone: {total} processed ({changed} changed, {unchanged} unchanged, {failed} failed).')


if __name__ == '__main__':
    image_dir = sys.argv[1] if len(sys.argv) > 1 else 'xx/stores'
    compress_png_images(image_dir)
