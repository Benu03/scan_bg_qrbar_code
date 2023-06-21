import keyboard
import requests
import tkinter as tk
from tkinter import messagebox
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        'packer'    : 'PACKER-002',
        'scan_value': barcode
    }
    # Ganti URL dengan URL endpoint yang sesuai
    url = 'https://dev-cloud.puninar.com:8029/api/hik/barcode-validate'
    try:
        # Kirim permintaan POST ke API
        response = requests.post(url, json=payload,verify=False)
        if response.status_code == 200:
            print("Request successful")
        else:
            print("Request failed with status code:", response.status_code)
            # messagebox.showerror(f"Request Failed status code: {response.status_code}", f"Data Request Failed : {barcode}")
           
           

    except requests.exceptions.RequestException as e:
        print("An error occurred:", str(e))
        

# Mendaftarkan fungsi on_key_event() sebagai event handler
keyboard.on_press(on_key_event)

# Loop terus-menerus untuk menjaga program tetap berjalan
while True:
    pass