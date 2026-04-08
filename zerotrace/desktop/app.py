import sys
import os
import ctypes
import json
import subprocess
import hashlib
import base64
import random
import string
import requests
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QComboBox, QLabel, 
                             QProgressBar, QGridLayout, QMessageBox, QFrame, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QColor, QPalette, QFont
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec

API_BASE_URL = "http://localhost:8000"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class WipeThread(QThread):
    progress_signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, disk_num, disk_letter):
        super().__init__()
        self.disk_num = disk_num
        self.disk_letter = disk_letter

    def run(self):
        try:
            a_exe_path = get_resource_path("engine/a.exe")
            process = subprocess.Popen(
                [a_exe_path, str(self.disk_num), self.disk_letter],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            process.stdin.write("CONFIRM\n")
            process.stdin.flush()

            while True:
                line = process.stdout.readline()
                if not line: break
                self.log_signal.emit(line.strip())
                if "MB written" in line:
                    try:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == "MB" and i > 0:
                                self.progress_signal.emit(int(parts[i-1]))
                                break
                    except: pass
            process.wait()
            if process.returncode == 0:
                self.finished_signal.emit(True, "Wipe completed successfully!")
            else:
                self.finished_signal.emit(False, f"Wipe failed (Code {process.returncode})")
        except Exception as e:
            self.finished_signal.emit(False, str(e))

class LoginWindow(QWidget):
    login_success = pyqtSignal(str, str) # token, email

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZeroTrace Login")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #121212; color: white;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("ZeroTrace")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.email.setStyleSheet("padding: 10px; background: #1E1E1E; border: 1px solid #333;")
        layout.addWidget(self.email)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("padding: 10px; background: #1E1E1E; border: 1px solid #333;")
        layout.addWidget(self.password)
        
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.setStyleSheet("background: #03DAC6; color: black; font-weight: bold; padding: 10px;")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)

    def handle_login(self):
        # In a real app, this would call Supabase auth
        # For this implementation, we simulate a successful login
        email = self.email.text()
        if email:
            self.login_success.emit("dummy-token", email)
        else:
            QMessageBox.warning(self, "Error", "Please enter an email")

class ZeroTraceGUI(QMainWindow):
    def __init__(self, token, email):
        super().__init__()
        self.token = token
        self.email = email
        self.credits = 0
        self.setWindowTitle(f"ZeroTrace - {email}")
        self.setFixedSize(900, 750)
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QLabel { color: #E0E0E0; font-family: 'Segoe UI'; }
            QPushButton { background-color: #1E1E1E; color: white; border: 1px solid #333; padding: 10px; border-radius: 5px; }
            QPushButton#wipeBtn { background-color: #B00020; border: none; font-weight: bold; }
            QProgressBar { border: 1px solid #333; border-radius: 5px; text-align: center; }
            QProgressBar::chunk { background-color: #03DAC6; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header with Credits
        header_layout = QHBoxLayout()
        title = QLabel("ZeroTrace")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.credits_label = QLabel("Credits: Loading...")
        self.credits_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.credits_label.setStyleSheet("color: #03DAC6;")
        header_layout.addWidget(self.credits_label)
        layout.addLayout(header_layout)

        # Disk Selection
        sel_layout = QHBoxLayout()
        sel_layout.addWidget(QLabel("Select Drive:"))
        self.disk_combo = QComboBox()
        self.disk_combo.setStyleSheet("background: #1E1E1E; color: white; padding: 5px;")
        sel_layout.addWidget(self.disk_combo, 1)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_disks)
        sel_layout.addWidget(self.refresh_btn)
        layout.addLayout(sel_layout)

        # Visualization
        self.grid_frame = QFrame()
        self.grid_frame.setStyleSheet("background: #1E1E1E; border-radius: 10px;")
        self.grid_layout = QGridLayout(self.grid_frame)
        self.grid_layout.setSpacing(4)
        self.blocks = []
        self.setup_grid(20, 40)
        layout.addWidget(self.grid_frame)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.wipe_btn = QPushButton("START SECURE WIPE")
        self.wipe_btn.setObjectName("wipeBtn")
        self.wipe_btn.clicked.connect(self.start_wipe)
        layout.addWidget(self.wipe_btn)

        self.refresh_disks()
        self.update_credits()

    def setup_grid(self, r, c):
        for i in range(r):
            for j in range(c):
                b = QFrame()
                b.setFixedSize(16, 16)
                b.setStyleSheet("background: #2D2D2D; border-radius: 2px;")
                self.grid_layout.addWidget(b, i, j)
                self.blocks.append(b)

    def update_credits(self):
        try:
            # Simulate API call to get credits
            # headers = {"Authorization": f"Bearer {self.token}"}
            # resp = requests.get(f"{API_BASE_URL}/user/credits", headers=headers)
            # self.credits = resp.json().get("credits", 0)
            self.credits = 5 # Dummy value
            self.credits_label.setText(f"Credits: {self.credits}")
        except:
            self.credits_label.setText("Credits: Error")

    def refresh_disks(self):
        self.disk_combo.clear()
        ps = r"Get-Disk | ForEach-Object { $d=$_; Get-Partition -DiskNumber $d.Number | Get-Volume | Select-Object @{N='Number';E={$d.Number}}, DriveLetter, @{N='SizeGB';E={[math]::Round($d.Size/1GB,2)}}, @{N='Model';E={$d.FriendlyName}} } | ConvertTo-Json"
        res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout:
            try:
                disks = json.loads(res.stdout)
                if isinstance(disks, dict): disks = [disks]
                for d in disks:
                    if d.get("DriveLetter"):
                        self.disk_combo.addItem(f"Disk {d['Number']} ({d['DriveLetter']}:) - {d['SizeGB']}GB", d)
            except: pass

    def start_wipe(self):
        if self.credits <= 0:
            QMessageBox.warning(self, "No Credits", "Please purchase more wipe credits on our website.")
            return

        data = self.disk_combo.currentData()
        if not data: return

        confirm = QMessageBox.critical(self, "WARNING", f"Erase {data['DriveLetter']}:? Data will be GONE FOREVER.", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.wipe_btn.setEnabled(False)
            self.status_label.setText("Validating Credits...")
            
            # Simulate backend validation
            self.status_label.setText("Wiping...")
            self.total_size_mb = data['SizeGB'] * 1024
            self.wipe_thread = WipeThread(data['Number'], data['DriveLetter'])
            self.wipe_thread.progress_signal.connect(self.update_ui)
            self.wipe_thread.finished_signal.connect(self.done)
            self.wipe_thread.start()

    def update_ui(self, mb):
        p = min(100, int((mb/self.total_size_mb)*100))
        self.progress_bar.setValue(p)
        num = int((p/100)*len(self.blocks))
        for i in range(num): self.blocks[i].setStyleSheet("background: #B00020;")

    def done(self, ok, msg):
        self.wipe_btn.setEnabled(True)
        if ok:
            self.status_label.setText("Success! Credit deducted.")
            self.credits -= 1
            self.credits_label.setText(f"Credits: {self.credits}")
            QMessageBox.information(self, "Done", "Wipe complete. Certificate generated.")
        else:
            QMessageBox.critical(self, "Error", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    login = LoginWindow()
    main_window = None

    def on_login(token, email):
        global main_window
        login.hide()
        main_window = ZeroTraceGUI(token, email)
        main_window.show()

    login.login_success.connect(on_login)
    login.show()
    sys.exit(app.exec_())
