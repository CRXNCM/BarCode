
# 📸 Barcode Reader GUI

A user-friendly GUI application to read barcodes from images using Python. This project utilizes `tkinter` for the graphical interface, `Pillow` for image processing, and `pyzbar` for barcode decoding.

## 🚀 Features

- **Open Image:** Select an image file containing barcodes.
- **Barcode Detection:** Automatically detects and decodes barcodes from the selected image.
- **Results Display:** Displays the type and data of each detected barcode.
- **Save Results:** Save the barcode information to a text file for future reference.

## 📷 Screenshots

![Screenshot 1](Images/screenshot1.png)
![Screenshot 2](Images/screenshot2.png)

## 🛠️ Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/CRXNCM/BarCode.git
    cd BarCode
    ```

2. Install the required packages:
    ```bash
    pip install pillow pyzbar
    ```

3. Run the application:
    ```bash
    python Barcode.py
    ```

## 📝 Usage

1. **Open Image:** Click on the "Open Image" button to select an image file containing barcodes.
2. **View Results:** The detected barcodes will be displayed in the text area.
3. **Save Results:** Click on the "Save Results" button to save the barcode information to a text file.

## 🧩 Dependencies

- [Python](https://www.python.org/) (>= 3.6)
- [Pillow](https://python-pillow.org/) (for image processing)
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) (for barcode decoding)
- [tkinter](https://docs.python.org/3/library/tkinter.html) (for GUI)

## 👥 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.


## 🌟 Acknowledgements

- [Pillow](https://python-pillow.org/)
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
