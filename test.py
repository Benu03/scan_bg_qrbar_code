import keyboard
import requests
import tkinter as tk
from tkinter import messagebox
import urllib3
import psutil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

barcode = ""
browser_opened = False  # Variabel untuk menyimpan status browser

def check_browser_open():
    global browser_opened
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'chrome.exe':  # Ganti dengan nama proses browser yang sesuai
            browser_opened = True
            return
    browser_opened = False

def on_key_event(event):
    global barcode, browser_opened
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "enter":
            # Pindai barcode selesai, kirim permintaan ke API jika browser sudah dibuka
            if browser_opened:
                print("Sending barcode:", barcode)
                send_request(barcode)
            else:
                print("Browser is not opened")
            # Reset nilai barcode untuk pindai selanjutnya
            barcode = ""
        else:
            # Tambahkan karakter ke nilai barcode
            barcode += event.name

# Mengecek status browser secara teratur
keyboard.add_hotkey('ctrl', check_browser_open)

def get_open_browser_url():
    # Ganti dengan URL spesifik yang ingin dicek
    specific_url = "https://idcak01iten081.puninar.com:9075"
    open_browsers = []
    for proc in psutil.process_iter(['pid']):
        try:
            p = psutil.Process(proc.info['pid'])
            if p.name().lower() == "chrome.exe":
                open_browsers.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    for browser in open_browsers:
        for conn in browser.connections():
            if conn.status == psutil.CONN_ESTABLISHED:
                if specific_url in conn.laddr.ip and conn.laddr.port in (80, 443):
                    return True
    return False

def send_request(barcode):
    # Buat payload sesuai dengan kebutuhan API
    payload = {
        'barcode': barcode
    }
    # Ganti URL dengan URL endpoint yang sesuai
    url = 'https://idcak01iten081.puninar.com:9075/barcode'
    try:
        # Kirim permintaan POST ke API
        response = requests.post(url, json=payload, verify=False)
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
    if get_open_browser_url():
        browser_opened = True
    else:
        browser_opened = False
    pass
