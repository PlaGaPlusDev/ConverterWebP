import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip

def convert_video(input_file, output_format):
    output_file = input_file.replace(input_format, output_format)
    video = VideoFileClip(input_file)
    video.write_videofile(output_file)
    print(f"Converted {input_file} to {output_format}")

def convert_audio(input_file, output_format):
    output_file = input_file.replace(input_format, output_format)
    audio = AudioFileClip(input_file)
    audio.write_audiofile(output_file)
    print(f"Converted {input_file} to {output_format}")

def convert_image(input_file, output_format):
    output_file = input_file.replace(input_format, output_format)
    clip = ImageClip(input_file)
    clip.set_duration(1).write_videofile(output_file)
    print(f"Converted {input_file} to {output_format}")

root = tk.Tk()
root.title("Media Converter")

input_format = tk.StringVar()
output_format = tk.StringVar()

input_file_label = tk.Label(root, text="Select input file:")
input_file_label.pack()
input_file_button = tk.Button(root, text="Browse", command=lambda: input_file_button.config(text=filedialog.askopenfilename()))
input_file_button.pack()

input_format.set(".mp4")
output_format.set(".avi")

input_format_label = tk.Label(root, text="Input format:")
input_format_label.pack()
input_format_menu = tk.OptionMenu(root, input_format, ".mp4", ".mov", ".avi", ".webm", ".gif")
input_format_menu.pack()

output_format_label = tk.Label(root, text="Output format:")
output_format_label.pack()
output_format_menu = tk.OptionMenu(root, output_format, ".mp4", ".mov", ".avi", ".webm", ".gif")
output_format_menu.pack()

convert_button = tk.Button(root, text="Convert", command=lambda: convert_media(input_file_button.cget("text"), input_format.get(), output_format.get()))
convert_button.pack()

def convert_media(input_file, input_format, output_format):
    if input_file:
        if input_file.lower().endswith(input_format.lower()):
            if "video" in input_format.lower():
                convert_video(input_file, output_format)
            elif "audio" in input_format.lower():
                convert_audio(input_file, output_format)
            elif "image" in input_format.lower():
                convert_image(input_file, output_format)
        else:
            print("Input file format does not match the selected input format.")

root.mainloop()