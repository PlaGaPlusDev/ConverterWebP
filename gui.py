import customtkinter as ctk
from tkinter import filedialog, Listbox, messagebox
import os
from converter import convert_image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image Converter")
        self.geometry("700x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Frames ---
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.middle_frame = ctk.CTkFrame(self)
        self.middle_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # --- Top Frame Widgets ---
        self.add_files_button = ctk.CTkButton(self.top_frame, text="Add Files", command=self.add_files)
        self.add_files_button.pack(side="left", padx=5, pady=5)

        self.output_format_label = ctk.CTkLabel(self.top_frame, text="Output Format:")
        self.output_format_label.pack(side="left", padx=5, pady=5)
        self.output_format_menu = ctk.CTkOptionMenu(self.top_frame, values=["jpg", "png", "webp", "gif"])
        self.output_format_menu.pack(side="left", padx=5, pady=5)

        self.clear_button = ctk.CTkButton(self.top_frame, text="Clear Files", command=self.clear_files)
        self.clear_button.pack(side="right", padx=5, pady=5)

        # --- Middle Frame Widgets ---
        self.file_listbox = Listbox(self.middle_frame, selectmode="extended")
        self.file_listbox.pack(expand=True, fill="both", padx=5, pady=5)

        # --- Bottom Frame Widgets ---
        self.output_dir_button = ctk.CTkButton(self.bottom_frame, text="Select Output Directory", command=self.select_output_dir)
        self.output_dir_button.pack(side="left", padx=5, pady=5)

        self.output_dir_label = ctk.CTkLabel(self.bottom_frame, text=f"Output: {os.getcwd()}")
        self.output_dir_label.pack(side="left", padx=5, pady=5)

        self.convert_button = ctk.CTkButton(self.bottom_frame, text="Convert", command=self.convert_images)
        self.convert_button.pack(side="right", padx=5, pady=5)

        self.progress_bar = ctk.CTkProgressBar(self.bottom_frame, orientation="horizontal")
        self.progress_bar.pack(side="right", padx=5, pady=5, fill="x", expand=True)
        self.progress_bar.set(0)

        # --- Variables ---
        self.file_paths = []
        self.output_dir = os.getcwd()

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=(("Image Files", "*.jpg *.jpeg *.png *.gif *.webp"), ("All files", "*.*"))
        )
        for f in files:
            if f not in self.file_paths:
                self.file_paths.append(f)
                self.file_listbox.insert("end", os.path.basename(f))

    def clear_files(self):
        self.file_paths.clear()
        self.file_listbox.delete(0, "end")

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_dir_label.configure(text=f"Output: {self.output_dir}")

    def convert_images(self):
        output_format = self.output_format_menu.get()
        total_files = len(self.file_paths)
        if total_files == 0:
            messagebox.showinfo("No files", "Please add files to convert.")
            return

        errors = []
        for i, file_path in enumerate(self.file_paths):
            success, message = convert_image(file_path, self.output_dir, output_format)
            if not success:
                errors.append(message)
            self.progress_bar.set((i + 1) / total_files)
            self.update_idletasks()

        if errors:
            messagebox.showerror("Conversion Errors", "\n".join(errors))
        else:
            messagebox.showinfo("Success", "All files converted successfully!")

        self.progress_bar.set(0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
