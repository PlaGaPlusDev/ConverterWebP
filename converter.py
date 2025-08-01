import os
from PIL import Image, ImageSequence

def convert_image(input_path, output_dir, output_format, compression=95, fps=24):
    try:
        filename = os.path.basename(input_path)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.{output_format}")

        with Image.open(input_path) as img:
            save_params = {}
            if output_format == 'jpg':
                save_params['quality'] = compression
                img = img.convert('RGB') # JPG doesn't support alpha
            elif output_format == 'png':
                save_params['compress_level'] = int((100 - compression) / 10) # PIL uses 0-9 for PNG
            elif output_format == 'webp':
                save_params['quality'] = compression

            if img.is_animated and output_format in ["gif", "webp"]:
                frames = []
                for frame in ImageSequence.Iterator(img):
                    if output_format == 'gif':
                        frame = frame.convert('RGB')
                    else:
                        frame = frame.copy()
                    frames.append(frame)

                if frames:
                    save_params['save_all'] = True
                    save_params['append_images'] = frames[1:]
                    save_params['loop'] = 0
                    save_params['duration'] = 1000 // fps
                    if output_format == 'webp':
                         save_params['allow_mixed'] = True

                    frames[0].save(output_path, **save_params)
            else:
                img.save(output_path, **save_params)

        return True, filename
    except Exception as e:
        return False, f"Error converting {filename}: {e}"
