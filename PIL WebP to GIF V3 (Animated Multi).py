from PIL import Image
import easygui
from tqdm import tqdm

def convert_webp_to_gif_or_png():
    # Seleccionar archivos
    input_files = easygui.fileopenbox(default="*.webp", filetypes=["*.webp"])
    if not input_files:
        print("No se seleccionó nada.")
        return

    # Seleccionar Salida
    output_file = easygui.filesavebox(default=input_files[0].replace(".webp", ".gif"), filetypes=["*.gif"])
    if not output_file:
        print("No se selecciono ruta de salida.")
        return

    for input_file in tqdm(input_files):
        try:
            # Abrir WebP
            img = Image.open(input_file)
            if img.is_animated:
                # Convertir WebP animado a GIF
                frames = []
                last_frame = img.n_frames - 1
                for i in range(img.n_frames):
                    img.seek(i)
                    frames.append(img.convert("RGB"))

                frames[0].save(output_file, format="GIF", append_images=frames[1:],
                               save_all=True, duration=img.info["duration"],
                               loop=0)
                print(f"La conversión de {input_file.split('/')[-1]} a GIF se completo.")
            else:
                # Convertir WebP estático a PNG
                output_file = output_file.replace(".gif", ".png")
                img.save(output_file, format="PNG")
                print(f"La conversión de {input_file.split('/')[-1]} a PNG se completo.")
        except EOFError:
            pass
        print("La conversión se completo.")

#Ejecutar
convert_webp_to_gif_or_png()