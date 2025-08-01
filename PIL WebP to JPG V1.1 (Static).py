from PIL import Image
import easygui
def convert_webp_to_gif():
    #Seleccionar archivo
        input_file = easygui.fileopenbox(default="*.webp", filetypes=["*.webp"])
        if not input_file:
            print("No se seleccionó nada.")
            return input_file
        #Seleccionar Salida
        output_file = easygui.filesavebox(default=input_file.replace(".webp", ".jpg"), filetypes=["*.jpg"])
        if not output_file:
            print("No se selecciono ruta de salida.")
            return

        try:
            img = Image.open(input_file).convert("RGB")
            img.save(output_file, 'jpg')
            print("La conversion se completo.")
        except IOError:
            print("No se pudo convertir.")
#Ejecutar
convert_webp_to_gif()