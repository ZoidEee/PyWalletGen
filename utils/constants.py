WALLET_TYPES = [
    "Legacy",
    "Native SegWit (bech32)",
    "P2SH-SegWit (Nested SegWit)",
    "HD Wallet",
    "Testnet",
]

APP_STYLE = """
    QWidget {
        background-color: #1b1b1b;
        color: #f2a900;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
    }
    QMainWindow {
        min-width: 950px;
        min-height: 500px;
    }
    QLabel {
        color: #f2a900;
        padding: 5px;
    }
    QPushButton {
        background-color: #f2a900;
        color: black;
        border: none;
        padding: 8px 15px;
        border-radius: 5px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #d89e00;
    }
    QPushButton:pressed {
        background-color: #c78c00;
    }
    QLineEdit {
        color: #f2a900;
        border: 2px solid #444444;
        padding: 6px;
        border-radius: 5px;
        background-color: #2c2c2c;
        min-width: 200px;
    }
    QComboBox {
        color: #f2a900;
        border: 2px solid #444444;
        padding: 6px;
        border-radius: 5px;
        background-color: #2c2c2c;
        min-width: 200px;
    }
    QLineEdit:focus, QComboBox:focus {
        border: 2px solid #f2a900;
    }
    QComboBox::drop-down {
        border: none;
        background-color: #f2a900;
        width: 30px;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
    }
    QComboBox::down-arrow {
        image: url(images/down-chevron.png);
        width: 20px;
        height: 20px;
    }
    QComboBox QAbstractItemView {
        background-color: #2c2c2c;
        border: 1px solid #f2a900;
    }
    QComboBox QAbstractItemView::item {
        color: #f2a900;
        padding: 5px;
    }
    QComboBox QAbstractItemView::item:selected {
        background-color: #f2a900;
        color: #2c2c2c;
    }
    QComboBox QAbstractItemView::item:hover {
        background-color: #f2a900;
        color: #2c2c2c;
    }
    QMenuBar {
        background-color: #222222;
        color: #f2a900;
        padding: 5px;
    }
    QMenuBar::item {
        padding: 5px 10px;
        border-radius: 3px;
    }
    QMenuBar::item:selected {
        background-color: #f2a900; 
        color: #1b1b1b;
    }
    QMenu {
        background-color: #222222; 
        color: #f2a900; 
        border: none; 
    }
    QMenu::item {
        padding: 5px 20px; 
    }
    QMenu::item:selected {
        background-color: #f2a900; 
        color: #1b1b1b;
    }
    #header_label {
        font-size: 24px; 
        font-weight: bold; 
        margin: 10px 0; 
        color: #f2a900; 
    }
    #generate_wallet_btn {
        min-width: 150px; 
        min-height: 30px; 
    }
    #wallet_address, #public_key_address, #private_key_address {
        font-size: 12px; 
        background-color: #333333; 
        border-radius: 3px; 
        padding: 5px; 
    }
    #pub_qr_code, #priv_qr_code {
        background-color: white; 
        border-radius: 5px; 
        min-width: 200px; 
        min-height: 200px; 
    }
    #qr_label {
        font-weight: bold; 
        margin-top: 20px; 
        color: #f2a900; 
    }
"""
