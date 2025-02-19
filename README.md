# 📱 Professional QR Code Generator

A feature-rich GUI application for generating customized QR codes using Python. Built with `tkinter` for the interface, `qrcode` for QR generation, and `Pillow` for image processing.

## 🚀 Features

- **Multiple Content Types:** Generate QR codes for:
  - Text/URL
  - WiFi credentials
  - vCard contacts
  - Email addresses
  - Phone numbers
  - Geographic locations

- **Advanced Customization:**
  - Multiple style patterns (Square, Circle, Rounded, etc.)
  - Custom colors and gradients
  - Logo embedding
  - Error correction levels
  - Size and border adjustments

- **Batch Operations:**
  - Batch QR code generation
  - Export generation history
  - Print QR codes directly

## 🛠️ Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/qr-generator.git
    cd qr-generator
    ```

2. Install required packages:
    ```bash
    pip install qrcode[pil] pillow
    ```

3. Run the application:
    ```bash
    python qr_generator.py
    ```

## 📝 Usage

1. **Basic Settings:**
   - Choose content type
   - Enter required information
   - Adjust QR code parameters
   - Click "Generate" to create QR code

2. **Advanced Settings:**
   - Customize QR pattern style
   - Add custom colors
   - Embed logo
   - Apply effects

3. **Additional Features:**
   - Save QR codes in multiple formats
   - Copy to clipboard
   - Print directly
   - Track generation history

## 🧩 Dependencies

- [Python](https://www.python.org/) (>= 3.6)
- [qrcode](https://github.com/lincolnloop/python-qrcode)
- [Pillow](https://python-pillow.org/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

## 👥 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for new features or improvements.

## 🌟 Key Features

- User-friendly interface with tabbed organization
- Real-time QR code preview
- Multiple styling options
- Batch processing capabilities
- History tracking and export
- Direct printing support
