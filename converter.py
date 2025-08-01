import os
from PIL import Image, ImageSequence

def convert_image(input_path, output_dir, output_format):
    try:
        filename = os.path.basename(input_path)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.{output_format}")

        with Image.open(input_path) as img:
            if img.is_animated and output_format in ["gif", "webp"]:
                # Handle animated images
                frames = []
                for frame in ImageSequence.Iterator(img):
                    # For formats that don't support RGBA, convert them
                    if output_format == 'gif':
                        frame = frame.convert('RGB')
                    else: # webp supports RGBA
                        frame = frame.copy()
                    frames.append(frame)

                if frames:
                    frames[0].save(
                        output_path,
                        save_all=True,
                        append_images=frames[1:],
                        loop=0,
                        duration=img.info.get("duration", 100),
                        quality=80, # for webp
                        allow_mixed=True # for webp
                    )
            else:
                # Handle static images or animated to static formats
                # Convert to RGB if saving as JPG
                if output_format == 'jpg':
                    img = img.convert('RGB')
                img.save(output_path, quality=95) # quality for jpg/webp

        return True, filename
    except Exception as e:
        return False, f"Error converting {filename}: {e}"
