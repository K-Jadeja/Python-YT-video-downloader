import streamlit as st
import os
from utils import download_audio, download_video

st.set_page_config(page_title="YouTube Downloader", page_icon="🎥")

st.title("YouTube Downloader")

# URL input
url = st.text_input("Enter YouTube URL", "")

# Download type selection
download_type = st.radio("Select download type", ("Audio", "Video"))

# Download button
if st.button("Download"):
    if url:
        try:
            with st.spinner("Downloading..."):
                if download_type == "Audio":
                    result = download_audio(url)
                else:
                    result = download_video(url)
                
                if result:
                    st.success(f"Download completed: {result}")
                    
                    # Create a download link
                    with open(result, "rb") as file:
                        btn = st.download_button(
                            label="Download file",
                            data=file,
                            file_name=os.path.basename(result),
                            mime="audio/mp3" if download_type == "Audio" else "video/mp4"
                        )
                else:
                    st.error("Download failed. Please check the URL and try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a YouTube URL.")

# Instructions
st.markdown("""
## Instructions:
1. Enter a valid YouTube URL in the text box.
2. Select whether you want to download audio or video.
3. Click the 'Download' button.
4. Once the download is complete, use the 'Download file' button to save the file to your computer.
""")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")