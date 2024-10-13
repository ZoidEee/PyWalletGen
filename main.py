import sys
from typing import Dict, Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMenuBar,
    QLabel,
    QComboBox,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
)
from bitcoinlib.wallets import Wallet, wallet_exists, wallet_delete


class BTCWalletGeneration:
    def __init__(self, wallet_name: str):
        self.wallet_name = wallet_name

        if wallet_exists(self.wallet_name):
            self._delete_existing_wallet()
        else:
            print(f"Wallet '{self.wallet_name}' does not exist.")

    def _delete_existing_wallet(self):
        try:
            if wallet_delete(self.wallet_name, force=True):
                print(f"Wallet '{self.wallet_name}' has been deleted successfully.")
            else:
                print(f"Error deleting wallet '{self.wallet_name}'.")
        except Exception as e:
            print(f"Exception occurred while deleting wallet: {e}")

    def _create_wallet(self, network: str, witness_type: str) -> Dict[str, Any]:
        try:
            wallet = Wallet.create(
                self.wallet_name, network=network, witness_type=witness_type
            )
            wallet_key = wallet.get_key()
            print(
                f"name: {wallet.name}\n"
                f"type: {witness_type}\n"
                f"address: {wallet_key.address}\n"
                f"private_key: {wallet_key.wif}\n"
                f"public_key: {wallet_key.key().public_hex}"
            )
            return {
                "name": wallet.name,
                "type": witness_type,
                "address": wallet_key.address,
                "private_key": wallet_key.wif,
                "public_key": wallet_key.key().public_hex,
            }
        except Exception as e:
            print(f"Exception occurred while creating wallet: {e}")
            return {}

    def legacy_wallet(self) -> Dict[str, Any]:
        return self._create_wallet("bitcoin", "legacy")

    def native_segwit(self) -> Dict[str, Any]:
        return self._create_wallet("bitcoin", "segwit")

    def p2sh_segwit(self) -> Dict[str, Any]:
        return self._create_wallet("bitcoin", "p2sh-segwit")

    def testnet_wallet(self) -> Dict[str, Any]:
        return self._create_wallet("testnet", "legacy")

    def hd_wallet(self, derivation_path: str = "m/44'/0'/0'/0") -> Dict[str, Any]:
        try:
            wallet = Wallet.create(
                self.wallet_name, network="bitcoin", key_path=derivation_path
            )
            wallet_key = wallet.get_key()
            return {
                "name": wallet.name,
                "derivation_path": wallet.key_path,
                "address": wallet_key.address,
                "private_key": wallet_key.wif,
                "public_key": wallet_key.key().public_hex,
            }
        except Exception as e:
            print(f"Exception occurred while creating HD wallet: {e}")
            return {}


class Demo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()
        self.setup_main_window()

    def initialize_ui(self):
        self.setWindowTitle("Crpyto Wallet Generator")
        self.setFixedSize(600, 400)

    def setup_main_window(self):
        self.create_actions()
        self.setup_menu_bar()

        wallet_types = [
            "Legacy",
            "Native SegWit (bech32)",
            "P2SH-SegWit (Nested SegWit)",
            "HD Wallet",
            "Testnet",
        ]

        # Create main layout
        main_layout = QVBoxLayout()

        # Header
        self.header_lbl = QLabel("Bitcoin Wallet Generator")
        self.header_lbl.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(self.header_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        # Wallet type and generate button
        wallet_generate_hbox = QHBoxLayout()
        self.wallet_type_menu = QComboBox()
        self.wallet_type_menu.addItems(wallet_types)
        self.wallet_type_menu.setFixedWidth(100)
        wallet_generate_hbox.addWidget(self.wallet_type_menu)

        self.generate_wallet_btn = QPushButton("Generate Wallet")
        self.generate_wallet_btn.setFixedSize(150, 25)
        wallet_generate_hbox.addWidget(self.generate_wallet_btn)
        main_layout.addLayout(wallet_generate_hbox)

        # Wallet details
        details_layout = QFormLayout()
        details_layout.setVerticalSpacing(10)

        self.wallet_name_label = QLabel("Wallet Name:")
        self.wallet_name_label.setFixedSize(150, 25)
        self.wallet_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wallet_name_input = QLineEdit()
        self.wallet_name_input.setPlaceholderText("Enter wallet name...")

        self.wallet_address = QLabel("Address:")
        self.wallet_address.setFixedSize(150, 25)
        self.wallet_address.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wallet_address_lbl = QLabel("...")

        self.public_key = QLabel("Public Key:")
        self.public_key.setFixedSize(150, 25)
        self.public_key.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pub_key_lbl = QLabel("...")

        self.priv_key = QLabel("Private Key:")
        self.priv_key.setFixedSize(150, 25)
        self.priv_key.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.priv_key_lbl = QLabel("...")

        details_layout.addRow(self.wallet_name_label, self.wallet_name_input)
        details_layout.addRow(self.wallet_address, self.wallet_address_lbl)
        details_layout.addRow(self.public_key, self.pub_key_lbl)
        details_layout.addRow(self.priv_key, self.priv_key_lbl)

        main_layout.addLayout(details_layout)

        # Set the main layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def setup_menu_bar(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        # Create File menu and add actions
        file_menu = menubar.addMenu("File")
        file_menu.addSeparator()  # Add a separator line
        file_menu.addAction(self.minimize_action)
        file_menu.addAction(self.exit_action)

        # Create Edit menu and add actions
        edit_menu = menubar.addMenu("Edit")

    def create_actions(self):
        # File actions
        self.exit_action = QAction(QIcon(), "Exit", self)
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.close)

        self.minimize_action = QAction(QIcon(), "Minimize", self)
        self.minimize_action.setStatusTip("Minimize the application")
        self.minimize_action.triggered.connect(self.showMinimized)


def main():
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
