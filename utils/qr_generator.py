import os
import tempfile

import qrcode
from PIL import Image
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

def generate_qr_code(data, box_size=10, border=4):
    qr = qrcode.QRCode(version=1, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def get_qr_pixmap(data, size=200):
    img = generate_qr_code(data)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        img.save(temp_file.name)
        pixmap = QPixmap(temp_file.name)
    os.unlink(temp_file.name)  # Immediately delete the temporary file
    return pixmap

def set_qr_code(label: QLabel, data: str, size=200):
    pixmap = get_qr_pixmap(data, size)
    label.setPixmap(pixmap)
    label.setFixedSize(size, size)