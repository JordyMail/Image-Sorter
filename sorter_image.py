import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from PIL import Image, ImageTk
import json
import keyboard
from pathlib import Path

class ImageSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Penyortir Gambar")
        self.root.geometry("1200x800")
        
        # Variabel untuk menyimpan data
        self.source_folder = ""
        self.destination_folders = []
        self.image_files = []
        self.current_image_index = 0
        self.folder_configs = []
        self.shortcut_configs = {}
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Frame untuk konfigurasi awal
        self.config_frame = ttk.LabelFrame(self.root, text="Konfigurasi Awal", padding=10)
        self.config_frame.pack(fill="x", padx=10, pady=5)
        
        # Tombol pilih folder sumber
        ttk.Button(self.config_frame, text="Pilih Folder Foto", 
                  command=self.select_source_folder).grid(row=0, column=0, padx=5, pady=5)
        
        self.source_label = ttk.Label(self.config_frame, text="Belum ada folder dipilih")
        self.source_label.grid(row=0, column=1, padx=5, pady=5)
        
        # Frame untuk konfigurasi folder tujuan
        self.dest_frame = ttk.LabelFrame(self.root, text="Konfigurasi Folder Tujuan", padding=10)
        self.dest_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.dest_frame, text="Jumlah Folder:").grid(row=0, column=0, padx=5, pady=5)
        self.folder_count = tk.IntVar(value=2)
        ttk.Spinbox(self.dest_frame, from_=1, to=10, textvariable=self.folder_count, 
                   width=10).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.dest_frame, text="Buat Konfigurasi", 
                  command=self.create_folder_config).grid(row=0, column=2, padx=5, pady=5)
        
        # Frame untuk konfigurasi fungsi tombol
        self.function_frame = ttk.LabelFrame(self.root, text="Konfigurasi Fungsi Tombol", padding=10)
        self.function_frame.pack(fill="x", padx=10, pady=5)
        
        # Frame untuk menampilkan gambar
        self.image_frame = ttk.LabelFrame(self.root, text="Preview Gambar", padding=10)
        self.image_frame.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.image_label = ttk.Label(self.image_frame, text="Silakan pilih folder foto terlebih dahulu")
        self.image_label.pack(expand=True, fill="both")
        
        # Frame untuk informasi gambar
        self.info_frame = ttk.Frame(self.image_frame)
        self.info_frame.pack(fill="x", pady=5)
        
        self.image_info_label = ttk.Label(self.info_frame, text="")
        self.image_info_label.pack()
        
        # Frame untuk tombol aksi
        self.action_frame = ttk.LabelFrame(self.root, text="Tombol Aksi", padding=10)
        self.action_frame.pack(fill="x", padx=10, pady=5)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Siap", relief=tk.SUNKEN)
        self.status_bar.pack(fill="x", padx=10, pady=5)
        
    def select_source_folder(self):
        folder = filedialog.askdirectory(title="Pilih Folder yang Berisi Foto")
        if folder:
            self.source_folder = folder
            self.source_label.config(text=f"Folder: {folder}")
            self.load_images()
            self.update_status(f"Folder sumber: {folder}")
    
    def load_images(self):
        """Muat semua file gambar dari folder sumber"""
        extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
        self.image_files = []
        
        try:
            for file in os.listdir(self.source_folder):
                if file.lower().endswith(extensions):
                    self.image_files.append(os.path.join(self.source_folder, file))
            
            self.image_files.sort()
            self.current_image_index = 0
            
            if self.image_files:
                self.show_current_image()
                self.update_status(f"Ditemukan {len(self.image_files)} gambar")
            else:
                self.image_label.config(text="Tidak ada gambar ditemukan dalam folder")
                self.update_status("Tidak ada gambar ditemukan")
                
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat gambar: {str(e)}")
    
    def create_folder_config(self):
        """Membuat konfigurasi folder tujuan"""
        count = self.folder_count.get()
        self.destination_folders = []
        self.folder_configs = []
        
        # Buat dialog untuk memilih folder
        dialog = tk.Toplevel(self.root)
        dialog.title("Pilih Folder Tujuan")
        dialog.geometry("600x400")
        
        ttk.Label(dialog, text=f"Pilih {count} folder tujuan:", 
                 font=("Arial", 12)).pack(pady=10)
        
        frame = ttk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        folder_entries = []
        
        for i in range(count):
            ttk.Label(frame, text=f"Folder {chr(65+i)}:").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            folder_entries.append(entry)
            
            ttk.Button(frame, text="Browse", 
                      command=lambda e=entry: self.browse_folder(e)).grid(row=i, column=2, padx=5, pady=5)
        
        ttk.Button(dialog, text="Simpan Konfigurasi", 
                  command=lambda: self.save_folder_config(dialog, folder_entries)).pack(pady=20)
        
        # Reset konfigurasi shortcut sebelumnya
        self.shortcut_configs = {}
        
    def browse_folder(self, entry):
        """Membuka dialog untuk memilih folder"""
        folder = filedialog.askdirectory(title="Pilih Folder")
        if folder:
            entry.delete(0, tk.END)
            entry.insert(0, folder)
    
    def save_folder_config(self, dialog, entries):
        """Menyimpan konfigurasi folder tujuan"""
        self.destination_folders = []
        self.folder_configs = []
        
        for i, entry in enumerate(entries):
            folder_path = entry.get().strip()
            if folder_path:
                if os.path.exists(folder_path):
                    folder_name = f"Folder {chr(65+i)}"
                    self.destination_folders.append((folder_name, folder_path))
                    self.folder_configs.append({
                        'name': folder_name,
                        'path': folder_path,
                        'shortcut': str(i+1)
                    })
                else:
                    messagebox.showerror("Error", f"Folder {folder_path} tidak ditemukan!")
                    return
            else:
                messagebox.showerror("Error", f"Folder {chr(65+i)} belum dipilih!")
                return
        
        dialog.destroy()
        self.create_button_config()
        self.update_status(f"Berhasil mengkonfigurasi {len(self.destination_folders)} folder tujuan")
    
    def create_button_config(self):
        """Membuat konfigurasi fungsi tombol"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Konfigurasi Fungsi Tombol")
        dialog.geometry("800x600")
        
        ttk.Label(dialog, text="Konfigurasi Fungsi Tombol Keyboard", 
                 font=("Arial", 14)).pack(pady=10)
        
        # Frame untuk daftar tombol
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Buat konfigurasi tombol default
        self.button_configs = []
        
        # Tombol untuk masing-masing folder
        for i, (folder_name, folder_path) in enumerate(self.destination_folders):
            config = {
                'id': len(self.button_configs) + 1,
                'name': f"Tombol {len(self.button_configs) + 1}",
                'shortcut': str(len(self.button_configs) + 1),
                'action': [folder_name],
                'description': f"Simpan ke {folder_name}"
            }
            self.button_configs.append(config)
        
        # Tombol untuk kombinasi
        if len(self.destination_folders) >= 2:
            # Semua folder
            all_folders = [f[0] for f in self.destination_folders]
            config = {
                'id': len(self.button_configs) + 1,
                'name': f"Tombol {len(self.button_configs) + 1}",
                'shortcut': str(len(self.button_configs) + 1),
                'action': all_folders,
                'description': f"Simpan ke semua folder"
            }
            self.button_configs.append(config)
            
            # Kombinasi folder pertama dan kedua
            if len(self.destination_folders) >= 2:
                config = {
                    'id': len(self.button_configs) + 1,
                    'name': f"Tombol {len(self.button_configs) + 1}",
                    'shortcut': str(len(self.button_configs) + 1),
                    'action': [self.destination_folders[0][0], self.destination_folders[1][0]],
                    'description': f"Simpan ke {self.destination_folders[0][0]} dan {self.destination_folders[1][0]}"
                }
                self.button_configs.append(config)
            
            # Kombinasi folder kedua dan ketiga
            if len(self.destination_folders) >= 3:
                config = {
                    'id': len(self.button_configs) + 1,
                    'name': f"Tombol {len(self.button_configs) + 1}",
                    'shortcut': str(len(self.button_configs) + 1),
                    'action': [self.destination_folders[1][0], self.destination_folders[2][0]],
                    'description': f"Simpan ke {self.destination_folders[1][0]} dan {self.destination_folders[2][0]}"
                }
                self.button_configs.append(config)
        
        # Tampilkan konfigurasi yang dapat diedit
        columns = ('ID', 'Shortcut', 'Deskripsi', 'Aksi')
        tree = ttk.Treeview(button_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(button_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Isi data
        for config in self.button_configs:
            tree.insert('', tk.END, values=(
                config['id'],
                config['shortcut'],
                config['description'],
                ', '.join(config['action'])
            ))
        
        # Frame untuk menambah konfigurasi custom
        custom_frame = ttk.LabelFrame(dialog, text="Tambah Konfigurasi Custom", padding=10)
        custom_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(custom_frame, text="Pilih folder tujuan:").grid(row=0, column=0, padx=5, pady=5)
        
        # Variabel untuk checkbox
        self.folder_vars = []
        for i, (folder_name, folder_path) in enumerate(self.destination_folders):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(custom_frame, text=folder_name, variable=var)
            cb.grid(row=i+1, column=0, sticky="w", padx=20)
            self.folder_vars.append((folder_name, var))
        
        ttk.Label(custom_frame, text="Shortcut keyboard:").grid(row=0, column=1, padx=5, pady=5)
        shortcut_entry = ttk.Entry(custom_frame, width=10)
        shortcut_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(custom_frame, text="Tambah Konfigurasi", 
                  command=lambda: self.add_custom_config(shortcut_entry, tree)).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(dialog, text="Simpan Konfigurasi Tombol", 
                  command=lambda: self.save_button_config(dialog)).pack(pady=20)
    
    def add_custom_config(self, shortcut_entry, tree):
        """Menambah konfigurasi custom"""
        selected_folders = []
        for folder_name, var in self.folder_vars:
            if var.get():
                selected_folders.append(folder_name)
        
        if not selected_folders:
            messagebox.showwarning("Peringatan", "Pilih minimal satu folder tujuan!")
            return
        
        shortcut = shortcut_entry.get().strip()
        if not shortcut:
            messagebox.showwarning("Peringatan", "Masukkan shortcut keyboard!")
            return
        
        # Cek duplikasi shortcut
        for config in self.button_configs:
            if config['shortcut'] == shortcut:
                messagebox.showwarning("Peringatan", f"Shortcut '{shortcut}' sudah digunakan!")
                return
        
        config = {
            'id': len(self.button_configs) + 1,
            'name': f"Tombol {len(self.button_configs) + 1}",
            'shortcut': shortcut,
            'action': selected_folders,
            'description': f"Simpan ke {', '.join(selected_folders)}"
        }
        
        self.button_configs.append(config)
        
        # Update tree
        tree.insert('', tk.END, values=(
            config['id'],
            config['shortcut'],
            config['description'],
            ', '.join(config['action'])
        ))
        
        shortcut_entry.delete(0, tk.END)
        messagebox.showinfo("Sukses", "Konfigurasi custom berhasil ditambahkan!")
    
    def save_button_config(self, dialog):
        """Menyimpan konfigurasi tombol dan mengaktifkan shortcut"""
        # Hapus shortcut sebelumnya
        try:
            keyboard.unhook_all()
        except:
            pass
        
        # Setup shortcut baru
        for config in self.button_configs:
            shortcut = config['shortcut']
            action = config['action']
            
            try:
                keyboard.add_hotkey(shortcut, lambda a=action: self.save_to_folders(a))
                self.shortcut_configs[shortcut] = action
            except Exception as e:
                print(f"Gagal setup shortcut {shortcut}: {e}")
        
        # Buat tombol GUI
        for widget in self.action_frame.winfo_children():
            widget.destroy()
        
        # Buat tombol berdasarkan konfigurasi
        for i, config in enumerate(self.button_configs):
            btn_text = f"{config['shortcut']}: {config['description']}"
            btn = ttk.Button(self.action_frame, text=btn_text, 
                           command=lambda a=config['action']: self.save_to_folders(a))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
        
        dialog.destroy()
        
        self.update_status(f"Berhasil mengkonfigurasi {len(self.button_configs)} tombol shortcut")
        messagebox.showinfo("Sukses", f"Konfigurasi tombol berhasil disimpan!\n\nShortcut keyboard:\n" + 
                          "\n".join([f"Tombol {c['shortcut']}: {c['description']}" for c in self.button_configs]))
    
    def save_to_folders(self, folder_names):
        """Menyimpan gambar ke folder yang dipilih"""
        if not self.image_files or self.current_image_index >= len(self.image_files):
            messagebox.showinfo("Info", "Tidak ada gambar untuk diproses")
            return
        
        current_image = self.image_files[self.current_image_index]
        filename = os.path.basename(current_image)
        
        saved_count = 0
        for folder_name in folder_names:
            # Cari path folder berdasarkan nama
            dest_path = None
            for name, path in self.destination_folders:
                if name == folder_name:
                    dest_path = path
                    break
            
            if dest_path:
                try:
                    dest_file = os.path.join(dest_path, filename)
                    shutil.copy2(current_image, dest_file)
                    saved_count += 1
                except Exception as e:
                    print(f"Gagal menyimpan ke {folder_name}: {e}")
        
        if saved_count > 0:
            self.update_status(f"✓ Berhasil menyimpan ke {saved_count} folder: {filename}")
            self.next_image()
        else:
            self.update_status(f"✗ Gagal menyimpan: {filename}")
    
    def next_image(self):
        """Menampilkan gambar berikutnya"""
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.show_current_image()
        else:
            self.update_status("✓ Selesai! Semua gambar telah diproses")
            messagebox.showinfo("Selesai", "Semua gambar telah diproses!")
    
    def previous_image(self):
        """Menampilkan gambar sebelumnya"""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_current_image()
    
    def show_current_image(self):
        """Menampilkan gambar saat ini"""
        if not self.image_files:
            return
        
        try:
            image_path = self.image_files[self.current_image_index]
            filename = os.path.basename(image_path)
            
            # Buka dan resize gambar
            image = Image.open(image_path)
            
            # Dapatkan ukuran frame
            self.image_frame.update_idletasks()
            frame_width = self.image_frame.winfo_width() - 50
            frame_height = self.image_frame.winfo_height() - 100
            
            # Resize gambar
            image.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo
            
            # Update informasi
            total_images = len(self.image_files)
            self.image_info_label.config(
                text=f"Gambar {self.current_image_index + 1} dari {total_images} | {filename}"
            )
            
        except Exception as e:
            self.image_label.config(text=f"Error memuat gambar: {str(e)}")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def on_closing(self):
        """Handler saat aplikasi ditutup"""
        try:
            keyboard.unhook_all()
        except:
            pass
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ImageSorterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
