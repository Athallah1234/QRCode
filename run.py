import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import datetime
import re

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")

        # Variables for customization options
        self.qr_type_var = tk.StringVar()
        self.data_var = tk.StringVar()
        self.version_var = tk.IntVar()
        self.error_correction_var = tk.StringVar()
        self.box_size_var = tk.IntVar()
        self.bg_color_var = tk.StringVar()
        self.fg_color_var = tk.StringVar()
        self.file_format_var = tk.StringVar()

        # Set default values
        self.qr_type_var.set("Text")
        self.error_correction_var.set("H")
        self.box_size_var.set(10)
        self.bg_color_var.set("white")
        self.fg_color_var.set("black")
        self.file_format_var.set(".png")

        self.qr_code_history = []

        self.create_widgets()

    def create_widgets(self):
        # QR code type selection
        self.label_qr_type = ttk.Label(self.root, text="Select QR Code Type:")
        self.label_qr_type.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        qr_type_options = ("Text", "URL", "Email", "Phone")
        self.qr_type_combo = ttk.Combobox(self.root, values=qr_type_options, textvariable=self.qr_type_var)
        self.qr_type_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # File format selection
        self.label_file_format = ttk.Label(self.root, text="Select File Format:")
        self.label_file_format.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        file_format_options = (".png", ".jpg", ".bmp", ".gif")
        self.file_format_combo = ttk.Combobox(self.root, values=file_format_options, textvariable=self.file_format_var)
        self.file_format_combo.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        # Entry for user input
        self.label_data = ttk.Label(self.root, text="Enter data:")
        self.label_data.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_data = ttk.Entry(self.root, width=40, textvariable=self.data_var)
        self.entry_data.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # QR code version
        self.label_version = ttk.Label(self.root, text="Select QR Code Version:")
        self.label_version.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        self.version_spinbox = ttk.Spinbox(self.root, from_=1, to=40, textvariable=self.version_var)
        self.version_spinbox.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.version_var.set(1)

        # Error correction level
        self.label_error_correction = ttk.Label(self.root, text="Error Correction Level:")
        self.label_error_correction.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.error_correction_combo = ttk.Combobox(self.root, values=("L", "M", "Q", "H"), textvariable=self.error_correction_var)
        self.error_correction_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Box size
        self.label_box_size = ttk.Label(self.root, text="Box Size:")
        self.label_box_size.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        self.box_size_entry = ttk.Entry(self.root, textvariable=self.box_size_var)
        self.box_size_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Background color
        self.label_bg_color = ttk.Label(self.root, text="Background Color:")
        self.label_bg_color.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.bg_color_entry = ttk.Entry(self.root, textvariable=self.bg_color_var)
        self.bg_color_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Foreground color
        self.label_fg_color = ttk.Label(self.root, text="Foreground Color:")
        self.label_fg_color.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.fg_color_entry = ttk.Entry(self.root, textvariable=self.fg_color_var)
        self.fg_color_entry.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Generate button
        self.generate_button = ttk.Button(self.root, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        # Save button
        self.save_button = ttk.Button(self.root, text="Save QR Code", command=self.save_qr_code)
        self.save_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Clear button
        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_qr_code)
        self.clear_button.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        # History button
        self.history_button = ttk.Button(self.root, text="View History", command=self.view_history)
        self.history_button.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Display generated QR code
        self.qr_code_image = ttk.Label(self.root, text="")
        self.qr_code_image.grid(row=7, column=1, columnspan=4, padx=10, pady=10, sticky="w")  # Adjust columnspan

    def view_history(self):
        # Display a new window or dialog with the QR Code history
        history_window = tk.Toplevel(self.root)
        history_window.title("QR Code History")

        # Create a text widget to display history
        history_text = tk.Text(history_window, wrap=tk.WORD, width=50, height=20)
        history_text.grid(row=0, column=0, padx=10, pady=10)

        # Insert history information into the text widget
        for entry in self.qr_code_history:
            history_text.insert(tk.END, f"Type: {entry['type']}\nData: {entry['data']}\nDate: {entry['date']}\n\n")

    def generate_qr_code(self):
        # Validation: Check if QR code type is selected
        qr_type = self.qr_type_var.get()
        if not qr_type:
            messagebox.showerror("Error", "Please select a QR code type.")
            return

        # Validation: Check if data is provided
        data = self.entry_data.get().strip()
        if not data:
            messagebox.showerror("Error", "Please enter data for the QR code.")
            return
        
        # Validation: Check if the box size is a positive integer
        try:
            box_size = int(self.box_size_var.get())
            if box_size <= 0:
                messagebox.showerror("Error", "Box Size must be a positive integer.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid Box Size. Please enter a valid integer.")
            return

        # Validation: Check if the version is an integer between 1 and 8
        try:
            version = int(self.version_var.get())
            if not (1 <= version <= 8):
                messagebox.showerror("Error", "Version must be an integer between 1 and 8.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid Version. Please enter a valid integer.")
            return

        # Get user input and customization options
        qr_type = self.qr_type_var.get()
        data = self.entry_data.get()
        version = int(self.version_var.get())
        error_correction = self.error_correction_var.get()
        box_size = int(self.box_size_var.get())
        bg_color = self.bg_color_var.get()
        fg_color = self.fg_color_var.get()

        # Generate QR code with customization options
        qr = qrcode.QRCode(
            version=version,
            error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction}"),
            box_size=box_size,
            border=4,
        )

        if qr_type == "Text":
            qr.add_data(data)
        elif qr_type == "URL":
            qr.add_data("http://" + data)
        elif qr_type == "Email":
            qr.add_data(f"mailto:{data}")
        elif qr_type == "Phone":
            qr.add_data(f"tel:{data}")

        qr.make(fit=True)

        qr_code = qr.make_image(fill_color=fg_color, back_color=bg_color)

        # Store information in history
        history_entry = {
            "data": data,
            "type": qr_type,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # Add more information as needed
        }
        self.qr_code_history.append(history_entry)

        # Display QR code in the Tkinter window
        self.qr_code_image.tk_img = ImageTk.PhotoImage(qr_code)
        self.qr_code_image.config(image=self.qr_code_image.tk_img)

    def validate_data_format(self, data, qr_type):
        if qr_type == "URL" and not data.startswith(("http://", "https://")):
            return False
        elif qr_type == "Email" and not re.match(r"[^@]+@[^@]+\.[^@]+", data):
            return False
        elif qr_type == "Phone" and not re.match(r"\d{10,15}$", data):
            return False
        return True

    def save_qr_code(self):
        # Check if QR code has been generated
        if not self.qr_code_history:
            messagebox.showerror("Error", "Please generate a QR code first.")
            return

        # Get user input and customization options
        qr_type = self.qr_type_var.get()
        data = self.entry_data.get()
        version = int(self.version_var.get())
        error_correction = self.error_correction_var.get()
        box_size = int(self.box_size_var.get())
        bg_color = self.bg_color_var.get()
        fg_color = self.fg_color_var.get()

        # Generate QR code with customization options
        qr = qrcode.QRCode(
            version=version,
            error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction}"),
            box_size=box_size,
            border=4,
        )

        if qr_type == "Text":
            qr.add_data(data)
        elif qr_type == "URL":
            qr.add_data("http://" + data)
        elif qr_type == "Email":
            qr.add_data(f"mailto:{data}")
        elif qr_type == "Phone":
            qr.add_data(f"tel:{data}")

        qr.make(fit=True)

        qr_code = qr.make_image(fill_color=fg_color, back_color=bg_color)

        # Save the QR code as an image file
        filename = filedialog.asksaveasfilename(defaultextension=self.file_format_var.get(), filetypes=[("Image files", "*.png;*.jpg;*.bmp;*.gif"), ("All files", "*.*")])
        if filename:
            qr_code.save(filename)

            # Display a success message
            messagebox.showinfo("QR Code Generator", "QR Code saved successfully!")

            # Clear the generated QR code and reset the input fields
            self.qr_code_image.config(image="")
            self.entry_data.delete(0, tk.END)
            # Remove the cleared QR code from history
            self.qr_code_history.clear()

    def clear_qr_code(self):
        # Check if QR code history is empty
        if not self.qr_code_history:
            messagebox.showinfo("Info", "No QR Code to clear.")
            return

        # Clear the generated QR code and reset the input fields
        self.qr_code_image.config(image="")
        self.entry_data.delete(0, tk.END)

        # Clear the QR code history
        self.qr_code_history.clear()

        # Display a message indicating successful clearing
        messagebox.showinfo("Info", "QR Code cleared successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()

