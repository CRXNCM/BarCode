import tkinter as tk
from tkinter import filedialog, messagebox
from pyzbar.pyzbar import decode
from PIL import Image

def read_barcode(image_path):
    try:
        img = Image.open(image_path)
        decoded_objects = decode(img)

        if not decoded_objects:
            return "No barcodes found."

        results = []
        for obj in decoded_objects:
            barcode_type = obj.type
            barcode_data = obj.data.decode('utf-8')
            results.append(f"Type: {barcode_type}\nData: {barcode_data}\n")
        
        return "\n".join(results)
    except Exception as e:
        return f"An error occurred: {e}"

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if file_path:
        result = read_barcode(file_path)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)

def save_results():
    result = result_text.get(1.0, tk.END).strip()
    if not result:
        messagebox.showwarning("No Results", "There are no results to save.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write(result)
        messagebox.showinfo("Saved", f"Results saved to {save_path}")

# Create the main window
root = tk.Tk()
root.title("Barcode Reader")

# Create and place widgets
open_button = tk.Button(root, text="Open Image", command=open_file)
open_button.pack(pady=10)

result_text = tk.Text(root, wrap='word', width=50, height=15)
result_text.pack(padx=10, pady=10)

save_button = tk.Button(root, text="Save Results", command=save_results)
save_button.pack(pady=10)

# Run the application
root.mainloop()
