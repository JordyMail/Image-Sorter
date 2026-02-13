import os
import shutil
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import json
from datetime import datetime

# Konfigurasi tema CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")  # Perbaikan: set_default_color_intersection -> set_default_color_theme

class ModernImageSorter:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Image Sorter Professional")
        self.window.geometry("1400x800")
        
        # Variabel
        self.source_folder = ""
        self.destination_folders = []
        self.image_files = []
        self.current_index = 0
        self.folder_count = 4
        self.button_functions = []
        self.keyboard_shortcuts = {}
        self.sorting_history = []
        self.sorted_count = 0
        
        # Warna tema
        self.colors = {
            'navy': "#1a2b4c",
            'navy_light': "#2c3e6e",
            'white': "#ffffff",
            'gray_light': "#f5f5f7",
            'gray': "#e0e0e0",
            'success': "#28a745",
            'danger': "#dc3545",
            'warning': "#ffc107"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI utama"""
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Main container
        self.main_container = ctk.CTkFrame(
            self.window,
            fg_color=self.colors['white'],
            corner_radius=0
        )
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        self.show_start_screen()
        
    def show_start_screen(self):
        """Tampilan awal aplikasi"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Start screen frame
        start_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['white'],
            corner_radius=20
        )
        start_frame.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")
        start_frame.grid_columnconfigure(0, weight=1)
        start_frame.grid_rowconfigure(1, weight=1)
        
        # Header dengan warna navy
        header_frame = ctk.CTkFrame(
            start_frame,
            fg_color=self.colors['navy'],
            height=100,
            corner_radius=15
        )
        header_frame.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Image Sorter Professional",
            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
            text_color=self.colors['white']
        )
        title_label.grid(row=0, column=0, pady=20)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Sort your images efficiently with custom categories",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color=self.colors['gray_light']
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 20))
        
        # Content frame
        content_frame = ctk.CTkFrame(
            start_frame,
            fg_color=self.colors['gray_light'],
            corner_radius=15
        )
        content_frame.grid(row=1, column=0, padx=30, pady=20, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Step indicators
        steps_frame = ctk.CTkFrame(
            content_frame,
            fg_color="transparent"
        )
        steps_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        steps_frame.grid_columnconfigure((0,1,2), weight=1)
        
        steps = [
            ("1", "Select Folder", "Choose source folder with images"),
            ("2", "Configure", "Setup folders and shortcuts"),
            ("3", "Start Sorting", "Begin organizing images")
        ]
        
        for i, (num, title, desc) in enumerate(steps):
            step_card = ctk.CTkFrame(
                steps_frame,
                fg_color=self.colors['white'],
                corner_radius=12,
                height=120
            )
            step_card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            step_card.grid_columnconfigure(0, weight=1)
            
            num_label = ctk.CTkLabel(
                step_card,
                text=num,
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=self.colors['navy'],
                width=40,
                height=40,
                corner_radius=20,
                fg_color=self.colors['gray_light']
            )
            num_label.grid(row=0, column=0, pady=(15, 5))
            
            title_label = ctk.CTkLabel(
                step_card,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=self.colors['navy']
            )
            title_label.grid(row=1, column=0, pady=5)
            
            desc_label = ctk.CTkLabel(
                step_card,
                text=desc,
                font=ctk.CTkFont(size=12),
                text_color="gray",
                wraplength=200
            )
            desc_label.grid(row=2, column=0, pady=(0, 15))
        
        # Select folder button
        self.select_btn = ctk.CTkButton(
            content_frame,
            text="Select Image Folder",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['navy'],
            hover_color=self.colors['navy_light'],
            height=60,
            corner_radius=12,
            command=self.select_source_folder
        )
        self.select_btn.grid(row=1, column=0, padx=50, pady=30, sticky="ew")
        
    def select_source_folder(self):
        """Pilih folder sumber gambar"""
        folder_selected = filedialog.askdirectory(
            title="Select Folder Containing Images"
        )
        
        if folder_selected:
            self.source_folder = folder_selected
            if self.load_images():
                self.show_configuration_screen()
            
    def load_images(self):
        """Load semua file gambar dari folder"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        self.image_files = []
        
        try:
            for file in os.listdir(self.source_folder):
                if Path(file).suffix.lower() in image_extensions:
                    self.image_files.append(os.path.join(self.source_folder, file))
            
            if not self.image_files:
                messagebox.showwarning("Warning", "No images found in the selected folder!")
                return False
            else:
                self.image_files.sort()
                return True
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load images: {str(e)}")
            return False
            
    def show_configuration_screen(self):
        """Tampilan konfigurasi folder dan tombol"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Config frame
        config_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['white'],
            corner_radius=20
        )
        config_frame.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")
        config_frame.grid_columnconfigure(0, weight=1)
        config_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            config_frame,
            text="Configuration Setup",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['navy']
        )
        header_label.grid(row=0, column=0, pady=(30, 20))
        
        # Main content area with scroll
        content_area = ctk.CTkScrollableFrame(
            config_frame,
            fg_color=self.colors['gray_light'],
            corner_radius=15
        )
        content_area.grid(row=1, column=0, padx=30, pady=20, sticky="nsew")
        content_area.grid_columnconfigure(0, weight=1)
        
        # Number of folders
        folder_count_frame = ctk.CTkFrame(
            content_area,
            fg_color=self.colors['white'],
            corner_radius=12
        )
        folder_count_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        folder_count_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            folder_count_frame,
            text="Number of Destination Folders:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['navy']
        ).grid(row=0, column=0, padx=20, pady=20)
        
        self.folder_count_var = ctk.StringVar(value="4")
        folder_spinbox = ctk.CTkEntry(
            folder_count_frame,
            textvariable=self.folder_count_var,
            width=80,
            height=40,
            font=ctk.CTkFont(size=14),
            border_color=self.colors['navy'],
            fg_color=self.colors['white']
        )
        folder_spinbox.grid(row=0, column=1, padx=20, pady=20)
        
        apply_btn = ctk.CTkButton(
            folder_count_frame,
            text="Apply",
            fg_color=self.colors['navy'],
            hover_color=self.colors['navy_light'],
            width=100,
            height=40,
            corner_radius=8,
            command=self.create_folder_inputs
        )
        apply_btn.grid(row=0, column=2, padx=20, pady=20)
        
        # Container for dynamic folder inputs
        self.folder_inputs_frame = ctk.CTkFrame(
            content_area,
            fg_color="transparent"
        )
        self.folder_inputs_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.folder_inputs_frame.grid_columnconfigure(0, weight=1)
        
        # Button configuration section
        button_config_frame = ctk.CTkFrame(
            content_area,
            fg_color=self.colors['white'],
            corner_radius=12
        )
        button_config_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        button_config_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            button_config_frame,
            text="Button Functions Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['navy']
        ).grid(row=0, column=0, padx=20, pady=(20, 10))
        
        info_text = ctk.CTkLabel(
            button_config_frame,
            text="Configure your sorting buttons below. Each button can save to one or multiple folders.",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=600
        )
        info_text.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Button functions container
        self.button_functions_frame = ctk.CTkFrame(
            button_config_frame,
            fg_color="transparent"
        )
        self.button_functions_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.button_functions_frame.grid_columnconfigure(0, weight=1)
        
        # Default button functions
        self.button_functions = []
        self.create_default_button_functions()
        
        # Add custom button
        add_button_btn = ctk.CTkButton(
            button_config_frame,
            text="+ Add Custom Button",
            fg_color=self.colors['navy_light'],
            hover_color=self.colors['navy'],
            width=200,
            height=40,
            corner_radius=8,
            command=self.add_custom_button_function
        )
        add_button_btn.grid(row=3, column=0, pady=20)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(
            config_frame,
            fg_color="transparent"
        )
        nav_frame.grid(row=2, column=0, padx=30, pady=(0, 30), sticky="ew")
        nav_frame.grid_columnconfigure((0,1), weight=1)
        
        back_btn = ctk.CTkButton(
            nav_frame,
            text="← Back",
            font=ctk.CTkFont(size=14),
            fg_color="gray",
            hover_color="darkgray",
            width=150,
            height=45,
            corner_radius=10,
            command=self.show_start_screen
        )
        back_btn.grid(row=0, column=0, padx=10)
        
        start_sorting_btn = ctk.CTkButton(
            nav_frame,
            text="Start Sorting →",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['success'],
            hover_color="#218838",
            width=150,
            height=45,
            corner_radius=10,
            command=self.start_sorting
        )
        start_sorting_btn.grid(row=0, column=1, padx=10)
        
        # Create initial folder inputs
        self.create_folder_inputs()
        
    def create_folder_inputs(self):
        """Create input fields for folder paths"""
        # Clear existing inputs
        for widget in self.folder_inputs_frame.winfo_children():
            widget.destroy()
        
        try:
            self.folder_count = int(self.folder_count_var.get())
            if self.folder_count < 1 or self.folder_count > 10:
                messagebox.showwarning("Warning", "Please enter a number between 1 and 10")
                self.folder_count = 4
                self.folder_count_var.set("4")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number")
            self.folder_count = 4
            self.folder_count_var.set("4")
        
        self.destination_folders = [""] * self.folder_count
        self.folder_paths = []
        
        # Title
        title_label = ctk.CTkLabel(
            self.folder_inputs_frame,
            text="Destination Folders:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['navy']
        )
        title_label.grid(row=0, column=0, pady=(10, 20), sticky="w")
        
        # Create input for each folder
        for i in range(self.folder_count):
            folder_frame = ctk.CTkFrame(
                self.folder_inputs_frame,
                fg_color=self.colors['white'],
                corner_radius=10,
                border_width=1,
                border_color=self.colors['gray']
            )
            folder_frame.grid(row=i+1, column=0, padx=10, pady=5, sticky="ew")
            folder_frame.grid_columnconfigure(1, weight=1)
            
            # Folder label
            folder_label = ctk.CTkLabel(
                folder_frame,
                text=f"Folder {chr(65+i)}:",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.colors['navy'],
                width=80
            )
            folder_label.grid(row=0, column=0, padx=15, pady=15)
            
            # Path entry
            path_var = ctk.StringVar()
            path_entry = ctk.CTkEntry(
                folder_frame,
                textvariable=path_var,
                font=ctk.CTkFont(size=12),
                height=40,
                border_color=self.colors['gray'],
                fg_color=self.colors['gray_light'],
                placeholder_text="Select folder location..."
            )
            path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            # Browse button
            browse_btn = ctk.CTkButton(
                folder_frame,
                text="Browse",
                font=ctk.CTkFont(size=12),
                fg_color=self.colors['navy_light'],
                hover_color=self.colors['navy'],
                width=80,
                height=35,
                corner_radius=6,
                command=lambda idx=i, var=path_var: self.browse_folder(idx, var)
            )
            browse_btn.grid(row=0, column=2, padx=15, pady=10)
            
            self.folder_paths.append((path_var, path_entry))
            
    def browse_folder(self, index, path_var):
        """Browse and select destination folder"""
        folder = filedialog.askdirectory(title=f"Select Folder {chr(65+index)} Location")
        if folder:
            path_var.set(folder)
            self.destination_folders[index] = folder
            
    def create_default_button_functions(self):
        """Create default button functions"""
        self.button_functions = []
        
        # Clear existing
        for widget in self.button_functions_frame.winfo_children():
            widget.destroy()
        
        # Single folder buttons
        default_functions = [
            ("1", "Save to Folder A", [0]),
            ("2", "Save to Folder B", [1]),
            ("3", "Save to Folder C", [2]),
            ("4", "Save to Folder D", [3]),
            ("5", "Save to Folders A & B", [0, 1]),
            ("6", "Save to Folders C & D", [2, 3]),
            ("7", "Save to All Folders", [0, 1, 2, 3]),
            ("8", "Save to Folders A, B & C", [0, 1, 2])
        ]
        
        for i, (key, desc, folders) in enumerate(default_functions):
            self.add_button_function_row(key, desc, folders)
            
    def add_button_function_row(self, key="", desc="", selected_folders=None):
        """Add a row for button function configuration"""
        if selected_folders is None:
            selected_folders = []
            
        row_frame = ctk.CTkFrame(
            self.button_functions_frame,
            fg_color=self.colors['gray_light'],
            corner_radius=8,
            height=70
        )
        row_frame.grid(row=len(self.button_functions), column=0, padx=10, pady=5, sticky="ew")
        row_frame.grid_columnconfigure(2, weight=1)
        row_frame.grid_propagate(False)
        
        # Keyboard shortcut
        key_var = ctk.StringVar(value=key)
        key_entry = ctk.CTkEntry(
            row_frame,
            textvariable=key_var,
            font=ctk.CTkFont(size=13, weight="bold"),
            width=50,
            height=35,
            border_color=self.colors['navy'],
            justify="center",
            placeholder_text="Key"
        )
        key_entry.grid(row=0, column=0, padx=(15, 5), pady=17)
        
        # Description
        desc_var = ctk.StringVar(value=desc)
        desc_entry = ctk.CTkEntry(
            row_frame,
            textvariable=desc_var,
            font=ctk.CTkFont(size=13),
            height=35,
            border_color=self.colors['gray'],
            placeholder_text="Button description"
        )
        desc_entry.grid(row=0, column=1, padx=5, pady=17, sticky="ew")
        
        # Folder selection checkboxes
        folders_frame = ctk.CTkFrame(
            row_frame,
            fg_color="transparent"
        )
        folders_frame.grid(row=0, column=2, padx=10, pady=17, sticky="ew")
        
        folder_vars = []
        for i in range(4):  # Max 4 folders for now
            var = ctk.IntVar(value=1 if i in selected_folders else 0)
            folder_vars.append(var)
            checkbox = ctk.CTkCheckBox(
                folders_frame,
                text=f"{chr(65+i)}",
                variable=var,
                font=ctk.CTkFont(size=12),
                checkbox_width=20,
                checkbox_height=20,
                border_color=self.colors['navy'],
                fg_color=self.colors['navy'],
                hover_color=self.colors['navy_light']
            )
            checkbox.grid(row=0, column=i, padx=5)
        
        # Delete button (for custom functions)
        if len(self.button_functions) >= 8:
            delete_btn = ctk.CTkButton(
                row_frame,
                text="✕",
                font=ctk.CTkFont(size=14, weight="bold"),
                width=35,
                height=35,
                fg_color=self.colors['danger'],
                hover_color="#c82333",
                corner_radius=6,
                command=lambda: self.delete_button_function(row_frame)
            )
            delete_btn.grid(row=0, column=3, padx=15, pady=17)
        
        # Store button function
        self.button_functions.append({
            'frame': row_frame,
            'key': key_var,
            'description': desc_var,
            'folder_vars': folder_vars,
            'row_index': len(self.button_functions)
        })
        
    def add_custom_button_function(self):
        """Add a custom button function"""
        if len(self.button_functions) < 12:
            next_key = str(len(self.button_functions) + 1)
            self.add_button_function_row(next_key, "Custom Function", [0])
        else:
            messagebox.showwarning("Warning", "Maximum 12 buttons allowed")
            
    def delete_button_function(self, frame):
        """Delete a custom button function"""
        for i, func in enumerate(self.button_functions):
            if func['frame'] == frame:
                frame.destroy()
                self.button_functions.pop(i)
                break
                
    def start_sorting(self):
        """Start the sorting process"""
        # Validate destination folders
        if not all(self.destination_folders):
            messagebox.showwarning("Warning", "Please select all destination folders!")
            return
            
        # Create destination folders if they don't exist
        for folder in self.destination_folders:
            if folder and not os.path.exists(folder):
                os.makedirs(folder)
                
        # Validate button functions
        if not self.button_functions:
            messagebox.showwarning("Warning", "Please configure at least one button function!")
            return
            
        # Setup keyboard shortcuts
        self.setup_keyboard_shortcuts()
        
        # Reset index and history
        self.current_index = 0
        self.sorting_history = []
        self.sorted_count = 0
        
        # Show sorting screen
        self.show_sorting_screen()
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for buttons"""
        self.keyboard_shortcuts = {}
        
        for func in self.button_functions:
            key = func['key'].get()
            if key:
                self.keyboard_shortcuts[key] = func
                
    def show_sorting_screen(self):
        """Tampilan utama untuk sorting gambar"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Main sorting layout
        self.sorting_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['white'],
            corner_radius=0
        )
        self.sorting_frame.grid(row=0, column=0, sticky="nsew")
        self.sorting_frame.grid_columnconfigure(0, weight=1)
        self.sorting_frame.grid_rowconfigure(1, weight=1)
        
        # Top bar with progress
        top_bar = ctk.CTkFrame(
            self.sorting_frame,
            fg_color=self.colors['navy'],
            height=80,
            corner_radius=0
        )
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(1, weight=1)
        
        # Progress info
        self.progress_label = ctk.CTkLabel(
            top_bar,
            text=f"Sorting Images • 0 of {len(self.image_files)}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['white']
        )
        self.progress_label.grid(row=0, column=0, padx=30, pady=20, sticky="w")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            top_bar,
            width=300,
            height=12,
            fg_color=self.colors['white'],
            progress_color=self.colors['success']
        )
        self.progress_bar.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.progress_bar.set(0)
        
        # Done button
        self.done_btn = ctk.CTkButton(
            top_bar,
            text="Finish Sorting",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['success'],
            hover_color="#218838",
            width=150,
            height=45,
            corner_radius=10,
            command=self.finish_sorting
        )
        self.done_btn.grid(row=0, column=2, padx=30, pady=20)
        
        # Main content area
        content_frame = ctk.CTkFrame(
            self.sorting_frame,
            fg_color=self.colors['gray_light'],
            corner_radius=0
        )
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Image display area (left side)
        image_frame = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors['white'],
            corner_radius=20
        )
        image_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        image_frame.grid_columnconfigure(0, weight=1)
        image_frame.grid_rowconfigure(0, weight=1)
        
        # Image container
        image_container = ctk.CTkFrame(
            image_frame,
            fg_color=self.colors['gray_light'],
            corner_radius=15
        )
        image_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        image_container.grid_columnconfigure(0, weight=1)
        image_container.grid_rowconfigure(0, weight=1)
        
        # Image label
        self.image_label = ctk.CTkLabel(
            image_container,
            text="No Image",
            font=ctk.CTkFont(size=16),
            fg_color=self.colors['white'],
            corner_radius=10
        )
        self.image_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Image info
        self.image_info_label = ctk.CTkLabel(
            image_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.image_info_label.grid(row=1, column=0, pady=(0, 20))
        
        # Navigation controls
        nav_frame = ctk.CTkFrame(
            image_frame,
            fg_color="transparent"
        )
        nav_frame.grid(row=2, column=0, pady=(0, 20))
        
        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="← Previous",
            font=ctk.CTkFont(size=13),
            fg_color="gray",
            hover_color="darkgray",
            width=120,
            height=40,
            corner_radius=8,
            command=self.previous_image
        )
        self.prev_btn.grid(row=0, column=0, padx=10)
        
        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="Next →",
            font=ctk.CTkFont(size=13),
            fg_color=self.colors['navy'],
            hover_color=self.colors['navy_light'],
            width=120,
            height=40,
            corner_radius=8,
            command=self.next_image
        )
        self.next_btn.grid(row=0, column=1, padx=10)
        
        # Buttons area (right side)
        buttons_frame = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors['white'],
            corner_radius=20
        )
        buttons_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(2, weight=1)
        
        # Buttons header
        ctk.CTkLabel(
            buttons_frame,
            text="Sorting Actions",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['navy']
        ).grid(row=0, column=0, pady=(30, 20))
        
        ctk.CTkLabel(
            buttons_frame,
            text="Press the corresponding key on your keyboard",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).grid(row=1, column=0, pady=(0, 20))
        
        # Scrollable buttons container
        buttons_container = ctk.CTkScrollableFrame(
            buttons_frame,
            fg_color="transparent"
        )
        buttons_container.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        buttons_container.grid_columnconfigure(0, weight=1)
        
        # Create sorting buttons
        self.sorting_buttons = []
        for i, func in enumerate(self.button_functions):
            btn_frame = ctk.CTkFrame(
                buttons_container,
                fg_color=self.colors['gray_light'],
                corner_radius=12
            )
            btn_frame.grid(row=i, column=0, padx=10, pady=8, sticky="ew")
            btn_frame.grid_columnconfigure(1, weight=1)
            
            # Shortcut key
            key_text = func['key'].get() or str(i+1)
            key_label = ctk.CTkLabel(
                btn_frame,
                text=key_text,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=self.colors['white'],
                width=40,
                height=40,
                corner_radius=20,
                fg_color=self.colors['navy']
            )
            key_label.grid(row=0, column=0, padx=15, pady=15)
            
            # Button description
            desc_text = func['description'].get() or f"Sort to selected folders"
            desc_label = ctk.CTkLabel(
                btn_frame,
                text=desc_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.colors['navy']
            )
            desc_label.grid(row=0, column=1, padx=10, pady=15, sticky="w")
            
            # Destination folders indicator
            folders_indicator = []
            for j, var in enumerate(func['folder_vars']):
                if var.get() == 1 and j < self.folder_count:
                    folders_indicator.append(chr(65+j))
            
            if folders_indicator:
                folder_text = f"→ Folder(s): {', '.join(folders_indicator)}"
                folder_label = ctk.CTkLabel(
                    btn_frame,
                    text=folder_text,
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                folder_label.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="w")
            
            # Bind button click
            btn_frame.bind("<Button-1>", lambda e, f=func: self.sort_image(f))
            
            # Get the folders to save to
            target_folders = []
            for j, var in enumerate(func['folder_vars']):
                if var.get() == 1 and j < len(self.destination_folders):
                    if self.destination_folders[j]:
                        target_folders.append(self.destination_folders[j])
            
            self.sorting_buttons.append({
                'frame': btn_frame,
                'key': key_text,
                'function': func,
                'target_folders': target_folders,
                'description': desc_text
            })
        
        # Bind keyboard shortcuts
        self.window.bind('<Key>', self.handle_keyboard)
        
        # Load first image
        if self.image_files:
            self.load_current_image()
        else:
            messagebox.showerror("Error", "No images to sort!")
            self.show_start_screen()
            
    def load_current_image(self):
        """Load dan tampilkan gambar saat ini"""
        try:
            if 0 <= self.current_index < len(self.image_files):
                image_path = self.image_files[self.current_index]
                
                # Load and resize image
                pil_image = Image.open(image_path)
                
                # Calculate resize ratio to fit in display area
                display_width = 700
                display_height = 500
                
                # Calculate aspect ratio
                aspect_ratio = pil_image.width / pil_image.height
                if aspect_ratio > 1:
                    new_width = display_width
                    new_height = int(display_width / aspect_ratio)
                else:
                    new_height = display_height
                    new_width = int(display_height * aspect_ratio)
                
                # Resize image
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(pil_image)
                
                # Update label
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo
                
                # Update info
                filename = os.path.basename(image_path)
                file_size = os.path.getsize(image_path) / 1024
                self.image_info_label.configure(
                    text=f"{filename} • {file_size:.1f} KB • {pil_image.width}x{pil_image.height}"
                )
                
                # Update progress
                self.progress_label.configure(
                    text=f"Sorting Images • {self.current_index + 1} of {len(self.image_files)}"
                )
                self.progress_bar.set((self.current_index + 1) / len(self.image_files))
                
                # Update navigation buttons state
                self.prev_btn.configure(state="normal" if self.current_index > 0 else "disabled")
                self.next_btn.configure(
                    state="normal" if self.current_index < len(self.image_files) - 1 else "disabled"
                )
                
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_label.configure(text=f"Error loading image: {str(e)}")
            
    def sort_image(self, button_function):
        """Sort gambar ke folder yang dituju"""
        if not self.image_files or self.current_index >= len(self.image_files):
            return
            
        try:
            image_path = self.image_files[self.current_index]
            filename = os.path.basename(image_path)
            
            # Get target folders from button function
            target_folders = []
            for j, var in enumerate(button_function['folder_vars']):
                if var.get() == 1 and j < len(self.destination_folders):
                    if self.destination_folders[j]:
                        target_folders.append(self.destination_folders[j])
            
            if not target_folders:
                messagebox.showwarning("Warning", "No destination folder selected!")
                return
                
            # Save to each target folder
            saved_count = 0
            for folder in target_folders:
                if folder and os.path.exists(folder):
                    destination = os.path.join(folder, filename)
                    
                    # If file exists, add number suffix
                    if os.path.exists(destination):
                        name, ext = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(os.path.join(folder, f"{name}_{counter}{ext}")):
                            counter += 1
                        destination = os.path.join(folder, f"{name}_{counter}{ext}")
                    
                    shutil.copy2(image_path, destination)
                    saved_count += 1
            
            if saved_count > 0:
                # Record to history
                self.sorting_history.append({
                    'image': filename,
                    'folders': [os.path.basename(f) for f in target_folders],
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
                self.sorted_count += 1
                
                # Move to next image
                self.next_image()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort image: {str(e)}")
            
    def handle_keyboard(self, event):
        """Handle keyboard shortcuts"""
        key = event.char
        
        # Check if key is a number
        if key.isdigit() or key:
            for button in self.sorting_buttons:
                if button['key'] == key:
                    self.sort_image(button['function'])
                    break
        
        # Navigation with arrow keys
        if event.keysym == 'Left':
            self.previous_image()
        elif event.keysym == 'Right':
            self.next_image()
            
    def previous_image(self):
        """Pindah ke gambar sebelumnya"""
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_image()
            
    def next_image(self):
        """Pindah ke gambar berikutnya"""
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.load_current_image()
            
    def finish_sorting(self):
        """Selesaikan proses sorting"""
        # Summary dialog
        summary = f"Sorting completed!\n\n"
        summary += f"Total images processed: {self.sorted_count}\n"
        summary += f"Total images remaining: {len(self.image_files) - self.current_index - 1}\n\n"
        summary += f"Images have been saved to {len(self.destination_folders)} folders."
        
        messagebox.showinfo("Sorting Complete", summary)
        
        # Reset and return to start screen
        self.window.unbind('<Key>')
        self.show_start_screen()
        
    def run(self):
        """Jalankan aplikasi"""
        self.window.mainloop()

if __name__ == "__main__":
    app = ModernImageSorter()
    app.run()
