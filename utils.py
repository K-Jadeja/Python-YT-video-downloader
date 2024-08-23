import os
from pytube import YouTube

def download_audio(youtube_url, output_path="."):
    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)
        
        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # Download the audio
        out_file = audio_stream.download(output_path=output_path)
        
        # Rename the file to have an .mp3 extension
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        
        print(f"Audio downloaded successfully: {new_file}")
        return new_file
    except Exception as e:
        print(f"An error occurred while downloading audio: {str(e)}")
        return None

def download_video(youtube_url, output_path=".", max_resolution="1080p"):
    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)
        
        # Get the highest resolution video stream without audio, up to 1080p
        video_stream = yt.streams.filter(
            adaptive=True, 
            file_extension='mp4', 
            only_video=True, 
            resolution=max_resolution
        ).first()
        
        # If no 1080p stream is available, get the next highest resolution
        if not video_stream:
            video_stream = yt.streams.filter(
                adaptive=True, 
                file_extension='mp4', 
                only_video=True
            ).order_by('resolution').desc().first()
        
        # Download the video
        out_file = video_stream.download(output_path=output_path)
        
        print(f"Video downloaded successfully: {out_file}")
        return out_file
    except Exception as e:
        print(f"An error occurred while downloading video: {str(e)}")
        return None