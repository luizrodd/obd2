from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QApplication)
from PyQt6.QtCore import Qt
import sys
from obd_connection import conectar_obd
from obd_monitor import OBDMonitor

class ConnectUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Conectar ao OBD-II")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Selecione a porta OBD-II:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.label)
        
        self.port_selector = QComboBox()
        self.port_selector.addItems(["COM3", "COM4", "COM5", "COM6"])  # Exemplo de portas
        self.port_selector.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.port_selector)
        
        self.connect_btn = QPushButton("Conectar")
        self.connect_btn.setStyleSheet("background-color: #008CBA; color: white; font-size: 16px; padding: 10px;")
        self.connect_btn.clicked.connect(self.connect_to_obd)
        layout.addWidget(self.connect_btn)
        
        self.status_label = QLabel("Aguardando conexão...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def connect_to_obd(self):
        porta = self.port_selector.currentText()
        self.status_label.setText(f"Conectando à {porta}...")
        
        connection = conectar_obd(porta)
        if connection and connection.is_connected():
            self.status_label.setText("✅ Conectado com sucesso!")
            self.monitor_ui = OBDMonitor(connection)
            self.monitor_ui.show()
            self.close()
        else:
            self.status_label.setText("❌ Falha ao conectar! Tente outra porta.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConnectUI()
    window.show()
    sys.exit(app.exec())
