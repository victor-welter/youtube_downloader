# YouTube Downloader

A simple desktop application to download YouTube videos in high quality.

---

### ✨ Features

* Downloads videos in the best available quality using `yt-dlp`.
* Automatically merges video and audio streams with **FFmpeg**.
* Simple and intuitive graphical user interface (GUI).
* Real-time progress bar and status updates.
* Allows the user to choose the destination folder.

---

### 🚀 How to Run

**Prerequisites:**
* **Python 3.8+**
* **FFmpeg** (must be installed and available in the system's PATH)

**Steps:**

1.  **Clone the project:**
    ```bash
    git clone [https://github.com/your-username/youtube-downloader.git](https://github.com/your-username/youtube-downloader.git)
    cd youtube-downloader
    ```

2.  **Set up the environment:**
    ```bash
    # Create and activate the virtual environment
    python -m venv .venv
    
    # On Windows
    .\.venv\Scripts\Activate
    
    # On macOS / Linux
    source .venv/bin/activate
    
    # Install dependencies and the project
    pip install -r requirements.txt
    pip install -e .
    ```

3.  **Run the application:**
    ```bash
    python run.py
    ```

---