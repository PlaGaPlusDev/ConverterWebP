from PIL import Image, ImageSequence
import easygui
from tqdm import tqdm
import os

def convert_webp_to_gif_or_png():
    # Seleccionar archivos WebP
    input_files = easygui.fileopenbox(
        title="Seleccionar archivos WebP animados/estáticos",
        default="*.webp",
        filetypes=["*.webp"],
        multiple=True
    )
    if not input_files:
        print("Operación cancelada.")
        return

    # Seleccionar carpeta destino
    output_dir = easygui.diropenbox(title="Seleccionar carpeta de guardado")
    if not output_dir:
        print("Operación cancelada.")
        return

    # Procesar cada archivo
    for input_path in tqdm(input_files, desc="Procesando"):
        try:
            filename = os.path.basename(input_path)
            base_name = os.path.splitext(filename)[0]
            
            with Image.open(input_path) as img:
                # Determinar tipo de WebP
                if img.is_animated:
                    # Configuración para GIF animado
                    output_path = os.path.join(output_dir, f"{base_name}.gif")
                    
                    frames = []
                    durations = []
                    
                    # Extraer frames con paleta optimizada
                    for frame in ImageSequence.Iterator(img):
                        # Convertir a paleta indexada con transparencia
                        frame = frame.convert("RGB")
                        palette = Image.new("P", frame.size, color=0)
                        palette.putpalette(frame.getpalette() or b"")
                        quantized = frame.quantize(method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
                        
                        frames.append(quantized)
                        durations.append(frame.info.get("duration", 100))  # Default 100ms
                    
                    # Guardar GIF optimizado
                    frames[0].save(
                        output_path,
                        format="GIF",
                        append_images=frames[1:],
                        save_all=True,
                        duration=durations,
                        loop=0,
                        disposal=2,
                        transparency=0
                    )
                    
                else:
                    # Guardar PNG estático con transparencia
                    output_path = os.path.join(output_dir, f"{base_name}.png")
                    img.convert("RGB").save(output_path, format="PNG", optimize=True)
                
                print(f"✅ Éxito: {filename}")

        except Exception as e:
            print(f"❌ Error en {filename}: {str(e)}")

    print("\nProceso completado. Revise los resultados.")

if __name__ == "__main__":
    convert_webp_to_gif_or_png()