import os
from yt_dlp import YoutubeDL

def download_audio(youtube_url, output_path="."):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            print(f"Audio downloaded successfully: {ydl.prepare_filename(info_dict)}")
            return ydl.prepare_filename(info_dict)
    
    except Exception as e:
        print(f"An error occurred while downloading audio: {str(e)}")
        return None

def download_video(youtube_url, output_path=".", max_resolution="1080p"):
    try:
        ydl_opts = {
            'format': f'bestvideo[height<={max_resolution}]+bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            print(f"Video downloaded successfully: {ydl.prepare_filename(info_dict)}")
            return ydl.prepare_filename(info_dict)
    
    except Exception as e:
        print(f"An error occurred while downloading video: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage:
    youtube_url = "https://www.youtube.com/watch?v=KhFlD54nQrY"  # Replace with your YouTube URL
    output_path = "./downloads"  # Set your desired output directory

    # Download audio
    print("Downloading audio...")
    download_audio(youtube_url, output_path)

    # Download video
    print("Downloading video...")
    download_video(youtube_url, output_path, max_resolution="1080p")
