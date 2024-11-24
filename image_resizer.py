from PIL import Image
import os

def resize_image_by_dimensions(img_path, target_width=None, target_height=None):
    """Resize an image by width or height, maintaining aspect ratio."""
    img = Image.open(img_path)
    if target_width and not target_height:
        ratio = target_width / img.width
        new_size = (target_width, int(img.height * ratio))
    elif target_height and not target_width:
        ratio = target_height / img.height
        new_size = (int(img.width * ratio), target_height)
    else:
        raise ValueError("Specify either target_width or target_height, not both.")
    return img.resize(new_size, Image.ANTIALIAS)

def resize_image_by_filesize(img_path, target_size_kb, output_path):
    """Resize an image to be under the target file size (KB), maintaining aspect ratio."""
    img = Image.open(img_path)
    quality = 95  # Start with high quality
    while True:
        img.save(output_path, "JPEG", quality=quality)
        if os.path.getsize(output_path) / 1024 <= target_size_kb or quality < 10:
            break
        quality -= 5  # Gradually reduce quality to lower the file size
    return Image.open(output_path)

def resize_file(img_path, output_path, mode, **kwargs):
    """
    Resize an image file based on the specified mode.

    Modes:
        - 'dimensions': Resize by width or height (use target_width or target_height in kwargs).
        - 'filesize': Resize to fit under a file size limit (use target_size_kb in kwargs).
    """
    try:
        if mode == 'dimensions':
            target_width = kwargs.get('target_width')
            target_height = kwargs.get('target_height')
            img = resize_image_by_dimensions(img_path, target_width, target_height)
            img.save(output_path)
            print(f"Resized {img_path} -> {output_path}")
        elif mode == 'filesize':
            target_size_kb = kwargs.get('target_size_kb')
            resize_image_by_filesize(img_path, target_size_kb, output_path)
            print(f"Resized {img_path} -> {output_path} under {target_size_kb} KB")
        else:
            raise ValueError("Invalid mode. Use 'dimensions' or 'filesize'.")
    except Exception as e:
        print(f"Error resizing {img_path}: {e}")

# Example usage:
# Resize to width 800px, maintaining aspect ratio
resize_file('/path/to/image.jpg', '/path/to/resized_image.jpg', mode='dimensions', target_width=800)

# Resize to fit under 500 KB
resize_file('/path/to/image.jpg', '/path/to/resized_image.jpg', mode='filesize', target_size_kb=500)
