import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
from PIL import Image

# --- Modern Configuration (Slate & Blue Palette) ---
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("dark-blue") 

# Professional Color Palette
COLOR_BG = "#F1F5F9"        # Light gray background
COLOR_SURFACE = "#FFFFFF"   # Clean white for cards
COLOR_PRIMARY = "#0F172A"   # Dark Navy
COLOR_ACCENT = "#3B82F6"    # Bright Blue
COLOR_TEXT = "#334155"      # Dark gray text
COLOR_BORDER = "#E2E8F0"    # Subtle border

class SortirFotoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SortirPro - Smart Photo Organizer")
        self.geometry("1100x800")
        self.configure(fg_color=COLOR_BG)

        # Data Variables
        self.source_folder = ""
        self.image_files = []
        self.current_image_index = 0
        
        self.folders_data = [] 
        self.shortcuts_data = []

        # Main Container
        self.main_scroll = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent", 
            corner_radius=0
        )
        self.main_scroll.pack(fill="both", expand=True, padx=0, pady=0)

        # Start with Configuration Page
        self.init_config_page()

    # ==========================================
    # PAGE 1: CONFIGURATION (SETUP)
    # ==========================================
    def init_config_page(self):
        self.clear_frame(self.main_scroll)
        
        # Reset Important Data when returning to main menu
        self.image_files = []
        self.current_image_index = 0
        
        # --- Hero Header ---
        header_frame = ctk.CTkFrame(self.main_scroll, fg_color=COLOR_PRIMARY, height=100, corner_radius=0)
        header_frame.pack(fill="x")
        
        lbl_title = ctk.CTkLabel(
            header_frame, 
            text="Photo Sorting Configuration", 
            font=("Segoe UI", 28, "bold"), 
            text_color="white"
        )
        lbl_title.pack(pady=(25, 5))
        lbl_subtitle = ctk.CTkLabel(
            header_frame, 
            text="Set your source folder, destination folders, and keyboard shortcuts", 
            font=("Segoe UI", 14), 
            text_color="#94A3B8"
        )
        lbl_subtitle.pack(pady=(0, 25))

        # Content Container
        content_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        content_frame.pack(fill="both", padx=40, pady=20)

        # 1. Card: Select Source Folder
        self._create_section_header(content_frame, "1. Photo Source", "Select the folder containing photos to organize.")
        
        card_source = ctk.CTkFrame(content_frame, fg_color=COLOR_SURFACE, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        card_source.pack(fill="x", pady=(5, 20), ipady=10)

        inner_source = ctk.CTkFrame(card_source, fg_color="transparent")
        inner_source.pack(fill="x", padx=20, pady=10)

        self.btn_source = ctk.CTkButton(
            inner_source, 
            text="📂 Select Source Folder", 
            command=self.select_source_folder,
            fg_color=COLOR_ACCENT, 
            hover_color="#2563EB",
            font=("Segoe UI", 14, "bold"),
            height=40
        )
        self.btn_source.pack(side="left")
        
        # Display path if already exists (e.g., user returns to menu but path is still saved)
        display_path = self.source_folder if self.source_folder else "No folder selected"
        self.lbl_source_path = ctk.CTkLabel(inner_source, text=display_path, text_color="gray", font=("Consolas", 12))
        self.lbl_source_path.pack(side="left", padx=15)

        # 2. Card: Destination Folder Setup
        self._create_section_header(content_frame, "2. Destination Folders", "Create category labels and their storage locations.")

        card_dest = ctk.CTkFrame(content_frame, fg_color=COLOR_SURFACE, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        card_dest.pack(fill="x", pady=(5, 20), ipady=5)

        self.folder_container = ctk.CTkFrame(card_dest, fg_color="transparent")
        self.folder_container.pack(fill="x", padx=10, pady=10)
        
        self.folder_entries = [] 
        
        btn_add_folder = ctk.CTkButton(
            card_dest, 
            text="+ Add New Category", 
            command=self.add_folder_row,
            fg_color="transparent", 
            text_color=COLOR_ACCENT,
            border_width=1,
            border_color=COLOR_ACCENT,
            hover_color="#EFF6FF"
        )
        btn_add_folder.pack(pady=10)

        # 3. Card: Shortcut Setup
        self._create_section_header(content_frame, "3. Keyboard Shortcuts", "Map keyboard keys to destination folders.")

        card_shortcut = ctk.CTkFrame(content_frame, fg_color=COLOR_SURFACE, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        card_shortcut.pack(fill="x", pady=(5, 20), ipady=5)

        self.shortcut_container = ctk.CTkFrame(card_shortcut, fg_color="transparent")
        self.shortcut_container.pack(fill="x", padx=10, pady=10)

        self.shortcut_rows = [] 

        btn_add_shortcut = ctk.CTkButton(
            card_shortcut, 
            text="+ Add Shortcut", 
            command=self.add_shortcut_row,
            fg_color="transparent", 
            text_color=COLOR_ACCENT,
            border_width=1,
            border_color=COLOR_ACCENT,
            hover_color="#EFF6FF"
        )
        btn_add_shortcut.pack(pady=10)

        # Start Button
        self.btn_start = ctk.CTkButton(
            content_frame, 
            text="START SORTING 🚀", 
            command=self.start_sorting_process,
            font=("Segoe UI", 16, "bold"),
            height=55,
            corner_radius=27,
            fg_color=COLOR_PRIMARY, 
            hover_color="#1E293B"
        )
        self.btn_start.pack(pady=30, fill="x", padx=100)

        # Initialize initial rows (or reload if data already exists - simple logic: reset first)
        self.add_folder_row()
        self.add_shortcut_row()

    def _create_section_header(self, parent, title, subtitle):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=(10,0))
        ctk.CTkLabel(f, text=title, font=("Segoe UI", 18, "bold"), text_color=COLOR_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(f, text=subtitle, font=("Segoe UI", 12), text_color="gray").pack(anchor="w")

    def add_folder_row(self):
        row_frame = ctk.CTkFrame(self.folder_container, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)
        
        idx = len(self.folder_entries) + 1
        ctk.CTkLabel(row_frame, text=f"#{idx}", width=30, text_color="gray").pack(side="left")

        entry_name = ctk.CTkEntry(row_frame, placeholder_text="Label Name (e.g., Vacation)", width=200, height=35)
        entry_name.pack(side="left", padx=5)
        
        entry_path = ctk.CTkEntry(row_frame, placeholder_text="Destination Folder Path...", width=300, height=35)
        entry_path.pack(side="left", padx=5, expand=True, fill="x")
        
        def browse_dest():
            d = filedialog.askdirectory()
            if d:
                entry_path.delete(0, "end")
                entry_path.insert(0, d)

        btn_browse = ctk.CTkButton(row_frame, text="📂", width=40, height=35, command=browse_dest, fg_color="#CBD5E1", hover_color="#94A3B8", text_color="black")
        btn_browse.pack(side="left", padx=5)

        self.folder_entries.append({"name": entry_name, "path": entry_path, "frame": row_frame})

    def add_shortcut_row(self):
        row_frame = ctk.CTkFrame(self.shortcut_container, fg_color="#F8FAFC", corner_radius=6, border_width=1, border_color="#E2E8F0")
        row_frame.pack(fill="x", pady=5, padx=5, ipady=5)
        
        left_sec = ctk.CTkFrame(row_frame, fg_color="transparent")
        left_sec.pack(side="left", padx=10)
        
        ctk.CTkLabel(left_sec, text="Press Key:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        entry_key = ctk.CTkEntry(left_sec, width=60, placeholder_text="A", font=("Consolas", 14, "bold"), justify="center")
        entry_key.pack()
        
        divider = ctk.CTkFrame(row_frame, width=1, height=40, fg_color="#CBD5E1")
        divider.pack(side="left", padx=10)

        right_sec = ctk.CTkFrame(row_frame, fg_color="transparent")
        right_sec.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(right_sec, text="Copy to Folder:", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 5))
        
        check_container = ctk.CTkFrame(right_sec, fg_color="transparent")
        check_container.pack(fill="x")
        
        self.shortcut_rows.append({"key": entry_key, "frame": check_container, "checks": []})
        self.refresh_shortcut_options()

    def refresh_shortcut_options(self):
        current_folders = [e["name"].get() for e in self.folder_entries]
        
        for row in self.shortcut_rows:
            for widget in row["frame"].winfo_children():
                widget.destroy()
            
            row["checks"] = []
            for i, folder_name in enumerate(current_folders):
                name_display = folder_name if folder_name else f"Folder {i+1}"
                chk = ctk.CTkCheckBox(
                    row["frame"], 
                    text=name_display, 
                    fg_color=COLOR_ACCENT,
                    font=("Segoe UI", 12),
                    checkbox_height=20, checkbox_width=20
                )
                chk.pack(side="left", padx=10)
                row["checks"].append(chk)

    def select_source_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.source_folder = path
            self.lbl_source_path.configure(text=path, text_color=COLOR_TEXT)

    # ==========================================
    # START LOGIC & VALIDATION
    # ==========================================
    def start_sorting_process(self):
        if not self.source_folder:
            messagebox.showerror("Error", "Please select a source photo folder first!")
            return

        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
        self.image_files = [f for f in os.listdir(self.source_folder) if f.lower().endswith(valid_extensions)]
        self.image_files.sort()
        
        if not self.image_files:
            messagebox.showerror("Error", "Folder is empty or no images found!")
            return

        self.folders_data = []
        for entry in self.folder_entries:
            name = entry["name"].get()
            path = entry["path"].get()
            if name and path:
                full_path = os.path.join(path, name)
                if not os.path.exists(full_path):
                    try:
                        os.makedirs(full_path)
                    except OSError as e:
                        messagebox.showerror("Error", f"Failed to create folder {name}: {e}")
                        return
                self.folders_data.append({"name": name, "path": full_path})
        
        if not self.folders_data:
            messagebox.showerror("Error", "Create at least 1 destination folder!")
            return

        self.shortcuts_data = []
        for row in self.shortcut_rows:
            key = row["key"].get().lower()
            selected_indices = [i for i, chk in enumerate(row["checks"]) if chk.get() == 1]
            
            if key and selected_indices:
                valid_indices = [i for i in selected_indices if i < len(self.folders_data)]
                if valid_indices:
                    self.shortcuts_data.append({"key": key, "targets": valid_indices})

        if not self.shortcuts_data:
            messagebox.showerror("Error", "Set at least 1 shortcut key!")
            return

        self.init_sorting_page()

    # ==========================================
    # PAGE 2: SORTING (DESIGN OVERHAUL)
    # ==========================================
    def init_sorting_page(self):
        self.clear_frame(self.main_scroll)
        self.current_image_index = 0
        self.bind("<Key>", self.handle_keypress)
        
        # Grid Layout
        container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left Column: Image Viewer
        left_col = ctk.CTkFrame(container, fg_color="#18181b", corner_radius=15)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # File Info Header
        self.info_frame = ctk.CTkFrame(left_col, fg_color="#27272a", height=50, corner_radius=10)
        self.info_frame.pack(fill="x", padx=10, pady=10)
        
        self.file_counter = ctk.CTkLabel(self.info_frame, text="1 / 100", font=("Consolas", 14, "bold"), text_color="#E2E8F0")
        self.file_counter.pack(side="right", padx=15)
        
        self.file_name_lbl = ctk.CTkLabel(self.info_frame, text="Filename.jpg", font=("Segoe UI", 14), text_color="white")
        self.file_name_lbl.pack(side="left", padx=15)

        # Image Label
        self.image_label = ctk.CTkLabel(left_col, text="", text_color="gray")
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Toast Overlay
        self.toast_label = ctk.CTkLabel(
            left_col, 
            text="", 
            fg_color=COLOR_ACCENT, 
            text_color="white", 
            corner_radius=20,
            font=("Segoe UI", 14, "bold"),
            width=200, height=40
        )

        # Right Column: Controls & Shortcut
        right_col = ctk.CTkFrame(container, fg_color="transparent", width=300)
        right_col.pack(side="right", fill="y")

        # Navigation
        nav_card = ctk.CTkFrame(right_col, fg_color=COLOR_SURFACE, corner_radius=10)
        nav_card.pack(fill="x", pady=(0, 20), ipady=10)
        
        ctk.CTkLabel(nav_card, text="Navigation", font=("Segoe UI", 12, "bold"), text_color="gray").pack(pady=5)
        nav_btns = ctk.CTkFrame(nav_card, fg_color="transparent")
        nav_btns.pack()
        
        ctk.CTkButton(nav_btns, text="← Prev", command=self.prev_image, width=80, fg_color="#E2E8F0", text_color="black", hover_color="#CBD5E1").pack(side="left", padx=5)
        ctk.CTkButton(nav_btns, text="Next →", command=self.next_image, width=80, fg_color="#E2E8F0", text_color="black", hover_color="#CBD5E1").pack(side="left", padx=5)

        # Shortcut Grid
        shortcut_card = ctk.CTkFrame(right_col, fg_color=COLOR_SURFACE, corner_radius=10)
        shortcut_card.pack(fill="both", expand=True, ipady=10)
        
        ctk.CTkLabel(shortcut_card, text="KEYBOARD SHORTCUTS", font=("Segoe UI", 14, "bold"), text_color=COLOR_PRIMARY).pack(pady=15)

        self.buttons_frame = ctk.CTkScrollableFrame(shortcut_card, fg_color="transparent")
        self.buttons_frame.pack(fill="both", expand=True, padx=10)

        for s_data in self.shortcuts_data:
            key = s_data["key"].upper()
            target_names = [self.folders_data[i]["name"] for i in s_data["targets"]]
            desc = " + ".join(target_names)
            
            btn_frame = ctk.CTkFrame(self.buttons_frame, fg_color="#F8FAFC", border_width=1, border_color="#E2E8F0", corner_radius=8)
            btn_frame.pack(fill="x", pady=5)
            
            key_container = ctk.CTkFrame(btn_frame, fg_color=COLOR_PRIMARY, width=50, height=50, corner_radius=6)
            key_container.pack(side="left", padx=5, pady=5)
            key_container.pack_propagate(False) 
            
            ctk.CTkLabel(key_container, text=key, font=("Consolas", 20, "bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
            
            info_container = ctk.CTkFrame(btn_frame, fg_color="transparent")
            info_container.pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkLabel(info_container, text="Save to:", font=("Segoe UI", 10), text_color="gray").pack(anchor="w")
            ctk.CTkLabel(info_container, text=desc, font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT, wraplength=150, justify="left").pack(anchor="w")

            btn_frame.bind("<Button-1>", lambda e, k=s_data["key"]: self.execute_sort(k))
            for child in btn_frame.winfo_children():
                for subchild in child.winfo_children():
                     subchild.bind("<Button-1>", lambda e, k=s_data["key"]: self.execute_sort(k))
                child.bind("<Button-1>", lambda e, k=s_data["key"]: self.execute_sort(k))

        self.load_image()

    def show_toast(self, message):
        self.toast_label.configure(text=f"✓ {message}")
        self.toast_label.place(relx=0.5, rely=0.9, anchor="center")
        self.after(1500, lambda: self.toast_label.place_forget())

    def load_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            file_name = self.image_files[self.current_image_index]
            file_path = os.path.join(self.source_folder, file_name)
            
            self.file_counter.configure(text=f"{self.current_image_index + 1} / {len(self.image_files)}")
            self.file_name_lbl.configure(text=file_name)
            
            try:
                img = Image.open(file_path)
                aspect_ratio = img.width / img.height
                new_height = 600
                new_width = int(new_height * aspect_ratio)
                
                my_image = ctk.CTkImage(light_image=img, dark_image=img, size=(new_width, new_height))
                self.image_label.configure(image=my_image, text="")
            except Exception as e:
                self.image_label.configure(image=None, text=f"Error loading: {e}")
        else:
            self.end_session()

    def handle_keypress(self, event):
        key = event.char.lower()
        for s in self.shortcuts_data:
            if s["key"] == key:
                self.execute_sort(key)
                break
                
    def execute_sort(self, key):
        shortcut = next((s for s in self.shortcuts_data if s["key"] == key), None)
        if not shortcut: return

        current_file = self.image_files[self.current_image_index]
        src_path = os.path.join(self.source_folder, current_file)

        success_list = []
        for target_idx in shortcut["targets"]:
            dest_folder_info = self.folders_data[target_idx]
            dest_path = dest_folder_info["path"]
            
            try:
                shutil.copy2(src_path, dest_path)
                success_list.append(dest_folder_info["name"])
            except Exception as e:
                print(f"Failed to copy to {dest_folder_info['name']}: {e}")

        folder_names = ', '.join(success_list)
        self.show_toast(f"Saved to: {folder_names}")
        
        self.next_image()

    def next_image(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.load_image()
        else:
            self.end_session()

    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image()

    # ==========================================
    # END SESSION LOGIC (FINISH)
    # ==========================================
    def end_session(self):
        self.unbind("<Key>") # Disable shortcuts
        self.clear_frame(self.main_scroll) # Clear sorting UI
        
        # Create "Finished" Page
        finish_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        finish_frame.pack(fill="both", expand=True, pady=100)
        
        ctk.CTkLabel(finish_frame, text="🎉", font=("Segoe UI", 80)).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            finish_frame, 
            text="Sorting Complete!", 
            font=("Segoe UI", 32, "bold"), 
            text_color=COLOR_PRIMARY
        ).pack(pady=10)
        
        ctk.CTkLabel(
            finish_frame, 
            text=f"All photos in the folder have been successfully sorted.", 
            font=("Segoe UI", 16), 
            text_color="gray"
        ).pack(pady=5)
        
        # Return to Main Menu Button
        ctk.CTkButton(
            finish_frame,
            text="Return to Main Menu",
            command=self.init_config_page, # Call setup page again
            font=("Segoe UI", 16, "bold"),
            height=50,
            width=250,
            fg_color=COLOR_PRIMARY,
            hover_color="#1E293B",
            corner_radius=25
        ).pack(pady=40)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = SortirFotoApp()
    app.mainloop()
