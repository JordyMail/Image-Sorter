import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
from PIL import Image

# --- Konfigurasi Tema & Warna ---
ctk.set_appearance_mode("Light")  # Mode terang (Dominan Putih)
ctk.set_default_color_theme("dark-blue") 

# Kode Warna Navy
NAVY_COLOR = "#001F3F"
NAVY_HOVER = "#003366"
WHITE_BG = "#FFFFFF"

class SortirFotoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aplikasi Sortir Gambar Modern")
        self.geometry("1000x700")
        self.configure(fg_color=WHITE_BG)

        # Variabel Data
        self.source_folder = ""
        self.image_files = []
        self.current_image_index = 0
        
        # Struktur Data: 
        # folders = [{"name": "Folder A", "path": "C:/..."}, ...]
        self.folders_data = [] 
        # shortcuts = [{"key": "1", "targets": [0, 1]}] (targets adalah index dari folders_data)
        self.shortcuts_data = []

        # Container Utama (Scrollable agar responsif di layar kecil)
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Mulai dengan Halaman Konfigurasi
        self.init_config_page()

    # ==========================================
    # HALAMAN 1: KONFIGURASI (SETUP)
    # ==========================================
    def init_config_page(self):
        self.clear_frame(self.main_scroll)
        
        # Header
        lbl_title = ctk.CTkLabel(self.main_scroll, text="Setup Sortir Foto", 
                                 font=("Roboto", 24, "bold"), text_color=NAVY_COLOR)
        lbl_title.pack(pady=20)

        # 1. Pilih Source Folder
        self.btn_source = ctk.CTkButton(self.main_scroll, text="Pilih Folder Sumber Foto", 
                                        command=self.select_source_folder,
                                        fg_color=NAVY_COLOR, hover_color=NAVY_HOVER)
        self.btn_source.pack(pady=10)
        
        self.lbl_source_path = ctk.CTkLabel(self.main_scroll, text="Belum ada folder dipilih", text_color="gray")
        self.lbl_source_path.pack(pady=(0, 20))

        ctk.CTkFrame(self.main_scroll, height=2, fg_color="lightgray").pack(fill="x", padx=50, pady=10)

        # 2. Setup Folder Tujuan
        ctk.CTkLabel(self.main_scroll, text="Langkah 1: Buat Folder Tujuan", font=("Roboto", 18, "bold"), text_color=NAVY_COLOR).pack(pady=10)
        
        self.folder_container = ctk.CTkFrame(self.main_scroll, fg_color="#F0F0F0")
        self.folder_container.pack(fill="x", padx=20, pady=10)
        
        self.folder_entries = [] # Menyimpan widget input folder
        
        btn_add_folder = ctk.CTkButton(self.main_scroll, text="+ Tambah Folder Tujuan", 
                                       command=self.add_folder_row,
                                       fg_color="gray", hover_color="darkgray")
        btn_add_folder.pack(pady=5)

        ctk.CTkFrame(self.main_scroll, height=2, fg_color="lightgray").pack(fill="x", padx=50, pady=20)

        # 3. Setup Shortcut Tombol
        ctk.CTkLabel(self.main_scroll, text="Langkah 2: Atur Fungsi Tombol/Shortcut", font=("Roboto", 18, "bold"), text_color=NAVY_COLOR).pack(pady=10)
        ctk.CTkLabel(self.main_scroll, text="Contoh: Tekan '1' simpan ke Folder A, Tekan '2' simpan ke Folder A & B", text_color="gray").pack()

        self.shortcut_container = ctk.CTkFrame(self.main_scroll, fg_color="#F0F0F0")
        self.shortcut_container.pack(fill="x", padx=20, pady=10)

        self.shortcut_rows = [] # Menyimpan widget shortcut

        btn_add_shortcut = ctk.CTkButton(self.main_scroll, text="+ Tambah Tombol Shortcut", 
                                         command=self.add_shortcut_row,
                                         fg_color="gray", hover_color="darkgray")
        btn_add_shortcut.pack(pady=5)

        # Tombol Mulai
        ctk.CTkFrame(self.main_scroll, height=2, fg_color="lightgray").pack(fill="x", padx=50, pady=30)
        self.btn_start = ctk.CTkButton(self.main_scroll, text="MULAI MENYORTIR", 
                                       command=self.start_sorting_process,
                                       font=("Roboto", 16, "bold"),
                                       height=50,
                                       fg_color=NAVY_COLOR, hover_color=NAVY_HOVER)
        self.btn_start.pack(pady=30, fill="x", padx=100)

        # Tambah baris awal default
        self.add_folder_row()
        self.add_shortcut_row()

    # --- Logika Setup Folder ---
    def add_folder_row(self):
        row_frame = ctk.CTkFrame(self.folder_container, fg_color="transparent")
        row_frame.pack(fill="x", pady=2)
        
        entry_name = ctk.CTkEntry(row_frame, placeholder_text="Nama Label Folder (misal: Folder A)", width=200)
        entry_name.pack(side="left", padx=5)
        
        entry_path = ctk.CTkEntry(row_frame, placeholder_text="Lokasi Simpan", width=300)
        entry_path.pack(side="left", padx=5)
        
        def browse_dest():
            d = filedialog.askdirectory()
            if d:
                entry_path.delete(0, "end")
                entry_path.insert(0, d)

        btn_browse = ctk.CTkButton(row_frame, text="Pilih Lokasi", width=80, command=browse_dest, fg_color=NAVY_COLOR)
        btn_browse.pack(side="left", padx=5)

        self.folder_entries.append({"name": entry_name, "path": entry_path, "frame": row_frame})

    # --- Logika Setup Shortcut ---
    def add_shortcut_row(self):
        row_frame = ctk.CTkFrame(self.shortcut_container, fg_color="transparent", border_width=1, border_color="#DDD")
        row_frame.pack(fill="x", pady=5, padx=5)
        
        ctk.CTkLabel(row_frame, text="Tombol Keyboard:").pack(side="left", padx=5)
        entry_key = ctk.CTkEntry(row_frame, width=50, placeholder_text="1")
        entry_key.pack(side="left", padx=5)
        
        ctk.CTkLabel(row_frame, text="Akan menyimpan ke:").pack(side="left", padx=10)
        
        # Checkboxes area (akan diisi nanti saat tombol refresh ditekan atau saat start, 
        # tapi untuk dinamis kita buat placeholder text dulu)
        lbl_info = ctk.CTkLabel(row_frame, text="(Folder diambil dari langkah 1 diatas)", text_color="gray", font=("Arial", 10))
        lbl_info.pack(side="left")
        
        # Kita simpan referensi row ini
        self.shortcut_rows.append({"key": entry_key, "frame": row_frame, "checks": []})
        
        # Update checkbox berdasarkan folder yang ada saat ini
        self.refresh_shortcut_options()

    def refresh_shortcut_options(self):
        # Update pilihan folder di setiap baris shortcut
        current_folders = [e["name"].get() for e in self.folder_entries]
        
        for row in self.shortcut_rows:
            # Hapus checkbox lama
            for widget in row["frame"].winfo_children():
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.destroy()
            
            row["checks"] = []
            for i, folder_name in enumerate(current_folders):
                name_display = folder_name if folder_name else f"Folder {i+1}"
                chk = ctk.CTkCheckBox(row["frame"], text=name_display, fg_color=NAVY_COLOR)
                chk.pack(side="left", padx=5)
                row["checks"].append(chk)

    def select_source_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.source_folder = path
            self.lbl_source_path.configure(text=path)

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
                # Validasi index folder (jika user menghapus baris folder tp checkbox masih ada)
                valid_indices = [i for i in selected_indices if i < len(self.folders_data)]
                if valid_indices:
                    self.shortcuts_data.append({"key": key, "targets": valid_indices})

        if not self.shortcuts_data:
            messagebox.showerror("Error", "Atur minimal 1 tombol shortcut!")
            return

        # Masuk ke Halaman Sortir
        self.init_sorting_page()

    # ==========================================
    # HALAMAN 2: SORTIR (MAIN UI)
    # ==========================================
    def init_sorting_page(self):
        self.clear_frame(self.main_scroll)
        self.current_image_index = 0
        
        # Bind Keyboard Events
        self.bind("<Key>", self.handle_keypress)

        # Layout Grid
        self.main_scroll.grid_columnconfigure(0, weight=1)

        # 1. Area Gambar
        self.image_label = ctk.CTkLabel(self.main_scroll, text="")
        self.image_label.pack(pady=10, padx=10, expand=True)

        # 2. Info File
        self.file_info_label = ctk.CTkLabel(self.main_scroll, text="Nama File", font=("Roboto", 14))
        self.file_info_label.pack(pady=5)

        # 3. Kontrol Navigasi
        nav_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        nav_frame.pack(pady=10)
        
        ctk.CTkButton(nav_frame, text="< Sebelumnya", command=self.prev_image, fg_color="gray").pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Lewati / Selanjutnya >", command=self.next_image, fg_color="gray").pack(side="left", padx=10)

        # 4. Panel Tombol Shortcut (Visual Guide)
        shortcut_frame = ctk.CTkFrame(self.main_scroll, fg_color="#F0F0F0")
        shortcut_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(shortcut_frame, text="Shortcut Tersedia:", font=("Roboto", 14, "bold")).pack(pady=5)
        
        # Buat grid tombol visual
        grid_frame = ctk.CTkFrame(shortcut_frame, fg_color="transparent")
        grid_frame.pack(pady=10)
        
        for s_data in self.shortcuts_data:
            key = s_data["key"].upper()
            # Ambil nama folder target
            target_names = [self.folders_data[i]["name"] for i in s_data["targets"]]
            desc = " & ".join(target_names)
            
            btn_text = f"[{key}]\nSimpan ke:\n{desc}"
            
            # Tombol ini juga bisa diklik selain ditekan di keyboard
            btn = ctk.CTkButton(grid_frame, text=btn_text, 
                                command=lambda k=s_data["key"]: self.execute_sort(k),
                                width=150, height=60,
                                fg_color=NAVY_COLOR, hover_color=NAVY_HOVER)
            btn.pack(side="left", padx=10, pady=5)

        self.load_image()

    def load_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            file_name = self.image_files[self.current_image_index]
            file_path = os.path.join(self.source_folder, file_name)
            
            # Update Info
            self.file_info_label.configure(text=f"[{self.current_image_index + 1}/{len(self.image_files)}] {file_name}")
            
            # Load & Resize Image
            try:
                img = Image.open(file_path)
                
                # Hitung rasio resize agar muat di layar tapi tidak pecah
                # Max height 500px
                aspect_ratio = img.width / img.height
                new_height = 500
                new_width = int(new_height * aspect_ratio)
                
                my_image = ctk.CTkImage(light_image=img, dark_image=img, size=(new_width, new_height))
                self.image_label.configure(image=my_image)
            except Exception as e:
                self.file_info_label.configure(text=f"Error loading image: {e}")
        else:
            self.end_session()

    def handle_keypress(self, event):
        key = event.char.lower()
        # Cek apakah tombol yang ditekan ada di daftar shortcut
        for s in self.shortcuts_data:
            if s["key"] == key:
                self.execute_sort(key)
                break
                
    def execute_sort(self, key):
        # Cari konfigurasi shortcut
        shortcut = next((s for s in self.shortcuts_data if s["key"] == key), None)
        if not shortcut: return

        current_file = self.image_files[self.current_image_index]
        src_path = os.path.join(self.source_folder, current_file)

        # Lakukan penyalinan ke SEMUA folder target
        success_list = []
        for target_idx in shortcut["targets"]:
            dest_folder_info = self.folders_data[target_idx]
            dest_path = dest_folder_info["path"]
            
            try:
                shutil.copy2(src_path, dest_path) # copy2 menjaga metadata
                success_list.append(dest_folder_info["name"])
            except Exception as e:
                print(f"Gagal copy ke {dest_folder_info['name']}: {e}")

        # Feedback visual sebentar (opsional, bisa ditambah toast message)
        print(f"Berhasil simpan {current_file} ke: {', '.join(success_list)}")
        
        # Slide otomatis (Requirement 5)
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
        self.image_label.configure(image=None, text="SELESAI!\nSemua foto telah disortir.")
        self.unbind("<Key>") # Matikan keyboard shortcut

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = SortirFotoApp()
    app.mainloop()
