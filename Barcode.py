import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import *
from qrcode.image.styles.colormasks import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import datetime
import csv
import os

class QRCodeGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Professional QR Code Generator")
        self.window.geometry("1200x800")
        self.window.configure(bg="#f0f0f0")
        
        # Initialize history
        self.history = []
        
        # Create main container
        self.create_notebook()
        self.setup_styles()
        self.initialize_tabs()
        
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tabs
        self.basic_tab = ttk.Frame(self.notebook, padding="20")
        self.advanced_tab = ttk.Frame(self.notebook, padding="20")
        self.history_tab = ttk.Frame(self.notebook, padding="20")
        
        self.notebook.add(self.basic_tab, text="Basic Settings")
        self.notebook.add(self.advanced_tab, text="Advanced Settings")
        self.notebook.add(self.history_tab, text="History")
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Action.TButton", padding=10, font=("Helvetica", 10))
        style.configure("Section.TLabelframe", padding=10)
        
    def initialize_tabs(self):
        self.setup_basic_tab()
        self.setup_advanced_tab()
        self.setup_history_tab()
        
    def setup_basic_tab(self):
        # Content Type Section
        self.setup_content_section()
        
        # QR Settings Section
        self.setup_qr_settings()
        
        # Quick Actions Section
        self.setup_quick_actions()
        
        # Preview Section
        self.setup_preview_section(self.basic_tab)
        
    def setup_content_section(self):
        content_frame = ttk.LabelFrame(self.basic_tab, text="Content", style="Section.TLabelframe")
        content_frame.pack(fill=tk.X, pady=10)
        
        # Content Type Selector
        ttk.Label(content_frame, text="Content Type:").pack(anchor="w")
        self.content_type = ttk.Combobox(content_frame, 
            values=["Text/URL", "WiFi", "vCard", "Email", "Phone", "Location"])
        self.content_type.set("Text/URL")
        self.content_type.pack(fill=tk.X, pady=5)
        self.content_type.bind('<<ComboboxSelected>>', self.update_content_fields)
        
        # Dynamic Content Fields
        self.content_fields = ttk.Frame(content_frame)
        self.content_fields.pack(fill=tk.X, pady=5)
        
        # Default Text Field
        self.data_entry = tk.Text(self.content_fields, height=3)
        self.data_entry.pack(fill=tk.X)
        
    def setup_qr_settings(self):
        settings_frame = ttk.LabelFrame(self.basic_tab, text="QR Settings", style="Section.TLabelframe")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Create grid for settings
        grid = ttk.Frame(settings_frame)
        grid.pack(fill=tk.X)
        
        # Version Settings
        ttk.Label(grid, text="Version:").grid(row=0, column=0, sticky="w", padx=5)
        self.version = ttk.Spinbox(grid, from_=1, to=40, width=10)
        self.version.set(1)
        self.version.grid(row=0, column=1, padx=5, pady=5)
        
        # Error Correction
        ttk.Label(grid, text="Error Correction:").grid(row=0, column=2, sticky="w", padx=5)
        self.error_correction = ttk.Combobox(grid, values=["L (7%)", "M (15%)", "Q (25%)", "H (30%)"])
        self.error_correction.set("M (15%)")
        self.error_correction.grid(row=0, column=3, padx=5, pady=5)
        
        # Size Settings
        ttk.Label(grid, text="Box Size:").grid(row=1, column=0, sticky="w", padx=5)
        self.box_size = ttk.Spinbox(grid, from_=1, to=50, width=10)
        self.box_size.set(10)
        self.box_size.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(grid, text="Border:").grid(row=1, column=2, sticky="w", padx=5)
        self.border = ttk.Spinbox(grid, from_=0, to=10, width=10)
        self.border.set(4)
        self.border.grid(row=1, column=3, padx=5, pady=5)
        
    def setup_quick_actions(self):
        actions_frame = ttk.LabelFrame(self.basic_tab, text="Quick Actions", style="Section.TLabelframe")
        actions_frame.pack(fill=tk.X, pady=10)
        
        # First Row
        row1 = ttk.Frame(actions_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Button(row1, text="Generate", command=self.generate_qr, 
                  style="Action.TButton").pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(row1, text="Save", command=self.save_qr,
                  style="Action.TButton").pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(row1, text="Copy", command=self.copy_to_clipboard,
                  style="Action.TButton").pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Second Row
        row2 = ttk.Frame(actions_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Button(row2, text="Print", command=self.print_qr,
                  style="Action.TButton").pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(row2, text="Batch Generate", command=self.batch_generate,
                  style="Action.TButton").pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(row2, text="Export History", command=self.export_history,
                  style="Action.TButton").pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    def print_qr(self):
        img = self.generate_qr()
        if img:
            temp_path = "temp_print.png"
            img.save(temp_path)
            os.startfile(temp_path, "print")
            # Clean up after printing
            import time
            time.sleep(2)
            os.remove(temp_path)

    def batch_generate(self):
        input_file = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if input_file:
            output_dir = filedialog.askdirectory(title="Select Output Directory")
            if output_dir:
                with open(input_file, 'r') as file:
                    for i, line in enumerate(file.readlines(), 1):
                        # Store current content
                        current_content = self.data_entry.get("1.0", tk.END)
                        
                        # Generate QR for new content
                        self.data_entry.delete("1.0", tk.END)
                        self.data_entry.insert("1.0", line.strip())
                        img = self.generate_qr()
                        if img:
                            img.save(f"{output_dir}/{line.strip()}.png")
                        
                        # Restore original content
                        self.data_entry.delete("1.0", tk.END)
                        self.data_entry.insert("1.0", current_content)
                
                messagebox.showinfo("Success", f"Batch generation complete!\nFiles saved in: {output_dir}")
    def get_content(self):
        """Returns formatted content based on content type"""
        content_type = self.content_type.get()
        if content_type == "WiFi":
            return f"WIFI:T:{self.wifi_security.get()};S:{self.wifi_ssid.get()};P:{self.wifi_password.get()};;"
        elif content_type == "vCard":
            vcard = ["BEGIN:VCARD", "VERSION:3.0"]
            for field, entry in self.vcard_entries.items():
                key = field.replace(":", "").upper()
                vcard.append(f"{key}:{entry.get()}")
            vcard.append("END:VCARD")
            return "\n".join(vcard)
        elif content_type == "Email":
            return f"mailto:{self.email.get()}?subject={self.email_subject.get()}"
        elif content_type == "Location":
            return f"geo:{self.latitude.get()},{self.longitude.get()}"
        else:
            return self.data_entry.get("1.0", "end-1c")

    def get_style_drawer(self):
        """Returns the selected style drawer"""
        style_map = {
            "Square": SquareModuleDrawer(),
            "Gapped Square": GappedSquareModuleDrawer(),
            "Circle": CircleModuleDrawer(),
            "Rounded": RoundedModuleDrawer()
        }
        return style_map.get(self.style.get(), SquareModuleDrawer())

    def get_color_mask(self):
        """Returns color mask with selected colors"""
        return SolidFillColorMask(
            front_color=(0, 0, 0),  # Default black
            back_color=(255, 255, 255)  # Default white
        )

    def add_to_history(self):
        """Add current generation to history"""
        timestamp = datetime.datetime.now()
        self.history.append([
            timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            self.content_type.get(),
            self.get_content(),
            f"Version: {self.version.get()}, Error: {self.error_correction.get()}"
        ])
        self.update_history_view()

    def update_history_view(self):
        """Update history tab view"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        for entry in self.history:
            self.history_tree.insert("", "end", values=entry)

    def update_preview(self, img):
        """Update preview with generated QR"""
        preview = ImageTk.PhotoImage(img.resize((200, 200)))
        self.preview_label.configure(image=preview)
        self.preview_label.image = preview

    def export_history(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=f"qr_history_{timestamp}.csv",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Type", "Content", "Settings"])
                writer.writerows(self.history)
            messagebox.showinfo("Success", f"History exported to: {file_path}")

    def setup_preview_section(self, parent):
        preview_frame = ttk.LabelFrame(parent, text="Preview", style="Section.TLabelframe")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(pady=10)
        
    def setup_advanced_tab(self):
        # Style Settings
        self.setup_style_settings()
        
        # Color Settings
        self.setup_color_settings()
        
        # Logo Settings
        self.setup_logo_settings()
        
    def setup_history_tab(self):
        # Create history view
        self.history_tree = ttk.Treeview(self.history_tab, columns=("Date", "Type", "Content"))
        self.history_tree.heading("Date", text="Date")
        self.history_tree.heading("Type", text="Type")
        self.history_tree.heading("Content", text="Content")
        self.history_tree.pack(fill=tk.BOTH, expand=True)
    def setup_style_settings(self):
        style_frame = ttk.LabelFrame(self.advanced_tab, text="Style Settings", padding="10")
        style_frame.pack(fill=tk.X, pady=10)
        
        # QR Pattern Style
        pattern_frame = ttk.Frame(style_frame)
        pattern_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pattern_frame, text="Pattern Style:").grid(row=0, column=0, sticky="w")
        self.style = ttk.Combobox(pattern_frame, 
            values=["Square", "Gapped Square", "Circle", "Rounded", "Vertical Bars", "Horizontal Bars"])
        self.style.set("Square")
        self.style.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Pattern Size
        ttk.Label(pattern_frame, text="Pattern Size:").grid(row=1, column=0, sticky="w", pady=5)
        self.pattern_size = ttk.Scale(pattern_frame, from_=1, to=10, orient="horizontal")
        self.pattern_size.set(5)
        self.pattern_size.grid(row=1, column=1, padx=5, sticky="ew")
        
        # Eye Style
        ttk.Label(pattern_frame, text="Corner Eye Style:").grid(row=2, column=0, sticky="w", pady=5)
        self.eye_style = ttk.Combobox(pattern_frame, 
            values=["Square", "Circle", "Rounded", "Cushion"])
        self.eye_style.set("Square")
        self.eye_style.grid(row=2, column=1, padx=5, sticky="ew")
        
        # Pattern Effects
        effects_frame = ttk.LabelFrame(style_frame, text="Effects", padding="5")
        effects_frame.pack(fill=tk.X, pady=5)
        
        self.gradient_enabled = tk.BooleanVar(value=False)
        ttk.Checkbutton(effects_frame, text="Enable Gradient", 
            variable=self.gradient_enabled).pack(anchor="w")
        
        self.shadow_enabled = tk.BooleanVar(value=False)
        ttk.Checkbutton(effects_frame, text="Add Shadow Effect", 
            variable=self.shadow_enabled).pack(anchor="w")
        
        # Bind events for live preview
        self.style.bind('<<ComboboxSelected>>', lambda e: self.update_preview(self.generate_qr()))
        self.eye_style.bind('<<ComboboxSelected>>', lambda e: self.update_preview(self.generate_qr()))
        self.pattern_size.bind('<ButtonRelease-1>', lambda e: self.update_preview(self.generate_qr()))
    def setup_style_settings(self):
        style_frame = ttk.LabelFrame(self.advanced_tab, text="Style Settings", padding="10")
        style_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(style_frame, text="QR Pattern:").pack(anchor="w")
        self.style = ttk.Combobox(style_frame, 
            values=["Square", "Gapped Square", "Circle", "Rounded"])
        self.style.set("Square")
        self.style.pack(fill=tk.X, pady=5)

    def setup_color_settings(self):
        color_frame = ttk.LabelFrame(self.advanced_tab, text="Color Settings", padding="10")
        color_frame.pack(fill=tk.X, pady=10)
        
        # Foreground Color
        fg_frame = ttk.Frame(color_frame)
        fg_frame.pack(fill=tk.X, pady=5)
        ttk.Label(fg_frame, text="Foreground:").pack(side=tk.LEFT)
        self.fg_color = tk.StringVar(value="#000000")
        ttk.Button(fg_frame, text="Choose Color", 
            command=lambda: self.choose_color('fg')).pack(side=tk.LEFT, padx=5)
        
        # Background Color
        bg_frame = ttk.Frame(color_frame)
        bg_frame.pack(fill=tk.X, pady=5)
        ttk.Label(bg_frame, text="Background:").pack(side=tk.LEFT)
        self.bg_color = tk.StringVar(value="#FFFFFF")
        ttk.Button(bg_frame, text="Choose Color", 
            command=lambda: self.choose_color('bg')).pack(side=tk.LEFT, padx=5)

    def setup_logo_settings(self):
        logo_frame = ttk.LabelFrame(self.advanced_tab, text="Logo Settings", padding="10")
        logo_frame.pack(fill=tk.X, pady=10)
        
        self.logo_path = tk.StringVar()
        self.logo_size = tk.IntVar(value=30)
        
        # Logo selection
        logo_select = ttk.Frame(logo_frame)
        logo_select.pack(fill=tk.X, pady=5)
        ttk.Entry(logo_select, textvariable=self.logo_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(logo_select, text="Browse Logo", 
            command=self.browse_logo).pack(side=tk.LEFT, padx=5)
        
        # Logo size slider
        ttk.Label(logo_frame, text="Logo Size (%):").pack(anchor="w")
        ttk.Scale(logo_frame, from_=10, to=50, 
            variable=self.logo_size, orient="horizontal").pack(fill=tk.X)

    def choose_color(self, target):
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            if target == 'fg':
                self.fg_color.set(color)
            else:
                self.bg_color.set(color)
        self.update_preview(self.generate_qr())

    def browse_logo(self):
        file_types = [
            ('Image files', '*.png *.jpg *.jpeg *.bmp'),
            ('All files', '*.*')
        ]
        filename = filedialog.askopenfilename(filetypes=file_types)
        if filename:
            self.logo_path.set(filename)
            self.update_preview(self.generate_qr())

    def add_logo_to_qr(self, qr_image):
        if not self.logo_path.get():
            return qr_image
        
        try:
            logo = Image.open(self.logo_path.get())
            # Calculate logo size
            qr_width = qr_image.size[0]
            logo_size = int(qr_width * self.logo_size.get() / 100)
            logo = logo.resize((logo_size, logo_size))
            
            # Calculate position
            pos = ((qr_width - logo_size) // 2,) * 2
            
            # Create final image
            final_img = qr_image.copy()
            final_img.paste(logo, pos)
            return final_img
        except Exception as e:
            messagebox.showerror("Logo Error", f"Failed to add logo: {str(e)}")
            return qr_image

    def update_content_fields(self, event=None):
        # Clear existing fields
        for widget in self.content_fields.winfo_children():
            widget.destroy()
            
        content_type = self.content_type.get()
        
        if content_type == "WiFi":
            ttk.Label(self.content_fields, text="Network Name:").pack(anchor="w")
            self.wifi_ssid = ttk.Entry(self.content_fields)
            self.wifi_ssid.pack(fill=tk.X, pady=2)
            
            ttk.Label(self.content_fields, text="Password:").pack(anchor="w")
            self.wifi_password = ttk.Entry(self.content_fields, show="*")
            self.wifi_password.pack(fill=tk.X, pady=2)
            
            ttk.Label(self.content_fields, text="Security:").pack(anchor="w")
            self.wifi_security = ttk.Combobox(self.content_fields, values=["WPA/WPA2", "WEP", "None"])
            self.wifi_security.set("WPA/WPA2")
            self.wifi_security.pack(fill=tk.X, pady=2)
            
        elif content_type == "vCard":
            fields = ["Name:", "Phone:", "Email:", "Company:", "Title:", "Website:"]
            self.vcard_entries = {}
            for field in fields:
                ttk.Label(self.content_fields, text=field).pack(anchor="w")
                self.vcard_entries[field] = ttk.Entry(self.content_fields)
                self.vcard_entries[field].pack(fill=tk.X, pady=2)
                
        elif content_type == "Email":
            ttk.Label(self.content_fields, text="Email:").pack(anchor="w")
            self.email = ttk.Entry(self.content_fields)
            self.email.pack(fill=tk.X, pady=2)
            
            ttk.Label(self.content_fields, text="Subject:").pack(anchor="w")
            self.email_subject = ttk.Entry(self.content_fields)
            self.email_subject.pack(fill=tk.X, pady=2)
            
        elif content_type == "Location":
            ttk.Label(self.content_fields, text="Latitude:").pack(anchor="w")
            self.latitude = ttk.Entry(self.content_fields)
            self.latitude.pack(fill=tk.X, pady=2)
            
            ttk.Label(self.content_fields, text="Longitude:").pack(anchor="w")
            self.longitude = ttk.Entry(self.content_fields)
            self.longitude.pack(fill=tk.X, pady=2)
            
        else:  # Text/URL or Phone
            self.data_entry = tk.Text(self.content_fields, height=3)
            self.data_entry.pack(fill=tk.X)
    def save_qr(self):
        img = self.generate_qr()
        if img:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=f"qr_code_{timestamp}",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            if file_path:
                img.save(file_path)
                self.add_to_history()

    def generate_qr(self):
        try:
            qr = qrcode.QRCode(
                version=int(self.version.get()),
                error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{self.error_correction.get()[0]}"),
                box_size=int(self.box_size.get()),
                border=int(self.border.get())
            )
            
            qr.add_data(self.get_content())
            qr.make(fit=True)
            
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=self.get_style_drawer(),
                color_mask=self.get_color_mask()
            )
            
            self.update_preview(img)
            self.add_to_history()
            return img
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
            return None
    def copy_to_clipboard(self):
        img = self.generate_qr()
        if img:
            # Convert QR code to PhotoImage
            photo = ImageTk.PhotoImage(img)
            # Copy to clipboard
            self.window.clipboard_clear()
            self.window.clipboard_append(photo)
            # Show success message
            messagebox.showinfo("Success", "QR Code copied to clipboard!")
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = QRCodeGenerator()
    app.run()
