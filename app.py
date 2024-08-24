import streamlit as st
from utils import download_audio, download_video

def main():
    st.title("YouTube Video & Audio Downloader")
    st.write("Enter the URL of the YouTube video you want to download.")

    # Input for YouTube URL
    youtube_url = st.text_input("YouTube URL", "")
    
    # Select output format: Audio or Video
    download_type = st.radio("Select Download Type", ('Audio (MP3)', 'Video (MP4)'))
    
    # Input for Output Path
    output_path = st.text_input("Output Path", "./downloads")
    
    # Resolution selector for video
    if download_type == 'Video (MP4)':
        resolution = st.selectbox("Select Maximum Resolution", ["1080p", "720p", "480p", "360p"])
    
    # Download button
    if st.button("Download"):
        if not youtube_url:
            st.error("Please enter a valid YouTube URL.")
        else:
            st.write("Downloading...")
            if download_type == 'Audio (MP3)':
                file_path = download_audio(youtube_url, output_path)
            else:
                file_path = download_video(youtube_url, output_path, max_resolution=resolution)
            
            if file_path:
                st.success(f"Download complete! File saved to: {file_path}")
            else:
                st.error("An error occurred during the download.")

if __name__ == "__main__":
    main()
