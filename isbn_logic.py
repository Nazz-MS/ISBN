# isbn_logic.py

def validate_format(isbn: str) -> bool:
    """
    Memastikan input memiliki panjang tepat 13 karakter dan semuanya berupa angka.
    """
    return len(isbn) == 13 and isbn.isdigit()

def calculate_check_digit(isbn_12: str) -> int:
    """
    Menghitung karakter uji (check digit) untuk 12 digit pertama ISBN.
    
    Rumus:
    1. Ambil 12 digit pertama.
    2. Kalikan secara bergantian dengan bobot 1 dan 3.
    3. Jumlahkan hasil perkalian tersebut.
    4. Sisa bagi jumlah tersebut dengan 10.
    5. Karakter uji adalah 10 dikurangi sisa bagi (jika sisa bagi 0, maka karakter uji 0).
    """
    total = 0
    for i in range(12):
        digit = int(isbn_12[i])
        # Alternasi pembobot 1 dan 3
        # Jika indeks genap (0, 2, 4...) pembobotnya 1
        # Jika indeks ganjil (1, 3, 5...) pembobotnya 3
        weight = 1 if i % 2 == 0 else 3
        total += digit * weight
    
    remainder = total % 10
    check_digit = 10 - remainder
    
    if check_digit == 10:
        check_digit = 0
        
    return check_digit

def check_isbn_validity(isbn: str) -> dict:
    """
    Fungsi utama untuk memvalidasi ISBN-13 secara lengkap.
    Mengembalikan dictionary berisi status, pesan error, dan karakter uji yang seharusnya.
    """
    # 1. Validasi format
    if not isbn:
        return {"is_valid": False, "error": "Input kosong. Silakan masukkan 13 digit ISBN.", "expected_check_digit": None}
    
    if not validate_format(isbn):
        return {"is_valid": False, "error": "Format salah. ISBN harus persis 13 digit angka (tanpa huruf/spasi/simbol).", "expected_check_digit": None}
    
    # 2. Hitung karakter uji yang seharusnya
    isbn_12 = isbn[:12]
    expected_check_digit = calculate_check_digit(isbn_12)
    
    # 3. Bandingkan dengan digit ke-13 (check digit aktual)
    actual_check_digit = int(isbn[12])
    
    if expected_check_digit == actual_check_digit:
        return {
            "is_valid": True,
            "error": None,
            "expected_check_digit": expected_check_digit
        }
    else:
        return {
            "is_valid": False,
            "error": f"Digit terakhir salah. Seharusnya {expected_check_digit}, tapi diinput {actual_check_digit}.",
            "expected_check_digit": expected_check_digit
        }
