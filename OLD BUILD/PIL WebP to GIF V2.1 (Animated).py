from PIL import Image
import easygui

def convert_webp_to_gif():
    #Seleccionar archivo
        input_file = easygui.fileopenbox(default="*.webp", filetypes=["*.webp"])
        if not input_file:
            print("No se seleccionó nada.")
            return input_file
        #Seleccionar Salida
        output_file = easygui.filesavebox(default=input_file.replace(".webp", ".gif"), filetypes=["*.gif"])
        if not output_file:
            print("No se selecciono ruta de salida.")
            return

        try:
        #Abrir WebP
            img = Image.open(input_file)
            if not img.is_animated:
                print("La imagen WebP proporcionada no esta animada")
                return input_file

            frames = []
            last_frame = img.n_frames - 1
            for i in range(img.n_frames):
                img.seek(i)
                frames.append(img.convert("RGB"))
        #Guardar a GIF
            
                frames[0].save(output_file, format="GIF", append_images=frames[1:],
                   save_all=True, duration=img.info["duration"],
                   loop=0)

        except EOFError:
                    pass
        print("La conversión se completo.")

#Ejecutar
convert_webp_to_gif()