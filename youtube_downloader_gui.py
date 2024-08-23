import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from utils import download_audio, download_video

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, save_path, download_type):
        QThread.__init__(self)
        self.url = url
        self.save_path = save_path
        self.download_type = download_type

    def run(self):
        try:
            if self.download_type == "audio":
                result = download_audio(self.url, self.save_path)
            else:
                result = download_video(self.url, self.save_path)
            
            if result:
                self.finished.emit(result)
            else:
                self.error.emit("Download failed")
        except Exception as e:
            self.error.emit(str(e))

class YouTubeDownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL")
        layout.addWidget(self.url_input)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Save to...")
        layout.addWidget(self.path_input)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(browse_button)

        button_layout = QHBoxLayout()
        self.audio_button = QPushButton("Download Audio")
        self.audio_button.clicked.connect(lambda: self.download("audio"))
        button_layout.addWidget(self.audio_button)

        self.video_button = QPushButton("Download Video")
        self.video_button.clicked.connect(lambda: self.download("video"))
        button_layout.addWidget(self.video_button)

        layout.addLayout(button_layout)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(300, 300, 400, 200)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.path_input.setText(folder)

    def download(self, download_type):
        url = self.url_input.text()
        save_path = self.path_input.text()

        if not url or not save_path:
            self.status_label.setText("Please enter URL and save location.")
            return

        self.download_thread = DownloadThread(url, save_path, download_type)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.error.connect(self.download_error)
        self.download_thread.start()

        self.audio_button.setEnabled(False)
        self.video_button.setEnabled(False)
        self.status_label.setText("Downloading...")

    def download_finished(self, file_path):
        self.status_label.setText(f"Download completed: {file_path}")
        self.audio_button.setEnabled(True)
        self.video_button.setEnabled(True)

    def download_error(self, error_message):
        self.status_label.setText(f"Error: {error_message}")
        self.audio_button.setEnabled(True)
        self.video_button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloaderGUI()
    ex.show()
    sys.exit(app.exec_())