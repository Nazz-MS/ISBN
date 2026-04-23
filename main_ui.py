import tkinter as tk
try:
    import customtkinter as ctk
    USE_CTK = True
except ImportError:
    # Fallback to standard tkinter if customtkinter is not available
    from tkinter import messagebox
    USE_CTK = False

from isbn_logic import check_isbn_validity

if USE_CTK:
    # Konfigurasi tema customtkinter
    ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

    class ISBNValidatorApp(ctk.CTk):
        def __init__(self):
            super().__init__()

            # Konfigurasi Window
            self.title("ISBN-13 Validator")
            self.geometry("500x450")
            self.resizable(False, False)

            # Frame Utama
            self.main_frame = ctk.CTkFrame(self)
            self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

            # Judul Aplikasi
            self.label_title = ctk.CTkLabel(
                self.main_frame, 
                text="Pengecekan Validasi ISBN-13", 
                font=ctk.CTkFont(size=22, weight="bold")
            )
            self.label_title.pack(pady=(20, 10))

            # Instruksi
            self.label_instruction = ctk.CTkLabel(
                self.main_frame, 
                text="Masukkan 13 digit angka ISBN:",
                font=ctk.CTkFont(size=14)
            )
            self.label_instruction.pack(pady=(10, 5))

            # Input Entry
            self.entry_isbn = ctk.CTkEntry(
                self.main_frame, 
                placeholder_text="Contoh: 9781234567897",
                width=280,
                height=40,
                font=ctk.CTkFont(size=16)
            )
            self.entry_isbn.pack(pady=(0, 20))
            
            # Bind return key to validation
            self.entry_isbn.bind("<Return>", lambda event: self.validate_clicked())

            # Tombol Validasi
            self.btn_validate = ctk.CTkButton(
                self.main_frame, 
                text="Cek Validasi ISBN", 
                command=self.validate_clicked,
                font=ctk.CTkFont(size=15, weight="bold"),
                height=40
            )
            self.btn_validate.pack(pady=(0, 20))

            # Area Output Output
            self.frame_output = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.frame_output.pack(pady=10, fill="x", padx=20)

            # Label Status
            self.label_status = ctk.CTkLabel(
                self.frame_output, 
                text="", 
                font=ctk.CTkFont(size=20, weight="bold")
            )
            self.label_status.pack(pady=5)

            # Label Check Digit (Karakter Uji)
            self.label_check_digit = ctk.CTkLabel(
                self.frame_output, 
                text="", 
                font=ctk.CTkFont(size=15)
            )
            self.label_check_digit.pack(pady=2)

            # Label Error Message
            self.label_error = ctk.CTkLabel(
                self.frame_output, 
                text="", 
                text_color="red",
                font=ctk.CTkFont(size=13)
            )
            self.label_error.pack(pady=2)

        def validate_clicked(self):
            # 1. Ambil input dari user
            isbn_input = self.entry_isbn.get().strip()

            # 2. Reset tampilan output
            self.label_status.configure(text="")
            self.label_check_digit.configure(text="")
            self.label_error.configure(text="")

            # 3. Panggil logika validasi
            result = check_isbn_validity(isbn_input)

            # 4. Tampilkan hasil di UI
            if result["is_valid"]:
                self.label_status.configure(text="✅ ISBN Valid", text_color="#10B981") # Warna hijau custom
                self.label_check_digit.configure(text=f"Angka Karakter Uji Seharusnya: {result['expected_check_digit']}")
                self.label_error.configure(text="")
            else:
                self.label_status.configure(text="❌ ISBN Tidak Valid", text_color="#EF4444") # Warna merah custom
                
                # Tampilkan pesan error
                if result["error"]:
                    self.label_error.configure(text=result["error"])
                
                # Tampilkan karakter uji seharusnya jika format benar
                if result["expected_check_digit"] is not None:
                    self.label_check_digit.configure(text=f"Angka Karakter Uji Seharusnya: {result['expected_check_digit']}")
                else:
                    self.label_check_digit.configure(text="")

else:
    # Fallback Implementation using standard Tkinter
    class ISBNValidatorApp(tk.Tk):
        def __init__(self):
            super().__init__()

            self.title("ISBN-13 Validator")
            self.geometry("450x350")
            self.resizable(False, False)
            self.configure(padx=20, pady=20)

            # Judul Aplikasi
            tk.Label(
                self, 
                text="Pengecekan Validasi ISBN-13", 
                font=("Arial", 16, "bold")
            ).pack(pady=(10, 20))

            # Instruksi
            tk.Label(
                self, 
                text="Masukkan 13 digit angka ISBN:",
                font=("Arial", 12)
            ).pack(pady=(0, 5))

            # Input Entry
            self.entry_isbn = tk.Entry(self, font=("Arial", 14), width=25)
            self.entry_isbn.pack(pady=(0, 15))
            self.entry_isbn.bind("<Return>", lambda event: self.validate_clicked())

            # Tombol Validasi
            tk.Button(
                self, 
                text="Cek Validasi ISBN", 
                command=self.validate_clicked,
                font=("Arial", 12, "bold"),
                bg="#007BFF",
                fg="white",
                padx=10,
                pady=5
            ).pack(pady=(0, 20))

            # Output Frame
            self.frame_output = tk.Frame(self)
            self.frame_output.pack(fill="x")

            # Status Label
            self.label_status = tk.Label(self.frame_output, text="", font=("Arial", 16, "bold"))
            self.label_status.pack(pady=5)

            # Check Digit Label
            self.label_check_digit = tk.Label(self.frame_output, text="", font=("Arial", 12))
            self.label_check_digit.pack(pady=2)

            # Error Label
            self.label_error = tk.Label(self.frame_output, text="", font=("Arial", 11), fg="red")
            self.label_error.pack(pady=2)

        def validate_clicked(self):
            isbn_input = self.entry_isbn.get().strip()

            self.label_status.config(text="")
            self.label_check_digit.config(text="")
            self.label_error.config(text="")

            result = check_isbn_validity(isbn_input)

            if result["is_valid"]:
                self.label_status.config(text="✅ ISBN Valid", fg="green")
                self.label_check_digit.config(text=f"Angka Karakter Uji Seharusnya: {result['expected_check_digit']}")
            else:
                self.label_status.config(text="❌ ISBN Tidak Valid", fg="red")
                if result["error"]:
                    self.label_error.config(text=result["error"])
                if result["expected_check_digit"] is not None:
                    self.label_check_digit.config(text=f"Angka Karakter Uji Seharusnya: {result['expected_check_digit']}")

if __name__ == "__main__":
    app = ISBNValidatorApp()
    app.mainloop()
