import tkinter as tk
try:
    import customtkinter as ctk
    USE_CTK = True
except ImportError:
    from tkinter import messagebox
    USE_CTK = False

# ==========================================
# BAGIAN 1: LOGIKA MATEMATIKA (isbn_logic.py)
# ==========================================

def validate_format(isbn: str) -> bool:
    """Memastikan input memiliki panjang tepat 13 karakter dan semuanya berupa angka."""
    return len(isbn) == 13 and isbn.isdigit()

def calculate_check_digit(isbn_12: str) -> int:
    """Menghitung karakter uji (check digit) untuk 12 digit pertama ISBN."""
    total = 0
    for i in range(12):
        digit = int(isbn_12[i])
        weight = 1 if i % 2 == 0 else 3
        total += digit * weight
    remainder = total % 10
    check_digit = 10 - remainder
    if check_digit == 10:
        check_digit = 0
    return check_digit

def check_isbn_validity(isbn: str) -> dict:
    """Fungsi utama untuk memvalidasi ISBN-13 secara lengkap."""
    if not isbn:
        return {"is_valid": False, "error": "Input kosong.\nSilakan masukkan 13 digit ISBN.", "expected_check_digit": None}
    if not validate_format(isbn):
        return {"is_valid": False, "error": "Format salah.\nISBN harus persis 13 digit angka.", "expected_check_digit": None}
    if not (isbn.startswith("978") or isbn.startswith("979")):
        return {"is_valid": False, "error": "Format salah. ISBN-13 harus diawali\ndengan angka 978 atau 979.", "expected_check_digit": None}
    
    isbn_12 = isbn[:12]
    expected_check_digit = calculate_check_digit(isbn_12)
    actual_check_digit = int(isbn[12])
    
    if expected_check_digit == actual_check_digit:
        return {"is_valid": True, "error": None, "expected_check_digit": expected_check_digit}
    else:
        return {
            "is_valid": False,
            "error": f"Digit ke-13 salah!\nSeharusnya {expected_check_digit}, tapi diinput {actual_check_digit}.",
            "expected_check_digit": expected_check_digit
        }

def validate_format_10(isbn: str) -> bool:
    """Memastikan input memiliki panjang tepat 10 karakter (9 angka + 1 angka/X)."""
    if len(isbn) != 10:
        return False
    if not isbn[:9].isdigit():
        return False
    if not (isbn[9].isdigit() or isbn[9].upper() == 'X'):
        return False
    return True

def calculate_check_digit_10(isbn_9: str) -> str:
    """Menghitung karakter uji (check digit) untuk 9 digit pertama ISBN-10."""
    total = 0
    for i in range(9):
        digit = int(isbn_9[i])
        weight = 10 - i
        total += digit * weight
    remainder = total % 11
    check_digit = (11 - remainder) % 11
    if check_digit == 10:
        return 'X'
    return str(check_digit)

def check_isbn_10_validity(isbn: str) -> dict:
    """Fungsi utama untuk memvalidasi ISBN-10."""
    if not isbn:
        return {"is_valid": False, "error": "Input kosong.\nSilakan masukkan 10 digit ISBN.", "expected_check_digit": None}
    if not validate_format_10(isbn):
        return {"is_valid": False, "error": "Format salah. Masukkan 9 digit angka\ndiikuti 1 angka atau huruf X.", "expected_check_digit": None}
    
    isbn_9 = isbn[:9]
    expected_check_digit = calculate_check_digit_10(isbn_9)
    actual_check_digit = isbn[9].upper()
    
    if expected_check_digit == actual_check_digit:
        return {"is_valid": True, "error": None, "expected_check_digit": expected_check_digit}
    else:
        return {
            "is_valid": False,
            "error": f"Digit ke-10 salah!\nSeharusnya {expected_check_digit}, tapi diinput {actual_check_digit}.",
            "expected_check_digit": expected_check_digit
        }


# ==========================================
# BAGIAN 2: ANTARMUKA PENGGUNA (PREMIUM DARK & BLUE ACCENT)
# ==========================================

if USE_CTK:
    # --- IMPLEMENTASI CUSTOMTKINTER ---
    ctk.set_appearance_mode("Dark")
    
    # Skema Warna Modern (Dark theme elegan dengan aksen biru)
    BG_COLOR = "#111827"    # Dark slate blue/gray (Background luar)
    CARD_COLOR = "#1F2937"  # Lighter slate (Kartu di tengah)
    ACCENT = "#2563EB"      # Vibrant Modern Blue
    ACCENT_HOVER = "#1D4ED8"
    TEXT_MAIN = "#F9FAFB"
    TEXT_SUB = "#9CA3AF"
    ERROR_COLOR = "#EF4444"
    SUCCESS_COLOR = "#10B981"

    class ISBNValidatorApp(ctk.CTk):
        def __init__(self):
            super().__init__()

            self.title("ISBN-13 Validator")
            self.geometry("520x520")
            self.resizable(False, False)
            self.configure(fg_color=BG_COLOR)

            self.show_main_menu()

        def clear_window(self):
            for widget in self.winfo_children():
                widget.destroy()

        def draw_version_label(self):
            """Menampilkan teks versi aplikasi di sudut kiri bawah layar"""
            lbl_version = ctk.CTkLabel(
                self, text="v2.0.2", font=ctk.CTkFont(size=12, weight="bold"), text_color="#4B5563"
            )
            lbl_version.place(x=15, rely=1.0, anchor="sw", y=-10)

        def show_main_menu(self):
            """Halaman Menu Utama"""
            self.clear_window()
            
            main_frame = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=15, border_width=1, border_color="#374151")
            main_frame.pack(pady=40, padx=40, fill="both", expand=True)

            label_title = ctk.CTkLabel(
                main_frame, text="Aplikasi Validasi\nISBN", font=ctk.CTkFont(size=28, weight="bold"), text_color=TEXT_MAIN
            )
            label_title.pack(pady=(40, 30))

            btn_isbn13 = ctk.CTkButton(
                main_frame, text="ISBN-13", command=self.show_validator_13, font=ctk.CTkFont(size=18, weight="bold"), height=50,
                fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="white", corner_radius=8
            )
            btn_isbn13.pack(pady=(5, 10), fill="x", padx=50)

            btn_isbn10 = ctk.CTkButton(
                main_frame, text="ISBN-10", command=self.show_validator_10, font=ctk.CTkFont(size=18, weight="bold"), height=50,
                fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="white", corner_radius=8
            )
            btn_isbn10.pack(pady=(5, 15), fill="x", padx=50)

            btn_exit = ctk.CTkButton(
                main_frame, text="Keluar", command=self.destroy, font=ctk.CTkFont(size=18, weight="bold"), height=50, 
                fg_color="transparent", border_width=2, border_color=ERROR_COLOR, hover_color="#7F1D1D", text_color=ERROR_COLOR, corner_radius=8
            )
            btn_exit.pack(pady=(5, 10), fill="x", padx=50)

            self.draw_version_label()

        def show_validator_13(self):
            """Halaman Input Validasi ISBN-13"""
            self.clear_window()
            
            self.main_frame = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=15, border_width=1, border_color="#374151")
            self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

            self.label_title = ctk.CTkLabel(
                self.main_frame, text="Pengecekan Validasi ISBN-13", font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_MAIN
            )
            self.label_title.pack(pady=(25, 10))

            self.label_instruction = ctk.CTkLabel(
                self.main_frame, text="Masukkan 13 digit angka ISBN:", font=ctk.CTkFont(size=14), text_color=TEXT_SUB
            )
            self.label_instruction.pack(pady=(10, 5))

            self.entry_isbn = ctk.CTkEntry(
                self.main_frame, placeholder_text="Contoh: 9781234567897", width=290, height=45, font=ctk.CTkFont(size=16),
                fg_color=BG_COLOR, border_color=ACCENT, border_width=1.5, text_color=TEXT_MAIN, placeholder_text_color="#6B7280", corner_radius=8
            )
            self.entry_isbn.pack(pady=(0, 20))
            self.entry_isbn.bind("<Return>", lambda event: self.validate_clicked_13())

            self.btn_validate = ctk.CTkButton(
                self.main_frame, text="Cek Validasi ISBN", command=self.validate_clicked_13, font=ctk.CTkFont(size=15, weight="bold"), height=45,
                fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="white", corner_radius=8
            )
            self.btn_validate.pack(pady=(0, 10))
            
            self.btn_back = ctk.CTkButton(
                self.main_frame, text="← Kembali ke Menu", command=self.show_main_menu, font=ctk.CTkFont(size=13), 
                fg_color="transparent", text_color=TEXT_SUB, hover_color=BG_COLOR
            )
            self.btn_back.pack(pady=(0, 15))

            self.frame_output = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.frame_output.pack(pady=5, fill="x", padx=20)

            self.label_status = ctk.CTkLabel(self.frame_output, text="", font=ctk.CTkFont(size=20, weight="bold"))
            self.label_status.pack(pady=5)

            self.label_check_digit = ctk.CTkLabel(self.frame_output, text="", font=ctk.CTkFont(size=15), text_color=TEXT_MAIN)
            self.label_check_digit.pack(pady=2)

            self.label_error = ctk.CTkLabel(self.frame_output, text="", text_color=ERROR_COLOR, font=ctk.CTkFont(size=13), justify="center")
            self.label_error.pack(pady=2)

            self.draw_version_label()

        def validate_clicked_13(self):
            isbn_input = self.entry_isbn.get().strip()

            self.label_status.configure(text="")
            self.label_check_digit.configure(text="")
            self.label_error.configure(text="")

            result = check_isbn_validity(isbn_input)

            if result["is_valid"]:
                self.label_status.configure(text="✅ ISBN Valid", text_color=SUCCESS_COLOR)
                self.label_check_digit.configure(text=f"Angka Karakter Uji: {result['expected_check_digit']}")
            else:
                self.label_status.configure(text="❌ ISBN Tidak Valid", text_color=ERROR_COLOR)
                if result["error"]:
                    self.label_error.configure(text=result["error"])
                if result["expected_check_digit"] is not None:
                    self.label_check_digit.configure(text=f"Angka Karakter Uji Seharusnya: {result['expected_check_digit']}")
                else:
                    self.label_check_digit.configure(text="")

        def show_validator_10(self):
            """Halaman Input Validasi ISBN-10"""
            self.clear_window()
            
            self.main_frame = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=15, border_width=1, border_color="#374151")
            self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

            self.label_title = ctk.CTkLabel(
                self.main_frame, text="Pengecekan Validasi ISBN-10", font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_MAIN
            )
            self.label_title.pack(pady=(25, 10))

            self.label_instruction = ctk.CTkLabel(
                self.main_frame, text="Masukkan 10 digit ISBN:", font=ctk.CTkFont(size=14), text_color=TEXT_SUB
            )
            self.label_instruction.pack(pady=(10, 5))

            self.entry_isbn = ctk.CTkEntry(
                self.main_frame, placeholder_text="Contoh: 0136091814", width=290, height=45, font=ctk.CTkFont(size=16),
                fg_color=BG_COLOR, border_color=ACCENT, border_width=1.5, text_color=TEXT_MAIN, placeholder_text_color="#6B7280", corner_radius=8
            )
            self.entry_isbn.pack(pady=(0, 20))
            self.entry_isbn.bind("<Return>", lambda event: self.validate_clicked_10())

            self.btn_validate = ctk.CTkButton(
                self.main_frame, text="Cek Validasi ISBN", command=self.validate_clicked_10, font=ctk.CTkFont(size=15, weight="bold"), height=45,
                fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="white", corner_radius=8
            )
            self.btn_validate.pack(pady=(0, 10))
            
            self.btn_back = ctk.CTkButton(
                self.main_frame, text="← Kembali ke Menu", command=self.show_main_menu, font=ctk.CTkFont(size=13), 
                fg_color="transparent", text_color=TEXT_SUB, hover_color=BG_COLOR
            )
            self.btn_back.pack(pady=(0, 15))

            self.frame_output = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.frame_output.pack(pady=5, fill="x", padx=20)

            self.label_status = ctk.CTkLabel(self.frame_output, text="", font=ctk.CTkFont(size=20, weight="bold"))
            self.label_status.pack(pady=5)

            self.label_check_digit = ctk.CTkLabel(self.frame_output, text="", font=ctk.CTkFont(size=15), text_color=TEXT_MAIN)
            self.label_check_digit.pack(pady=2)

            self.label_error = ctk.CTkLabel(self.frame_output, text="", text_color=ERROR_COLOR, font=ctk.CTkFont(size=13), justify="center")
            self.label_error.pack(pady=2)

            self.draw_version_label()

        def validate_clicked_10(self):
            isbn_input = self.entry_isbn.get().strip()

            self.label_status.configure(text="")
            self.label_check_digit.configure(text="")
            self.label_error.configure(text="")

            result = check_isbn_10_validity(isbn_input)

            if result["is_valid"]:
                self.label_status.configure(text="✅ ISBN Valid", text_color=SUCCESS_COLOR)
                self.label_check_digit.configure(text=f"Angka Karakter Uji: {result['expected_check_digit']}")
            else:
                self.label_status.configure(text="❌ ISBN Tidak Valid", text_color=ERROR_COLOR)
                if result["error"]:
                    self.label_error.configure(text=result["error"])
                if result["expected_check_digit"] is not None:
                    self.label_check_digit.configure(text=f"Angka Karakter Uji Seharusnya: {result['expected_check_digit']}")
                else:
                    self.label_check_digit.configure(text="")

else:
    # --- FALLBACK IMPLEMENTASI TKINTER STANDAR ---
    class ISBNValidatorApp(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("ISBN-13 Validator")
            self.geometry("450x420")
            self.resizable(False, False)
            self.configure(bg="#111827")
            
            self.show_main_menu()

        def clear_window(self):
            for widget in self.winfo_children():
                widget.destroy()

        def draw_version_label(self):
            tk.Label(self, text="v2.0.2", font=("Arial", 10, "bold"), fg="#4B5563", bg="#111827").place(x=10, rely=1.0, anchor="sw", y=-5)

        def show_main_menu(self):
            self.clear_window()
            
            frame = tk.Frame(self, bg="#1F2937", bd=1, relief="ridge")
            frame.pack(expand=True, fill="both", padx=30, pady=30)
            
            tk.Label(frame, text="Aplikasi Validasi\nISBN", font=("Arial", 22, "bold"), bg="#1F2937", fg="#F9FAFB").pack(pady=(20, 20))
            
            tk.Button(
                frame, text="ISBN-13", command=self.show_validator_13, font=("Arial", 14, "bold"), bg="#2563EB", fg="white", width=20, pady=10, relief="flat"
            ).pack(pady=5)

            tk.Button(
                frame, text="ISBN-10", command=self.show_validator_10, font=("Arial", 14, "bold"), bg="#2563EB", fg="white", width=20, pady=10, relief="flat"
            ).pack(pady=5)
            
            tk.Button(
                frame, text="Keluar", command=self.destroy, font=("Arial", 14, "bold"), bg="#111827", fg="#EF4444", width=20, pady=10, relief="flat"
            ).pack(pady=10)
            
            self.draw_version_label()

        def show_validator_13(self):
            self.clear_window()
            
            frame = tk.Frame(self, bg="#1F2937", bd=1, relief="ridge")
            frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            tk.Label(frame, text="Pengecekan Validasi ISBN-13", font=("Arial", 16, "bold"), bg="#1F2937", fg="#F9FAFB").pack(pady=(15, 10))
            tk.Label(frame, text="Masukkan 13 digit angka ISBN:", font=("Arial", 12), bg="#1F2937", fg="#9CA3AF").pack(pady=(0, 5))

            self.entry_isbn = tk.Entry(frame, font=("Arial", 14), width=25, bg="#111827", fg="#F9FAFB", insertbackground="white")
            self.entry_isbn.pack(pady=(0, 10))
            self.entry_isbn.bind("<Return>", lambda event: self.validate_clicked_13())

            tk.Button(
                frame, text="Cek Validasi ISBN", command=self.validate_clicked_13, font=("Arial", 12, "bold"), bg="#2563EB", fg="white", padx=10, pady=5, relief="flat"
            ).pack(pady=(0, 10))
            
            tk.Button(
                frame, text="← Kembali ke Menu Utama", command=self.show_main_menu, font=("Arial", 10), bg="#1F2937", fg="#2563EB", relief="flat", cursor="hand2"
            ).pack(pady=(0, 10))

            self.frame_output = tk.Frame(frame, bg="#1F2937")
            self.frame_output.pack(fill="x")

            self.label_status = tk.Label(self.frame_output, text="", font=("Arial", 14, "bold"), bg="#1F2937")
            self.label_status.pack(pady=5)

            self.label_check_digit = tk.Label(self.frame_output, text="", font=("Arial", 11), bg="#1F2937", fg="#F9FAFB")
            self.label_check_digit.pack(pady=2)

            self.label_error = tk.Label(self.frame_output, text="", font=("Arial", 10), bg="#1F2937", fg="#EF4444", justify="center")
            self.label_error.pack(pady=2)

            self.draw_version_label()

        def validate_clicked_13(self):
            isbn_input = self.entry_isbn.get().strip()

            self.label_status.config(text="")
            self.label_check_digit.config(text="")
            self.label_error.config(text="")

            result = check_isbn_validity(isbn_input)

            if result["is_valid"]:
                self.label_status.config(text="✅ ISBN Valid", fg="#10B981")
                self.label_check_digit.config(text=f"Angka Karakter Uji: {result['expected_check_digit']}")
            else:
                self.label_status.config(text="❌ ISBN Tidak Valid", fg="#EF4444")
                if result["error"]:
                    self.label_error.config(text=result["error"])
                if result["expected_check_digit"] is not None:
                    self.label_check_digit.config(text=f"Angka Karakter Uji Seharusnya: {result['expected_check_digit']}")

        def show_validator_10(self):
            self.clear_window()
            
            frame = tk.Frame(self, bg="#1F2937", bd=1, relief="ridge")
            frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            tk.Label(frame, text="Pengecekan Validasi ISBN-10", font=("Arial", 16, "bold"), bg="#1F2937", fg="#F9FAFB").pack(pady=(15, 10))
            tk.Label(frame, text="Masukkan 10 digit ISBN:", font=("Arial", 12), bg="#1F2937", fg="#9CA3AF").pack(pady=(0, 5))

            self.entry_isbn = tk.Entry(frame, font=("Arial", 14), width=25, bg="#111827", fg="#F9FAFB", insertbackground="white")
            self.entry_isbn.pack(pady=(0, 10))
            self.entry_isbn.bind("<Return>", lambda event: self.validate_clicked_10())

            tk.Button(
                frame, text="Cek Validasi ISBN", command=self.validate_clicked_10, font=("Arial", 12, "bold"), bg="#2563EB", fg="white", padx=10, pady=5, relief="flat"
            ).pack(pady=(0, 10))
            
            tk.Button(
                frame, text="← Kembali ke Menu Utama", command=self.show_main_menu, font=("Arial", 10), bg="#1F2937", fg="#2563EB", relief="flat", cursor="hand2"
            ).pack(pady=(0, 10))

            self.frame_output = tk.Frame(frame, bg="#1F2937")
            self.frame_output.pack(fill="x")

            self.label_status = tk.Label(self.frame_output, text="", font=("Arial", 14, "bold"), bg="#1F2937")
            self.label_status.pack(pady=5)

            self.label_check_digit = tk.Label(self.frame_output, text="", font=("Arial", 11), bg="#1F2937", fg="#F9FAFB")
            self.label_check_digit.pack(pady=2)

            self.label_error = tk.Label(self.frame_output, text="", font=("Arial", 10), bg="#1F2937", fg="#EF4444", justify="center")
            self.label_error.pack(pady=2)

            self.draw_version_label()

        def validate_clicked_10(self):
            isbn_input = self.entry_isbn.get().strip()

            self.label_status.config(text="")
            self.label_check_digit.config(text="")
            self.label_error.config(text="")

            result = check_isbn_10_validity(isbn_input)

            if result["is_valid"]:
                self.label_status.config(text="✅ ISBN Valid", fg="#10B981")
                self.label_check_digit.config(text=f"Angka Karakter Uji: {result['expected_check_digit']}")
            else:
                self.label_status.config(text="❌ ISBN Tidak Valid", fg="#EF4444")
                if result["error"]:
                    self.label_error.config(text=result["error"])
                if result["expected_check_digit"] is not None:
                    self.label_check_digit.config(text=f"Angka Karakter Uji Seharusnya: {result['expected_check_digit']}")

if __name__ == "__main__":
    app = ISBNValidatorApp()
    app.mainloop()
