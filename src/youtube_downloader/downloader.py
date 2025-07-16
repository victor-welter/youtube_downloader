import yt_dlp
import os

def download_video(url: str, output_path: str, progress_hook=None, completion_callback=None):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',    
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

        # The main download process
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if completion_callback:
            completion_callback(True, "Download completed successfully!")

    except Exception as e:
        if completion_callback:
            # yt-dlp often wraps errors, so we get the original message
            error_message = getattr(e, 'message', str(e))
            completion_callback(False, f"An error occurred: {error_message}")