import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
from PIL import Image

# --- Konfigurasi Modern (Palette Slate & Blue) ---
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("dark-blue") 

# Palette Warna Professional
COLOR_BG = "#F1F5F9"        # Background abu-abu muda
COLOR_SURFACE = "#FFFFFF"   # Putih bersih untuk kartu
COLOR_PRIMARY = "#0F172A"   # Navy Gelap
COLOR_ACCENT = "#3B82F6"    # Biru Cerah
COLOR_TEXT = "#334155"      # Teks abu tua
COLOR_BORDER = "#E2E8F0"    # Garis halus

class SortirFotoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SortirPro - Smart Photo Organizer")
        self.geometry("1100x800")
        self.configure(fg_color=COLOR_BG)

        # Variabel Data
        self.source_folder = ""
        self.image_files = []
        self.current_image_index = 0
        
        self.folders_data = [] 
        self.shortcuts_data = []

        # Container Utama
        self.main_scroll = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent", 
            corner_radius=0
        )
        self.main_scroll.pack(fill="both", expand=True, padx=0, pady=0)

        # Mulai dengan Halaman Konfigurasi
        self.init_config_page()

    # ==========================================
    # HALAMAN 1: KONFIGURASI (SETUP)
    # ==========================================
    def init_config_page(self):
        self.clear_frame(self.main_scroll)
        
        # Reset Data Penting saat kembali ke menu utama
        self.image_files = []
        self.current_image_index = 0
        
        # --- Hero Header ---
        header_frame = ctk.CTkFrame(self.main_scroll, fg_color=COLOR_PRIMARY, height=100, corner_radius=0)
        header_frame.pack(fill="x")
        
        lbl_title = ctk.CTkLabel(
            header_frame, 
            text="Konfigurasi Sortir Foto", 
            font=("Segoe UI", 28, "bold"), 
            text_color="white"
        )
        lbl_title.pack(pady=(25, 5))
        lbl_subtitle = ctk.CTkLabel(
            header_frame, 
            text="Atur folder sumber, tujuan, dan shortcut keyboard anda", 
            font=("Segoe UI", 14), 
            text_color="#94A3B8"
        )
        lbl_subtitle.pack(pady=(0, 25))

        # Container Content
        content_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        content_frame.pack(fill="both", padx=40, pady=20)

        # 1. Card: Pilih Source Folder
        self._create_section_header(content_frame, "1. Sumber Foto", "Pilih folder berisi foto yang ingin dirapikan.")
        
        card_source = ctk.CTkFrame(content_frame, fg_color=COLOR_SURFACE, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        card_source.pack(fill="x", pady=(5, 20), ipady=10)

        inner_source = ctk.CTkFrame(card_source, fg_color="transparent")
        inner_source.pack(fill="x", padx=20, pady=10)

        self.btn_source = ctk.CTkButton(
            inner_source, 
            text="📂 Pilih Folder Sumber", 
            command=self.select_source_folder,
            fg_color=COLOR_ACCENT, 
            hover_color="#2563EB",
            font=("Segoe UI", 14, "bold"),
            height=40
        )
        self.btn_source.pack(side="left")
        
        # Tampilkan path jika sudah ada (misal user kembali ke menu tapi path masih tersimpan)
        display_path = self.source_folder if self.source_folder else "Belum ada folder dipilih"
        self.lbl_source_path = ctk.CTkLabel(inner_source, text=display_path, text_color="gray", font=("Consolas", 12))
        self.lbl_source_path.pack(side="left", padx=15)

        # 2. Card: Setup Folder Tujuan
        self._create_section_header(content_frame, "2. Folder Tujuan", "Buat label kategori dan lokasi penyimpanannya.")

        card_dest = ctk.CTkFrame(content_frame, fg_color=COLOR_SURFACE, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        card_dest.pack(fill="x", pady=(5, 20), ipady=5)

        self.folder_container = ctk.CTkFrame(card_dest, fg_color="transparent")
        self.folder_container.pack(fill="x", padx=10, pady=10)
        
        self.folder_entries = [] 
        
        btn_add_folder = ctk.CTkButton(
            card_dest, 
            text="+ Tambah Kategori Baru", 
            command=self.add_folder_row,
            fg_color="transparent", 
            text_color=COLOR_ACCENT,
            border_width=1,
            border_color=COLOR_ACCENT,
            hover_color="#EFF6FF"
        )
        btn_add_folder.pack(pady=10)

        # 3. Card: Setup Shortcut
        self._create_section_header(content_frame, "3. Shortcut Keyboard", "Petakan tombol keyboard ke folder tujuan.")

        card_shortcut = ctk.CTkFrame(content_frame, fg_color=COLOR_SURFACE, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        card_shortcut.pack(fill="x", pady=(5, 20), ipady=5)

        self.shortcut_container = ctk.CTkFrame(card_shortcut, fg_color="transparent")
        self.shortcut_container.pack(fill="x", padx=10, pady=10)

        self.shortcut_rows = [] 

        btn_add_shortcut = ctk.CTkButton(
            card_shortcut, 
            text="+ Tambah Shortcut", 
            command=self.add_shortcut_row,
            fg_color="transparent", 
            text_color=COLOR_ACCENT,
            border_width=1,
            border_color=COLOR_ACCENT,
            hover_color="#EFF6FF"
        )
        btn_add_shortcut.pack(pady=10)

        # Tombol Mulai
        self.btn_start = ctk.CTkButton(
            content_frame, 
            text="MULAI MENYORTIR 🚀", 
            command=self.start_sorting_process,
            font=("Segoe UI", 16, "bold"),
            height=55,
            corner_radius=27,
            fg_color=COLOR_PRIMARY, 
            hover_color="#1E293B"
        )
        self.btn_start.pack(pady=30, fill="x", padx=100)

        # Inisialisasi baris awal (atau muat ulang jika data sudah ada sebelumnya - logic sederhana: reset dulu)
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

        entry_name = ctk.CTkEntry(row_frame, placeholder_text="Nama Label (mis: Liburan)", width=200, height=35)
        entry_name.pack(side="left", padx=5)
        
        entry_path = ctk.CTkEntry(row_frame, placeholder_text="Path Folder Tujuan...", width=300, height=35)
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
        
        ctk.CTkLabel(left_sec, text="Tekan Tombol:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        entry_key = ctk.CTkEntry(left_sec, width=60, placeholder_text="A", font=("Consolas", 14, "bold"), justify="center")
        entry_key.pack()
        
        divider = ctk.CTkFrame(row_frame, width=1, height=40, fg_color="#CBD5E1")
        divider.pack(side="left", padx=10)

        right_sec = ctk.CTkFrame(row_frame, fg_color="transparent")
        right_sec.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(right_sec, text="Salin ke Folder:", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 5))
        
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
    # LOGIKA START & VALIDASI
    # ==========================================
    def start_sorting_process(self):
        if not self.source_folder:
            messagebox.showerror("Error", "Pilih folder sumber foto dulu!")
            return

        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
        self.image_files = [f for f in os.listdir(self.source_folder) if f.lower().endswith(valid_extensions)]
        self.image_files.sort()
        
        if not self.image_files:
            messagebox.showerror("Error", "Folder kosong atau tidak ada gambar!")
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
                        messagebox.showerror("Error", f"Gagal membuat folder {name}: {e}")
                        return
                self.folders_data.append({"name": name, "path": full_path})
        
        if not self.folders_data:
            messagebox.showerror("Error", "Minimal buat 1 folder tujuan!")
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
            messagebox.showerror("Error", "Atur minimal 1 tombol shortcut!")
            return

        self.init_sorting_page()

    # ==========================================
    # HALAMAN 2: SORTIR (DESIGN OVERHAUL)
    # ==========================================
    def init_sorting_page(self):
        self.clear_frame(self.main_scroll)
        self.current_image_index = 0
        self.bind("<Key>", self.handle_keypress)
        
        # Grid Layout
        container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Kolom Kiri: Image Viewer
        left_col = ctk.CTkFrame(container, fg_color="#18181b", corner_radius=15)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Header Info File
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

        # Kolom Kanan: Kontrol & Shortcut
        right_col = ctk.CTkFrame(container, fg_color="transparent", width=300)
        right_col.pack(side="right", fill="y")

        # Navigasi
        nav_card = ctk.CTkFrame(right_col, fg_color=COLOR_SURFACE, corner_radius=10)
        nav_card.pack(fill="x", pady=(0, 20), ipady=10)
        
        ctk.CTkLabel(nav_card, text="Navigasi", font=("Segoe UI", 12, "bold"), text_color="gray").pack(pady=5)
        nav_btns = ctk.CTkFrame(nav_card, fg_color="transparent")
        nav_btns.pack()
        
        ctk.CTkButton(nav_btns, text="← Prev", command=self.prev_image, width=80, fg_color="#E2E8F0", text_color="black", hover_color="#CBD5E1").pack(side="left", padx=5)
        ctk.CTkButton(nav_btns, text="Next →", command=self.next_image, width=80, fg_color="#E2E8F0", text_color="black", hover_color="#CBD5E1").pack(side="left", padx=5)

        # Grid Shortcut
        shortcut_card = ctk.CTkFrame(right_col, fg_color=COLOR_SURFACE, corner_radius=10)
        shortcut_card.pack(fill="both", expand=True, ipady=10)
        
        ctk.CTkLabel(shortcut_card, text="SHORTCUT KEYBOARD", font=("Segoe UI", 14, "bold"), text_color=COLOR_PRIMARY).pack(pady=15)

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
            
            ctk.CTkLabel(info_container, text="Simpan ke:", font=("Segoe UI", 10), text_color="gray").pack(anchor="w")
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
                print(f"Gagal copy ke {dest_folder_info['name']}: {e}")

        folder_names = ', '.join(success_list)
        self.show_toast(f"Disimpan ke: {folder_names}")
        
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
    # LOGIKA END SESSION (FINISH)
    # ==========================================
    def end_session(self):
        self.unbind("<Key>") # Matikan shortcut
        self.clear_frame(self.main_scroll) # Bersihkan UI Sortir
        
        # Buat Halaman "Selesai"
        finish_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        finish_frame.pack(fill="both", expand=True, pady=100)
        
        ctk.CTkLabel(finish_frame, text="🎉", font=("Segoe UI", 80)).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            finish_frame, 
            text="Penyortiran Selesai!", 
            font=("Segoe UI", 32, "bold"), 
            text_color=COLOR_PRIMARY
        ).pack(pady=10)
        
        ctk.CTkLabel(
            finish_frame, 
            text=f"Semua foto dalam folder telah berhasil disortir.", 
            font=("Segoe UI", 16), 
            text_color="gray"
        ).pack(pady=5)
        
        # Tombol Kembali ke Utama
        ctk.CTkButton(
            finish_frame,
            text="Kembali ke Menu Utama",
            command=self.init_config_page, # Panggil ulang setup page
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
