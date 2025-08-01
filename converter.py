import argparse
import os
from PIL import Image, ImageSequence
from tqdm import tqdm

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

def main():
    parser = argparse.ArgumentParser(description="Convert images from one format to another.")

    parser.add_argument(
        "input_files",
        metavar="FILE",
        type=str,
        nargs="+",
        help="One or more input image files."
    )

    parser.add_argument(
        "-f", "--format",
        type=str,
        required=True,
        choices=["jpg", "png", "webp", "gif"],
        help="The output format."
    )

    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=".",
        help="The output directory for converted files. Defaults to the current directory."
    )

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for input_file in tqdm(args.input_files, desc="Converting images"):
        success, message = convert_image(input_file, args.output_dir, args.format)
        if not success:
            print(message)

if __name__ == "__main__":
    main()
