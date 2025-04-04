import os
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict

class File:
    """Represents a file in the system."""
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.size = os.path.getsize(path)  # Get file size in bytes
        self.last_accessed = os.path.getatime(path)  # Last accessed timestamp

class DigitalWasteManager:
    """Manages digital waste including duplicate and obsolete files."""
    def __init__(self):
        self.files = []  # List of File objects
        self.duplicates = defaultdict(list)  # Dictionary to store duplicates
        self.obsolete_files = []  # List to store obsolete files

    def scan_storage(self, folder_path):
        """Scans the given folder for files."""
        self.files.clear()
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                self.files.append(File(file_path))
        return len(self.files)

    def detect_duplicates(self):
        """Finds duplicate files based on name."""
        self.duplicates.clear()
        for file in self.files:
            self.duplicates[file.name].append(file.path)
        return {k: v for k, v in self.duplicates.items() if len(v) > 1}

    def detect_obsolete_files(self, days_threshold=365):
        """Finds files that haven't been accessed in the given number of days."""
        self.obsolete_files.clear()
        current_time = os.path.getatime(__file__)  # Use script's access time as reference
        for file in self.files:
            if (current_time - file.last_accessed) / (60 * 60 * 24) > days_threshold:
                self.obsolete_files.append(file.path)
        return self.obsolete_files

# GUI Implementation
class WasteManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Waste Management System")
        self.manager = DigitalWasteManager()

        # UI Elements
        self.label = tk.Label(root, text="Select a folder to scan:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.scan_button = tk.Button(root, text="Scan Folder", command=self.scan_folder, font=("Arial", 10))
        self.scan_button.pack(pady=5)

        self.duplicate_button = tk.Button(root, text="Find Duplicates", command=self.show_duplicates, font=("Arial", 10))
        self.duplicate_button.pack(pady=5)

        self.obsolete_button = tk.Button(root, text="Find Obsolete Files", command=self.show_obsolete, font=("Arial", 10))
        self.obsolete_button.pack(pady=5)

        self.result_text = tk.Text(root, height=10, width=50, font=("Arial", 10))
        self.result_text.pack(pady=10)

    def scan_folder(self):
        """Opens a dialog to select a folder and scans for files."""
        folder = filedialog.askdirectory()
        if folder:
            file_count = self.manager.scan_storage(folder)
            messagebox.showinfo("Scan Complete", f"Scanned {file_count} files.")

    def show_duplicates(self):
        """Displays duplicate files found."""
        duplicates = self.manager.detect_duplicates()
        self.result_text.delete("1.0", tk.END)
        if duplicates:
            self.result_text.insert(tk.END, "Duplicate Files Found:\n")
            for name, paths in duplicates.items():
                self.result_text.insert(tk.END, f"{name}:\n  " + "\n  ".join(paths) + "\n\n")
        else:
            self.result_text.insert(tk.END, "No duplicate files found.")

    def show_obsolete(self):
        """Displays obsolete files found."""
        obsolete_files = self.manager.detect_obsolete_files()
        self.result_text.delete("1.0", tk.END)
        if obsolete_files:
            self.result_text.insert(tk.END, "Obsolete Files Found:\n" + "\n".join(obsolete_files))
        else:
            self.result_text.insert(tk.END, "No obsolete files found.")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = WasteManagementGUI(root)
    root.mainloop()
