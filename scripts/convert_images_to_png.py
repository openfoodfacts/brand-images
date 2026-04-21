"""
Convert all .webp, .jpg, and .jpeg images in a directory to .png format.
Original files are removed after successful conversion.

Usage: python scripts/convert_images_to_png.py [directory]
Default directory: xx/stores
"""
import os
import sys
from PIL import Image


def convert_images_to_png(image_dir):
    extensions = ('.webp', '.jpg', '.jpeg')
    converted = 0
    failed = 0

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(extensions):
            src_path = os.path.join(image_dir, filename)
            base = os.path.splitext(filename)[0]
            dst_path = os.path.join(image_dir, base + '.png')

            try:
                with Image.open(src_path) as img:
                    img.convert('RGBA').save(dst_path, 'PNG')
                os.remove(src_path)
                print(f'Converted: {filename} -> {base}.png')
                converted += 1
            except Exception as e:
                print(f'Failed: {filename} ({e})')
                failed += 1

    print(f'\nDone: {converted} converted, {failed} failed.')


if __name__ == '__main__':
    image_dir = sys.argv[1] if len(sys.argv) > 1 else 'xx/stores'
    convert_images_to_png(image_dir)
