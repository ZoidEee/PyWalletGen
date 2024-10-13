import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QComboBox, QPushButton, QLineEdit,
    QFormLayout, QHBoxLayout, QVBoxLayout, QMessageBox, QFileDialog, QInputDialog
)
from PyWallGen.utils.constants import WALLET_TYPES, APP_STYLE
from PyWallGen.wallet.generator import BTCWalletGeneration
from PyWallGen.utils.qr_generator import set_qr_code
from PyWallGen.utils.security import export_encrypted_wallet, import_encrypted_wallet


class Demo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Wallet Generator")
        self.setStyleSheet(APP_STYLE)
        self.setup_ui()

    def setup_ui(self):
        self.create_actions()
        self.setup_menu_bar()

        main_layout = QVBoxLayout()

        self.header_label = QLabel("Bitcoin Wallet Generator", objectName="header_label")
        main_layout.addWidget(self.header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        input_layout = QHBoxLayout()
        self.wallet_type_menu = QComboBox()
        self.wallet_type_menu.addItems(WALLET_TYPES)
        self.wallet_name_input = QLineEdit()
        self.wallet_name_input.setPlaceholderText("Enter wallet name...")
        self.generate_wallet_btn = QPushButton("Generate Wallet", objectName="generate_wallet_btn")
        self.generate_wallet_btn.clicked.connect(self.create_wallet)
        input_layout.addWidget(self.wallet_type_menu)
        input_layout.addWidget(self.wallet_name_input)
        input_layout.addWidget(self.generate_wallet_btn)
        main_layout.addLayout(input_layout)

        details_layout = QFormLayout()
        self.wallet_address = QLabel("", objectName="wallet_address")
        self.public_key_address = QLabel("", objectName="public_key_address")
        self.private_key_address = QLabel("", objectName="private_key_address")
        details_layout.addRow("<b>Address:</b>", self.wallet_address)
        details_layout.addRow("<b>Public Key:</b>", self.public_key_address)
        details_layout.addRow("<b>Private Key:</b>", self.private_key_address)
        main_layout.addLayout(details_layout)

        qr_layout = QHBoxLayout()
        pub_qr_container = QVBoxLayout()
        pub_qr_label = QLabel("Public Address QR Code", objectName="qr_label")
        self.pub_qr_code = QLabel(objectName="pub_qr_code")
        self.pub_qr_code.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pub_qr_container.addWidget(pub_qr_label, alignment=Qt.AlignmentFlag.AlignCenter)
        pub_qr_container.addWidget(self.pub_qr_code)

        priv_qr_container = QVBoxLayout()
        priv_qr_label = QLabel("Private Key QR Code", objectName="qr_label")
        self.priv_qr_code = QLabel(objectName="priv_qr_code")
        self.priv_qr_code.setAlignment(Qt.AlignmentFlag.AlignCenter)
        priv_qr_container.addWidget(priv_qr_label, alignment=Qt.AlignmentFlag.AlignCenter)
        priv_qr_container.addWidget(self.priv_qr_code)

        qr_layout.addLayout(pub_qr_container)
        qr_layout.addLayout(priv_qr_container)
        main_layout.addLayout(qr_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.exit_action)

        # Add new menu items for export and import
        export_action = QAction("Export Wallet", self)
        export_action.triggered.connect(self.export_wallet)
        file_menu.addAction(export_action)

        import_action = QAction("Import Wallet", self)
        import_action.triggered.connect(self.import_wallet)
        file_menu.addAction(import_action)

    def create_actions(self):
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)

    def create_wallet(self):
        wallet_name = self.wallet_name_input.text()
        wallet_type = self.wallet_type_menu.currentText()
        wallet_creation = BTCWalletGeneration(wallet_name)

        wallet = {}
        if wallet_type == "Legacy":
            wallet = wallet_creation.legacy_wallet()
        elif wallet_type == "Native SegWit (bech32)":
            wallet = wallet_creation.native_segwit()
        elif wallet_type == "P2SH-SegWit (Nested SegWit)":
            wallet = wallet_creation.p2sh_segwit()
        elif wallet_type == "HD Wallet":
            wallet = wallet_creation.hd_wallet()
        elif wallet_type == "Testnet":
            wallet = wallet_creation.testnet_wallet()

        if wallet:
            self.current_wallet = wallet
            self.wallet_address.setText(wallet.get("address", "N/A"))
            self.public_key_address.setText(wallet.get("public_key", "N/A"))
            self.private_key_address.setText(wallet.get("private_key", "N/A"))

            set_qr_code(self.pub_qr_code, wallet.get("address", ""))

            # Auto-export wallet to desktop
            self.auto_export_wallet()

            reply = QMessageBox.question(self, 'Generate Private Key QR',
                                         "Do you want to generate a QR code for the private key? This can be a security risk.",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                set_qr_code(self.priv_qr_code, wallet.get("private_key", ""))
            else:
                self.priv_qr_code.clear()
        else:
            self.wallet_address.setText("Wallet creation failed")
            self.public_key_address.setText("N/A")
            self.private_key_address.setText("N/A")
            self.pub_qr_code.clear()
            self.priv_qr_code.clear()

    def auto_export_wallet(self):
        if not hasattr(self, 'current_wallet'):
            return

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = os.path.join(desktop_path, f"{self.current_wallet['name']}.ewf")

        password, ok = QInputDialog.getText(self, "Encryption Password", "Enter password for wallet encryption:",
                                            QLineEdit.EchoMode.Password)
        if ok and password:
            try:
                export_encrypted_wallet(self.current_wallet, filename, password)
                QMessageBox.information(self, "Export Successful", f"Wallet exported successfully to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export wallet: {str(e)}")

    def export_wallet(self):
        if not hasattr(self, 'current_wallet'):
            QMessageBox.warning(self, "Export Error", "No wallet to export. Please generate a wallet first.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Export Wallet", "", "Encrypted Wallet Files (*.ewf)")
        if filename:
            password, ok = QInputDialog.getText(self, "Encryption Password", "Enter password for encryption:",
                                                QLineEdit.EchoMode.Password)
            if ok and password:
                try:
                    export_encrypted_wallet(self.current_wallet, filename, password)
                    QMessageBox.information(self, "Export Successful", "Wallet exported successfully.")
                except Exception as e:
                    QMessageBox.critical(self, "Export Error", f"Failed to export wallet: {str(e)}")

    def import_wallet(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Import Wallet", "", "Encrypted Wallet Files (*.ewf)")
        if filename:
            password, ok = QInputDialog.getText(self, "Decryption Password", "Enter password for decryption:",
                                                QLineEdit.EchoMode.Password)
            if ok and password:
                try:
                    wallet = import_encrypted_wallet(filename, password)
                    self.current_wallet = wallet
                    self.wallet_address.setText(wallet.get("address", "N/A"))
                    self.public_key_address.setText(wallet.get("public_key", "N/A"))
                    self.private_key_address.setText(wallet.get("private_key", "N/A"))
                    set_qr_code(self.pub_qr_code, wallet.get("address", ""))
                    QMessageBox.information(self, "Import Successful", "Wallet imported successfully.")
                except Exception as e:
                    QMessageBox.critical(self, "Import Error", f"Failed to import wallet: {str(e)}")