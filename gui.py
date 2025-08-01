import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import os
from converter import convert_image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image Converter")
        self.geometry("800x600")

        # --- Configure grid layout (2x2) ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0) # Settings panel should not expand
        self.grid_rowconfigure(0, weight=0) # Top frame should not expand
        self.grid_rowconfigure(1, weight=1) # Middle frame should expand
        self.grid_rowconfigure(2, weight=0) # Bottom frame should not expand


        # --- Data ---
        self.files = {} # Using a dictionary to store file info and settings

        # --- Main Frames ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=1, column=1, padx=10, pady=0, sticky="ns")


        # --- Top Frame Widgets ---
        self.add_files_button = ctk.CTkButton(self.top_frame, text="Add Files", command=self.add_files)
        self.add_files_button.pack(side="left", padx=5, pady=5)

        self.clear_button = ctk.CTkButton(self.top_frame, text="Clear Files", command=self.clear_files)
        self.clear_button.pack(side="right", padx=5, pady=5)

        # --- Settings Frame Widgets ---
        self.settings_label = ctk.CTkLabel(self.settings_frame, text="Settings for selected file:")
        self.settings_label.pack(padx=10, pady=10)

        self.output_format_label = ctk.CTkLabel(self.settings_frame, text="Output Format:")
        self.output_format_label.pack(padx=10, pady=5)
        self.output_format_menu = ctk.CTkOptionMenu(self.settings_frame, values=["jpg", "png", "webp", "gif"], command=lambda val: self.update_setting("format", val))
        self.output_format_menu.pack(padx=10, pady=5)

        # Compression
        self.compression_label = ctk.CTkLabel(self.settings_frame, text="Compression (1-100):")
        self.compression_slider = ctk.CTkSlider(self.settings_frame, from_=1, to=100, command=lambda value: self.update_setting("compression", value))
        self.compression_entry = ctk.CTkEntry(self.settings_frame, width=50)

        # FPS
        self.fps_label = ctk.CTkLabel(self.settings_frame, text="FPS (1-60):")
        self.fps_slider = ctk.CTkSlider(self.settings_frame, from_=1, to=60, command=lambda value: self.update_setting("fps", value))
        self.fps_entry = ctk.CTkEntry(self.settings_frame, width=50)


        # --- Middle Frame Widgets (inside main_frame) ---
        self.tree = ttk.Treeview(self.main_frame, columns=("name", "path", "format", "settings"), show="headings")
        self.tree.heading("name", text="File Name")
        self.tree.heading("path", text="File Path")
        self.tree.heading("format", text="Output Format")
        self.tree.heading("settings", text="Settings")
        self.tree.grid(row=0, column=0, fill="both", padx=5, pady=5, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_file_select)
        self.toggle_settings_controls() # Initially hide all


        # --- Bottom Frame Widgets ---
        self.output_dir_button = ctk.CTkButton(self.bottom_frame, text="Select Output Directory", command=self.select_output_dir)
        self.output_dir_button.grid(row=0, column=0, padx=5, pady=5)

        self.output_dir_label = ctk.CTkLabel(self.bottom_frame, text=f"Output: {os.getcwd()}")
        self.output_dir_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.convert_button = ctk.CTkButton(self.bottom_frame, text="Convert", command=self.convert_images)
        self.convert_button.grid(row=0, column=3, padx=5, pady=5)

        self.progress_bar = ctk.CTkProgressBar(self.bottom_frame, orientation="horizontal")
        self.progress_bar.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.progress_bar.set(0)

        # --- Variables ---
        self.output_dir = os.getcwd()

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=(("Image Files", "*.jpg *.jpeg *.png *.gif *.webp"), ("All files", "*.*"))
        )
        for f in files:
            if f not in self.files:
                file_name = os.path.basename(f)
                output_format = "png" # Default format
                self.files[f] = {"format": output_format, "compression": 95, "fps": 24}
                self.tree.insert("", "end", iid=f, values=(file_name, f, output_format, "Comp: 95"))

    def clear_files(self):
        self.files.clear()
        for i in self.tree.get_children():
            self.tree.delete(i)

    def on_file_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            selected_file = selected_items[0]
            settings = self.files.get(selected_file)
            if settings:
                self.output_format_menu.set(settings["format"])
                self.compression_slider.set(settings["compression"])
                self.compression_entry.delete(0, "end")
                self.compression_entry.insert(0, str(settings["compression"]))
                self.fps_slider.set(settings["fps"])
                self.fps_entry.delete(0, "end")
                self.fps_entry.insert(0, str(settings["fps"]))
                self.toggle_settings_controls()

    def update_setting(self, setting_name, value):
        selected_items = self.tree.selection()
        if selected_items:
            selected_file = selected_items[0]
            if selected_file in self.files:
                if setting_name == "format":
                    self.files[selected_file]["format"] = value
                elif setting_name == "compression":
                    self.files[selected_file]["compression"] = int(value)
                    self.compression_entry.delete(0, "end")
                    self.compression_entry.insert(0, str(int(value)))
                elif setting_name == "fps":
                    self.files[selected_file]["fps"] = int(value)
                    self.fps_entry.delete(0, "end")
                    self.fps_entry.insert(0, str(int(value)))

                self.update_treeview_settings(selected_file)
                self.toggle_settings_controls()

    def toggle_settings_controls(self):
        selected_items = self.tree.selection()
        if not selected_items:
            self.compression_label.pack_forget()
            self.compression_slider.pack_forget()
            self.compression_entry.pack_forget()
            self.fps_label.pack_forget()
            self.fps_slider.pack_forget()
            self.fps_entry.pack_forget()
            return

        selected_file = selected_items[0]
        settings = self.files.get(selected_file)
        if settings:
            output_format = settings["format"]
            # Compression
            if output_format in ["jpg", "png"]:
                self.compression_label.pack(padx=10, pady=5)
                self.compression_slider.pack(padx=10, pady=5)
                self.compression_entry.pack(padx=10, pady=5)
            else:
                self.compression_label.pack_forget()
                self.compression_slider.pack_forget()
                self.compression_entry.pack_forget()
            # FPS
            if output_format in ["gif", "webp"]:
                self.fps_label.pack(padx=10, pady=5)
                self.fps_slider.pack(padx=10, pady=5)
                self.fps_entry.pack(padx=10, pady=5)
            else:
                self.fps_label.pack_forget()
                self.fps_slider.pack_forget()
                self.fps_entry.pack_forget()

    def update_treeview_settings(self, file_path):
        settings = self.files.get(file_path)
        if settings:
            settings_str = ""
            output_format = settings["format"]
            if output_format in ["jpg", "png"]:
                settings_str = f"Comp: {settings['compression']}"
            elif output_format in ["gif", "webp"]:
                settings_str = f"FPS: {settings['fps']}"

            self.tree.item(file_path, values=(os.path.basename(file_path), file_path, output_format, settings_str))

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_dir_label.configure(text=f"Output: {self.output_dir}")

    def convert_images(self):
        total_files = len(self.tree.get_children())
        if total_files == 0:
            messagebox.showinfo("No files", "Please add files to convert.")
            return

        errors = []
        for i, file_path in enumerate(self.tree.get_children()):
            settings = self.files.get(file_path)
            if settings:
                success, message = convert_image(file_path, self.output_dir, settings["format"], settings["compression"], settings["fps"])
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
