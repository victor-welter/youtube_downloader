import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from youtube_downloader.downloader import download_video

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyTube Downloader")
        self.geometry("700x400")
        self.minsize(500, 350)

        # --- Instance variables ---
        self.download_path = os.path.expanduser("~") # Default to user's home directory
        self.download_in_progress = False

        # --- Frames for Organization ---
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")
        self.path_frame = ttk.Frame(self)
        self.path_frame.pack(pady=10, padx=20, fill="x")
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(pady=10, padx=20, fill="x")
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # --- Create Widgets ---
        self._create_input_widgets()
        self._create_path_widgets()
        self._create_progress_widgets()
        self._create_status_widgets()

    def _create_input_widgets(self):
        url_label = ttk.Label(self.input_frame, text="YouTube URL:")
        url_label.pack(side="left", padx=(0, 10))
        self.url_variable = tk.StringVar()
        url_entry = ttk.Entry(self.input_frame, textvariable=self.url_variable, width=60)
        url_entry.pack(side="left", expand=True, fill="x")
        self.download_button = ttk.Button(self.input_frame, text="Download", command=self._on_download_click)
        self.download_button.pack(side="left", padx=(10, 0))

    def _create_path_widgets(self):
        path_label = ttk.Label(self.path_frame, text="Save to:")
        path_label.pack(side="left", padx=(0, 21)) # Adjusted padding for alignment
        self.path_variable = tk.StringVar(value=self.download_path)
        path_entry = ttk.Entry(self.path_frame, textvariable=self.path_variable, state="readonly")
        path_entry.pack(side="left", expand=True, fill="x")
        browse_button = ttk.Button(self.path_frame, text="Browse...", command=self._on_browse_click)
        browse_button.pack(side="left", padx=(10, 0))

    def _create_progress_widgets(self):
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(expand=True, fill="x")

    def _create_status_widgets(self):
        self.status_label = ttk.Label(self.status_frame, text="Ready. Please enter a YouTube URL.", anchor="center")
        self.status_label.pack(expand=True, fill="both")

    def _on_browse_click(self):
        if self.download_in_progress: return
        chosen_path = filedialog.askdirectory(initialdir=self.download_path, title="Select Download Folder")
        if chosen_path:
            self.download_path = chosen_path
            self.path_variable.set(self.download_path)

    def _on_download_click(self):
        if self.download_in_progress:
            messagebox.showwarning("In Progress", "A download is already in progress.")
            return

        url = self.url_variable.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL first.")
            return

        self.download_in_progress = True
        self.download_button.config(state="disabled")
        self.status_label.config(text="Starting download...")
        self.progress_bar['value'] = 0

        download_thread = threading.Thread(
            target=download_video,
            args=(url, self.download_path, self._update_progress, self._on_download_complete)
        )
        download_thread.start()

    def _update_progress(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                percentage = (d['downloaded_bytes'] / total_bytes) * 100
                self.progress_bar['value'] = percentage
                self.status_label.config(text=f"Downloading... {int(percentage)}%")
                self.update_idletasks()
        elif d['status'] == 'finished':
            self.status_label.config(text="Download finished, processing...")
            self.update_idletasks()

    def _on_download_complete(self, success: bool, message: str):
        self.status_label.config(text=message)
        self.download_button.config(state="normal")
        self.progress_bar['value'] = 100 if success else 0
        self.download_in_progress = False
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)