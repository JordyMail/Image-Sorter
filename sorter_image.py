import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
from PIL import Image
from datetime import datetime

# --- Konfigurasi Tema & Warna Modern ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Palet Warna Modern
PRIMARY_COLOR = "#2563eb"      # Biru cerah modern
PRIMARY_HOVER = "#1d4ed8"      # Biru gelap hover
SECONDARY_COLOR = "#64748b"    # Abu-abu slate
SUCCESS_COLOR = "#10b981"      # Hijau
WARNING_COLOR = "#f59e0b"      # Orange
BG_COLOR = "#ffffff"           # Putih
CARD_BG = "#f8fafc"           # Putih keabuan
BORDER_COLOR = "#e2e8f0"      # Abu-abu border
TEXT_DARK = "#0f172a"         # Hitam kebiruan
TEXT_LIGHT = "#64748b"        # Abu-abu teks
SHADOW_COLOR = "rgba(0,0,0,0.05)"  # Efek bayangan

class ModernCard(ctk.CTkFrame):
    """Frame dengan desain kartu modern"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=CARD_BG,
            border_width=1,
            border_color=BORDER_COLOR,
            corner_radius=12
        )

class SortirFotoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SortirFoto Pro - Aplikasi Sortir Gambar Cerdas")
        self.geometry("1200x800")
        self.configure(fg_color=BG_COLOR)
        
        # Center window
        self.center_window()

        # Variabel Data
        self.source_folder = ""
        self.image_files = []
        self.current_image_index = 0
        
        # Struktur Data
        self.folders_data = [] 
        self.shortcuts_data = []

        # Container Utama dengan padding konsisten
        self.main_scroll = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_button_color=PRIMARY_COLOR,
            scrollbar_button_hover_color=PRIMARY_HOVER
        )
        self.main_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        # Status Bar
        self.status_bar = ctk.CTkLabel(
            self, 
            text="✨ Selamat datang di SortirFoto Pro", 
            font=("Inter", 12),
            text_color=TEXT_LIGHT,
            fg_color=CARD_BG,
            corner_radius=6,
            height=30
        )
        self.status_bar.pack(side="bottom", fill="x", padx=20, pady=(0, 10))

        # Mulai dengan Halaman Konfigurasi
        self.init_config_page()

    def center_window(self):
        """Memposisikan window di tengah layar"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_header(self, text, subtitle=None):
        """Membuat header dengan desain modern"""
        header_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Garis dekoratif atas
        top_line = ctk.CTkFrame(header_frame, height=4, width=60, fg_color=PRIMARY_COLOR, corner_radius=2)
        top_line.pack(anchor="w", pady=(0, 10))
        
        lbl_title = ctk.CTkLabel(
            header_frame, 
            text=text, 
            font=("Inter", 28, "bold"), 
            text_color=TEXT_DARK,
            anchor="w"
        )
        lbl_title.pack(anchor="w")
        
        if subtitle:
            lbl_subtitle = ctk.CTkLabel(
                header_frame, 
                text=subtitle, 
                font=("Inter", 14), 
                text_color=TEXT_LIGHT,
                anchor="w"
            )
            lbl_subtitle.pack(anchor="w", pady=(5, 0))
        
        return header_frame

    # ==========================================
    # HALAMAN 1: KONFIGURASI (SETUP)
    # ==========================================
    def init_config_page(self):
        self.clear_frame(self.main_scroll)
        
        # Header dengan desain modern
        self.create_header(
            "Setup Sortir Foto", 
            "Konfigurasi folder sumber, folder tujuan, dan shortcut keyboard"
        )

        # 1. Source Folder Card
        source_card = ModernCard(self.main_scroll)
        source_card.pack(fill="x", pady=10)
        
        # Icon dan judul section
        section_header = ctk.CTkFrame(source_card, fg_color="transparent")
        section_header.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            section_header, 
            text="📁", 
            font=("Inter", 20)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            section_header, 
            text="Folder Sumber", 
            font=("Inter", 16, "bold"), 
            text_color=TEXT_DARK
        ).pack(side="left")
        
        # Content
        content_frame = ctk.CTkFrame(source_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.btn_source = ctk.CTkButton(
            content_frame, 
            text="📂  Pilih Folder Sumber Foto", 
            command=self.select_source_folder,
            fg_color=PRIMARY_COLOR, 
            hover_color=PRIMARY_HOVER,
            height=45,
            corner_radius=8,
            font=("Inter", 13)
        )
        self.btn_source.pack(side="left", padx=(0, 15))
        
        self.lbl_source_path = ctk.CTkLabel(
            content_frame, 
            text="Belum ada folder dipilih", 
            text_color=TEXT_LIGHT,
            font=("Inter", 12)
        )
        self.lbl_source_path.pack(side="left")

        # 2. Folder Tujuan Card
        dest_card = ModernCard(self.main_scroll)
        dest_card.pack(fill="x", pady=10)
        
        # Header dengan step indicator
        step_header = ctk.CTkFrame(dest_card, fg_color="transparent")
        step_header.pack(fill="x", padx=20, pady=15)
        
        step_badge = ctk.CTkFrame(step_header, fg_color=PRIMARY_COLOR, corner_radius=12, width=24, height=24)
        step_badge.pack(side="left", padx=(0, 10))
        step_badge.pack_propagate(False)
        
        ctk.CTkLabel(
            step_badge, 
            text="1", 
            font=("Inter", 12, "bold"), 
            text_color="white"
        ).pack(expand=True)
        
        ctk.CTkLabel(
            step_header, 
            text="Buat Folder Tujuan", 
            font=("Inter", 16, "bold"), 
            text_color=TEXT_DARK
        ).pack(side="left")
        
        # Container folder entries
        self.folder_container = ctk.CTkFrame(dest_card, fg_color="transparent")
        self.folder_container.pack(fill="x", padx=20, pady=10)
        
        self.folder_entries = []
        
        btn_add_folder = ctk.CTkButton(
            dest_card, 
            text="+  Tambah Folder Tujuan", 
            command=self.add_folder_row,
            fg_color="transparent",
            text_color=PRIMARY_COLOR,
            hover_color=CARD_BG,
            border_width=2,
            border_color=PRIMARY_COLOR,
            height=40,
            corner_radius=8,
            font=("Inter", 12)
        )
        btn_add_folder.pack(pady=(0, 20), padx=20)

        # 3. Shortcut Card
        shortcut_card = ModernCard(self.main_scroll)
        shortcut_card.pack(fill="x", pady=10)
        
        step_header = ctk.CTkFrame(shortcut_card, fg_color="transparent")
        step_header.pack(fill="x", padx=20, pady=15)
        
        step_badge = ctk.CTkFrame(step_header, fg_color=PRIMARY_COLOR, corner_radius=12, width=24, height=24)
        step_badge.pack(side="left", padx=(0, 10))
        step_badge.pack_propagate(False)
        
        ctk.CTkLabel(
            step_badge, 
            text="2", 
            font=("Inter", 12, "bold"), 
            text_color="white"
        ).pack(expand=True)
        
        ctk.CTkLabel(
            step_header, 
            text="Atur Shortcut Keyboard", 
            font=("Inter", 16, "bold"), 
            text_color=TEXT_DARK
        ).pack(side="left")
        
        info_text = ctk.CTkLabel(
            shortcut_card,
            text="💡 Tekan tombol keyboard untuk menyimpan gambar ke folder yang dipilih",
            font=("Inter", 11),
            text_color=TEXT_LIGHT,
            fg_color="#f1f5f9",
            corner_radius=6,
            height=30
        )
        info_text.pack(padx=20, pady=(0, 10), fill="x")
        
        self.shortcut_container = ctk.CTkFrame(shortcut_card, fg_color="transparent")
        self.shortcut_container.pack(fill="x", padx=20, pady=10)

        self.shortcut_rows = []

        btn_add_shortcut = ctk.CTkButton(
            shortcut_card, 
            text="+  Tambah Shortcut", 
            command=self.add_shortcut_row,
            fg_color="transparent",
            text_color=PRIMARY_COLOR,
            hover_color=CARD_BG,
            border_width=2,
            border_color=PRIMARY_COLOR,
            height=40,
            corner_radius=8,
            font=("Inter", 12)
        )
        btn_add_shortcut.pack(pady=(0, 20), padx=20)

        # Tombol Mulai
        button_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        button_container.pack(fill="x", pady=30)
        
        self.btn_start = ctk.CTkButton(
            button_container, 
            text="🚀  MULAI MENYORTIR", 
            command=self.start_sorting_process,
            font=("Inter", 16, "bold"),
            height=55,
            corner_radius=10,
            fg_color=SUCCESS_COLOR, 
            hover_color="#0d9488",
            border_width=0
        )
        self.btn_start.pack(fill="x", ipady=5)

        # Tambah baris awal default
        self.add_folder_row()
        self.add_shortcut_row()

    def add_folder_row(self):
        """Menambah baris input folder dengan desain modern"""
        row_frame = ctk.CTkFrame(self.folder_container, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)
        
        # Nomor urut
        folder_number = len(self.folder_entries) + 1
        
        number_badge = ctk.CTkFrame(
            row_frame, 
            fg_color=BORDER_COLOR, 
            corner_radius=6,
            width=28,
            height=28
        )
        number_badge.pack(side="left", padx=(0, 10))
        number_badge.pack_propagate(False)
        
        ctk.CTkLabel(
            number_badge, 
            text=str(folder_number), 
            font=("Inter", 11, "bold"),
            text_color=TEXT_DARK
        ).pack(expand=True)
        
        entry_name = ctk.CTkEntry(
            row_frame, 
            placeholder_text="Nama folder (contoh: Produk)", 
            width=200,
            height=38,
            corner_radius=8,
            border_color=BORDER_COLOR,
            font=("Inter", 12)
        )
        entry_name.pack(side="left", padx=5)
        
        entry_path = ctk.CTkEntry(
            row_frame, 
            placeholder_text="Lokasi penyimpanan", 
            width=300,
            height=38,
            corner_radius=8,
            border_color=BORDER_COLOR,
            font=("Inter", 12)
        )
        entry_path.pack(side="left", padx=5)
        
        def browse_dest():
            d = filedialog.askdirectory()
            if d:
                entry_path.delete(0, "end")
                entry_path.insert(0, d)

        btn_browse = ctk.CTkButton(
            row_frame, 
            text="📁  Pilih", 
            width=80,
            height=38,
            command=browse_dest,
            fg_color=SECONDARY_COLOR,
            hover_color="#475569",
            corner_radius=8,
            font=("Inter", 11)
        )
        btn_browse.pack(side="left", padx=5)

        self.folder_entries.append({"name": entry_name, "path": entry_path, "frame": row_frame})
        self.refresh_shortcut_options()

    def add_shortcut_row(self):
        """Menambah baris shortcut dengan desain modern"""
        row_frame = ctk.CTkFrame(
            self.shortcut_container, 
            fg_color=CARD_BG,
            border_width=1, 
            border_color=BORDER_COLOR,
            corner_radius=10
        )
        row_frame.pack(fill="x", pady=8, padx=5)
        
        content_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Label tombol
        ctk.CTkLabel(
            content_frame, 
            text="⌨️  Tekan tombol:", 
            font=("Inter", 12),
            text_color=TEXT_DARK
        ).pack(side="left", padx=(0, 10))
        
        entry_key = ctk.CTkEntry(
            content_frame, 
            width=60,
            height=38,
            placeholder_text="1",
            corner_radius=8,
            border_color=BORDER_COLOR,
            font=("Inter", 12),
            justify="center"
        )
        entry_key.pack(side="left", padx=5)
        
        ctk.CTkLabel(
            content_frame, 
            text="→  simpan ke:", 
            font=("Inter", 12),
            text_color=TEXT_DARK
        ).pack(side="left", padx=(15, 10))
        
        # Container untuk checkbox
        check_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        check_container.pack(side="left", fill="x", expand=True)
        
        # Kita simpan referensi row ini
        self.shortcut_rows.append({
            "key": entry_key, 
            "frame": content_frame, 
            "check_container": check_container,
            "checks": []
        })
        
        self.refresh_shortcut_options()

    def refresh_shortcut_options(self):
        """Update pilihan folder dengan desain modern"""
        current_folders = [e["name"].get() for e in self.folder_entries]
        
        for row in self.shortcut_rows:
            # Hapus checkbox lama
            for widget in row["check_container"].winfo_children():
                widget.destroy()
            
            row["checks"] = []
            
            if current_folders:
                for i, folder_name in enumerate(current_folders):
                    name_display = folder_name if folder_name else f"Folder {i+1}"
                    
                    chk = ctk.CTkCheckBox(
                        row["check_container"], 
                        text=name_display,
                        fg_color=PRIMARY_COLOR,
                        hover_color=PRIMARY_HOVER,
                        corner_radius=6,
                        font=("Inter", 11),
                        text_color=TEXT_DARK,
                        border_color=BORDER_COLOR
                    )
                    chk.pack(side="left", padx=8)
                    row["checks"].append(chk)
            else:
                ctk.CTkLabel(
                    row["check_container"], 
                    text="(Belum ada folder tujuan)",
                    text_color=TEXT_LIGHT,
                    font=("Inter", 11, "italic")
                ).pack(side="left")

    def select_source_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.source_folder = path
            self.lbl_source_path.configure(
                text=f"📂  {path}", 
                text_color=PRIMARY_COLOR,
                font=("Inter", 12, "bold")
            )
            self.update_status(f"Folder sumber dipilih: {os.path.basename(path)}")

    def update_status(self, message):
        """Update status bar"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_bar.configure(text=f"[{timestamp}]  {message}")

    # ==========================================
    # LOGIKA START & VALIDASI
    # ==========================================
    def start_sorting_process(self):
        # 1. Validasi Source
        if not self.source_folder:
            messagebox.showerror("Error", "Pilih folder sumber foto dulu!")
            return

        # 2. Ambil List Foto
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        self.image_files = [f for f in os.listdir(self.source_folder) if f.lower().endswith(valid_extensions)]
        self.image_files.sort()
        
        if not self.image_files:
            messagebox.showerror("Error", "Folder kosong atau tidak ada gambar!")
            return

        # 3. Validasi & Buat Folder Tujuan
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
                        messagebox.showerror("Error", f"Gagal membuat folder {name}: {e}")
                        return
                self.folders_data.append({"name": name, "path": full_path})
        
        if not self.folders_data:
            messagebox.showerror("Error", "Minimal buat 1 folder tujuan!")
            return

        # 4. Validasi Shortcuts
        self.shortcuts_data = []
        for row in self.shortcut_rows:
            key = row["key"].get().lower()
            selected_indices = [i for i, chk in enumerate(row["checks"]) if chk.get() == 1]
            
            if key and selected_indices:
                valid_indices = [i for i in selected_indices if i < len(self.folders_data)]
                if valid_indices:
                    self.shortcuts_data.append({"key": key, "targets": valid_indices})

        if not self.shortcuts_data:
            messagebox.showerror("Error", "Atur minimal 1 tombol shortcut!")
            return

        self.update_status(f"Memulai sortir {len(self.image_files)} gambar...")
        self.init_sorting_page()

    # ==========================================
    # HALAMAN 2: SORTIR (MAIN UI)
    # ==========================================
    def init_sorting_page(self):
        self.clear_frame(self.main_scroll)
        self.current_image_index = 0
        
        # Bind Keyboard Events
        self.bind("<Key>", self.handle_keypress)
        self.focus_set()

        # Header
        self.create_header(
            "Sortir Gambar", 
            f"{len(self.image_files)} gambar ditemukan"
        )

        # Main content grid
        content_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Column configuration
        content_frame.grid_columnconfigure(0, weight=1)

        # 1. Image Card
        image_card = ModernCard(content_frame)
        image_card.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Image container
        image_container = ctk.CTkFrame(image_card, fg_color=CARD_BG)
        image_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.image_label = ctk.CTkLabel(
            image_container, 
            text="",
            font=("Inter", 14)
        )
        self.image_label.pack(expand=True)

        # 2. File Info Card
        info_card = ModernCard(content_frame)
        info_card.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        info_container = ctk.CTkFrame(info_card, fg_color="transparent")
        info_container.pack(fill="x", padx=20, pady=15)
        
        self.file_info_label = ctk.CTkLabel(
            info_container, 
            text="Memuat gambar...",
            font=("Inter", 14, "bold"),
            text_color=TEXT_DARK
        )
        self.file_info_label.pack()
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            info_container,
            height=6,
            corner_radius=3,
            fg_color=BORDER_COLOR,
            progress_color=PRIMARY_COLOR
        )
        self.progress_bar.pack(fill="x", pady=(10, 0))
        self.progress_bar.set(0)

        # 3. Navigation Card
        nav_card = ModernCard(content_frame)
        nav_card.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        nav_container = ctk.CTkFrame(nav_card, fg_color="transparent")
        nav_container.pack(padx=20, pady=15)
        
        btn_prev = ctk.CTkButton(
            nav_container, 
            text="◀  Sebelumnya", 
            command=self.prev_image,
            fg_color=SECONDARY_COLOR,
            hover_color="#475569",
            height=40,
            width=150,
            corner_radius=8,
            font=("Inter", 12)
        )
        btn_prev.pack(side="left", padx=10)
        
        btn_next = ctk.CTkButton(
            nav_container, 
            text="Lewati  ▶", 
            command=self.next_image,
            fg_color=SECONDARY_COLOR,
            hover_color="#475569",
            height=40,
            width=150,
            corner_radius=8,
            font=("Inter", 12)
        )
        btn_next.pack(side="left", padx=10)

        # 4. Shortcut Panel
        shortcut_panel = ModernCard(content_frame)
        shortcut_panel.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        
        panel_header = ctk.CTkFrame(shortcut_panel, fg_color="transparent")
        panel_header.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            panel_header, 
            text="⌨️  Shortcut Keyboard", 
            font=("Inter", 16, "bold"),
            text_color=TEXT_DARK
        ).pack(side="left")
        
        # Grid untuk shortcut buttons
        grid_frame = ctk.CTkFrame(shortcut_panel, fg_color="transparent")
        grid_frame.pack(padx=20, pady=(0, 20))
        
        # Tombol shortcut dengan desain modern
        for i, s_data in enumerate(self.shortcuts_data):
            key = s_data["key"].upper()
            target_names = [self.folders_data[i]["name"] for i in s_data["targets"]]
            desc = " & ".join(target_names[:2])
            if len(target_names) > 2:
                desc += f" +{len(target_names)-2} lainnya"
            
            btn_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
            btn_frame.grid(row=i//3, column=i%3, padx=10, pady=10)
            
            btn = ctk.CTkButton(
                btn_frame,
                text=f"{key}",
                font=("Inter", 20, "bold"),
                width=70,
                height=70,
                corner_radius=12,
                fg_color=PRIMARY_COLOR,
                hover_color=PRIMARY_HOVER,
                command=lambda k=s_data["key"]: self.execute_sort(k)
            )
            btn.pack()
            
            ctk.CTkLabel(
                btn_frame,
                text=f"→ {desc}",
                font=("Inter", 11),
                text_color=TEXT_LIGHT,
                wraplength=150
            ).pack(pady=(5, 0))

        self.load_image()

    def load_image(self):
        """Memuat gambar dengan animasi progress"""
        if 0 <= self.current_image_index < len(self.image_files):
            file_name = self.image_files[self.current_image_index]
            file_path = os.path.join(self.source_folder, file_name)
            
            # Update progress
            progress = (self.current_image_index + 1) / len(self.image_files)
            self.progress_bar.set(progress)
            
            # Update Info
            self.file_info_label.configure(
                text=f"[{self.current_image_index + 1}/{len(self.image_files)}]  {file_name}"
            )
            
            # Load & Resize Image
            try:
                img = Image.open(file_path)
                
                # Hitung rasio resize
                max_height = 500
                max_width = 800
                
                aspect_ratio = img.width / img.height
                
                if img.width > max_width or img.height > max_height:
                    if aspect_ratio > 1:
                        new_width = min(max_width, img.width)
                        new_height = int(new_width / aspect_ratio)
                    else:
                        new_height = min(max_height, img.height)
                        new_width = int(new_height * aspect_ratio)
                else:
                    new_width, new_height = img.width, img.height
                
                my_image = ctk.CTkImage(
                    light_image=img, 
                    dark_image=img, 
                    size=(new_width, new_height)
                )
                self.image_label.configure(image=my_image, text="")
                
            except Exception as e:
                self.file_info_label.configure(
                    text=f"Error loading image: {e}",
                    text_color="#ef4444"
                )
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
                print(f"Gagal copy ke {dest_folder_info['name']}: {e}")

        # Feedback visual
        if success_list:
            self.update_status(f"✓ {current_file} → {', '.join(success_list)}")
        
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

    def end_session(self):
        """Tampilkan halaman selesai dengan desain modern"""
        self.clear_frame(self.main_scroll)
        
        # Card sukses
        success_card = ModernCard(self.main_scroll)
        success_card.pack(expand=True, padx=50, pady=50)
        
        # Icon sukses
        icon_frame = ctk.CTkFrame(success_card, fg_color=SUCCESS_COLOR, corner_radius=50, width=80, height=80)
        icon_frame.pack(pady=(40, 20))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame, 
            text="✓", 
            font=("Inter", 40, "bold"),
            text_color="white"
        ).pack(expand=True)
        
        ctk.CTkLabel(
            success_card, 
            text="Selesai!", 
            font=("Inter", 32, "bold"),
            text_color=TEXT_DARK
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            success_card, 
            text="Semua foto telah disortir", 
            font=("Inter", 16),
            text_color=TEXT_LIGHT
        ).pack(pady=(0, 30))
        
        # Ringkasan
        summary_frame = ctk.CTkFrame(success_card, fg_color=CARD_BG, corner_radius=10)
        summary_frame.pack(padx=40, pady=20, fill="x")
        
        total_images = len(self.image_files)
        total_folders = len(self.folders_data)
        
        ctk.CTkLabel(
            summary_frame,
            text=f"📸 {total_images} gambar telah disortir ke {total_folders} folder",
            font=("Inter", 14),
            text_color=TEXT_DARK
        ).pack(pady=15)
        
        btn_new = ctk.CTkButton(
            success_card,
            text="🔄  Mulai Sortir Baru",
            command=self.init_config_page,
            fg_color=PRIMARY_COLOR,
            hover_color=PRIMARY_HOVER,
            height=45,
            width=200,
            corner_radius=8,
            font=("Inter", 14, "bold")
        )
        btn_new.pack(pady=30)
        
        self.unbind("<Key>")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = SortirFotoApp()
    app.mainloop()
