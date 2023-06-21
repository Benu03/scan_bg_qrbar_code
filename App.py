import keyboard
import requests
import tkinter as tk


barcode = ""

def on_key_event(event):
    global barcode
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "enter":
            # Pindai barcode selesai, kirim permintaan ke API
            print("Sending barcode:", barcode)
            send_request(barcode)
            # Reset nilai barcode untuk pindai selanjutnya
            barcode = ""
        else:
            # Tambahkan karakter ke nilai barcode
            barcode += event.name

def send_request(barcode):
    # Buat payload sesuai dengan kebutuhan API
    payload = {
        'barcode': barcode
    }
    # Ganti URL dengan URL endpoint yang sesuai
    url = 'https://idcak01iten081.puninar.com:9075/barcode'
    try:
        # Kirim permintaan POST ke API
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Request successful")
        else:
            print("Request failed with status code:", response.status_code)
            show_error_popup(f"Failed Status Code {response.status_code}", f"Data Request Failed Update : {barcode}")
    except requests.exceptions.RequestException as e:
        show_error_popup("Error", str(e))

def close_popup(popup):
    popup.destroy()

def show_error_popup(title, message, timeout=3000):
    root = tk.Tk()
    root.withdraw()

    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("350x80")
    popup.resizable(False, False)

    label = tk.Label(popup, text=message)
    label.pack(pady=10)

    # Menutup jendela pesan error setelah jangka waktu tertentu
    popup.after(timeout, lambda: close_popup(popup))

    # Menempatkan jendela pesan error di tengah layar
    popup.update_idletasks()
    popup_width = popup.winfo_width()
    popup_height = popup.winfo_height()
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width // 2) - (popup_width // 2)
    y = (screen_height // 2) - (popup_height // 2)
    popup.geometry(f"+{x}+{y}")

    popup.mainloop()

# Mendaftarkan fungsi on_key_event() sebagai event handler
keyboard.on_press(on_key_event)


# Loop utama tanpa menggunakan jendela utama
while True:
    # Tambahkan logika atau pekerjaan lain yang diperlukan di sini
    pass
