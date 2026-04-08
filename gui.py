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
                             QProgressBar, QGridLayout, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QColor, QPalette, QFont
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec

SERVER_URL = "http://127.0.0.1:8081"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
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
            a_exe_path = get_resource_path("a.exe")
            # We use a subprocess and capture stdout to parse progress
            # Note: The 'a.exe' expects user input 'CONFIRM'. We'll need to pipe it.
            process = subprocess.Popen(
                [a_exe_path, str(self.disk_num), self.disk_letter],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # Send 'CONFIRM' to the stdin
            process.stdin.write("CONFIRM\n")
            process.stdin.flush()

            while True:
                line = process.stdout.readline()
                if not line:
                    break
                
                self.log_signal.emit(line.strip())
                
                # Check for progress output: "... 256 MB written"
                if "MB written" in line:
                    try:
                        # Find the number before 'MB written'
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == "MB" and i > 0:
                                mb_written = int(parts[i-1])
                                self.progress_signal.emit(mb_written)
                                break
                    except Exception as e:
                        print(f"Error parsing progress: {e}")

            process.wait()
            if process.returncode == 0:
                self.finished_signal.emit(True, "Wipe completed successfully!")
            else:
                self.finished_signal.emit(False, f"Wipe failed with exit code {process.returncode}")

        except Exception as e:
            self.finished_signal.emit(False, str(e))

class ZeroTraceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZeroTrace - Secure Data Sanitization")
        self.setFixedSize(900, 700)
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QLabel { color: #E0E0E0; font-family: 'Segoe UI'; }
            QPushButton { 
                background-color: #1E1E1E; color: white; border: 1px solid #333; 
                padding: 10px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #333; }
            QPushButton#wipeBtn { background-color: #B00020; border: none; }
            QPushButton#wipeBtn:hover { background-color: #CF6679; }
            QComboBox { background-color: #1E1E1E; color: white; border: 1px solid #333; padding: 5px; }
            QProgressBar { border: 1px solid #333; border-radius: 5px; text-align: center; color: white; }
            QProgressBar::chunk { background-color: #03DAC6; }
            QFrame#gridFrame { background-color: #1E1E1E; border-radius: 10px; border: 1px solid #333; }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        header = QLabel("ZeroTrace")
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header)

        tagline = QLabel("Secure. Irreversible. Data gone, forever.")
        tagline.setFont(QFont("Segoe UI", 10))
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("color: #888;")
        self.layout.addWidget(tagline)

        # Disk Selection
        selection_layout = QHBoxLayout()
        selection_layout.addWidget(QLabel("Select Drive:"))
        self.disk_combo = QComboBox()
        self.refresh_disks()
        selection_layout.addWidget(self.disk_combo, 1)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_disks)
        selection_layout.addWidget(self.refresh_btn)
        
        self.layout.addLayout(selection_layout)

        # Visualization Grid
        self.grid_frame = QFrame()
        self.grid_frame.setObjectName("gridFrame")
        self.grid_layout = QGridLayout(self.grid_frame)
        self.grid_layout.setSpacing(4)
        self.grid_frame.setMinimumHeight(350)
        
        self.blocks = []
        self.setup_animation_grid(20, 40) # 800 blocks
        
        self.layout.addWidget(self.grid_frame)

        # Progress and Status
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Actions
        self.wipe_btn = QPushButton("START SECURE WIPE")
        self.wipe_btn.setObjectName("wipeBtn")
        self.wipe_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.wipe_btn.clicked.connect(self.start_wipe_process)
        self.layout.addWidget(self.wipe_btn)

        if not is_admin():
            self.status_label.setText("⚠️ RUNNING WITHOUT ADMINISTRATOR PRIVILEGES - WIPING MAY FAIL")
            self.status_label.setStyleSheet("color: #FFB74D; font-weight: bold;")

    def setup_animation_grid(self, rows, cols):
        # Clear existing grid
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        self.blocks = []

        for r in range(rows):
            for c in range(cols):
                block = QFrame()
                block.setFixedSize(16, 16)
                block.setStyleSheet("background-color: #2D2D2D; border-radius: 2px;")
                self.grid_layout.addWidget(block, r, c)
                self.blocks.append(block)

    def refresh_disks(self):
        self.disk_combo.clear()
        ps_script = r"""
        Get-Disk | ForEach-Object {
            $disk = $_
            Get-Partition -DiskNumber $disk.Number -ErrorAction SilentlyContinue | ForEach-Object {
                $partition = $_
                Get-Volume -Partition $partition -ErrorAction SilentlyContinue | ForEach-Object {
                    [PSCustomObject]@{
                        Number = $disk.Number
                        Letter = $_.DriveLetter
                        SizeGB = [math]::Round($disk.Size/1GB,2)
                        Model = $disk.FriendlyName
                    }
                }
            }
        } | ConvertTo-Json
        """
        result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            try:
                disks = json.loads(result.stdout)
                if isinstance(disks, dict): disks = [disks]
                for d in disks:
                    if d.get("Letter"):
                        self.disk_combo.addItem(f"Disk {d['Number']} ({d['Letter']}:) - {d['SizeGB']} GB - {d['Model']}", d)
            except:
                pass
        if self.disk_combo.count() == 0:
            self.disk_combo.addItem("No suitable disks found")

    def start_wipe_process(self):
        data = self.disk_combo.currentData()
        if not data:
            QMessageBox.warning(self, "Error", "Please select a valid disk.")
            return

        confirm = QMessageBox.critical(self, "FINAL WARNING", 
                                       f"This will PERMANENTLY ERASE all data on {data['Letter']}: (Disk {data['Number']}).\n\n"
                                       "This action CANNOT be undone. Proceed?", 
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            self.wipe_btn.setEnabled(False)
            self.disk_combo.setEnabled(False)
            self.refresh_btn.setEnabled(False)
            self.status_label.setText("Wiping in progress...")
            self.progress_bar.setValue(0)
            
            # Reset grid
            for b in self.blocks:
                b.setStyleSheet("background-color: #2D2D2D; border-radius: 2px;")

            self.total_size_mb = data['SizeGB'] * 1024
            self.wipe_thread = WipeThread(data['Number'], data['Letter'])
            self.wipe_thread.progress_signal.connect(self.update_progress)
            self.wipe_thread.finished_signal.connect(self.wipe_finished)
            self.wipe_thread.start()

    def update_progress(self, mb_written):
        percentage = int((mb_written / self.total_size_mb) * 100)
        percentage = min(100, percentage)
        self.progress_bar.setValue(percentage)
        
        # Update blocks
        num_blocks_to_red = int((percentage / 100) * len(self.blocks))
        for i in range(min(num_blocks_to_red, len(self.blocks))):
            self.blocks[i].setStyleSheet("background-color: #B00020; border-radius: 2px;")

    def wipe_finished(self, success, message):
        self.wipe_btn.setEnabled(True)
        self.disk_combo.setEnabled(True)
        self.refresh_btn.setEnabled(True)
        
        if success:
            self.status_label.setText("Wipe Successful! Generating Certificate...")
            # Here we would call the registration/submission logic
            # For simplicity, I'll show a success message
            QMessageBox.information(self, "Success", message)
            
            # Trigger blockchain registration (async)
            data = self.disk_combo.currentData()
            a_args = f"{data['Number']}{data['Letter']}"
            device_id = f"zT{a_args}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{''.join(random.choices(string.ascii_letters + string.digits, k=6))}_usr"
            self.register_with_server(device_id)
        else:
            self.status_label.setText("Wipe Failed")
            QMessageBox.critical(self, "Error", message)

    def register_with_server(self, device_id):
        # This is a simplified version of the registration logic
        try:
            priv_key = ec.generate_private_key(ec.SECP256R1())
            pub_pem = priv_key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
            
            # Register
            requests.post(f"{SERVER_URL}/register_device", json={"device_id": device_id, "public_key": pub_pem.decode()}, timeout=5)
            
            # Submit
            cert_data = {"device_id": device_id, "timestamp": datetime.utcnow().isoformat()}
            cert_bytes = json.dumps(cert_data).encode()
            signature = priv_key.sign(hashlib.sha256(cert_bytes).hexdigest().encode(), ec.ECDSA(hashes.SHA256()))
            
            requests.post(f"{SERVER_URL}/submit_certificate_json", json={
                "device_id": device_id,
                "cert_bytes_b64": base64.b64encode(cert_bytes).decode(),
                "signature_b64": base64.b64encode(signature).decode()
            }, timeout=5)
            
            self.status_label.setText("Certificate Generated & Stored on Blockchain")
        except Exception as e:
            self.status_label.setText(f"Server error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # if not is_admin():
    #     ...
    
    window = ZeroTraceGUI()
    window.show()
    sys.exit(app.exec_())
