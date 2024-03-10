import os
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from requests.exceptions import RequestException


class VideoDownloaderUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Video Downloader')
        self.setGeometry(300, 300, 400, 200)
        self.setWindowIcon(QIcon('icon.png'))

        self.url_label = QLabel('视频下载链接:')
        self.url_input = QLineEdit()
        self.browse_button = QPushButton('选择存储路径')
        self.download_button = QPushButton('开始下载')
        self.progress_bar = QProgressBar()

        self.browse_button.clicked.connect(self.browse_directory)
        self.download_button.clicked.connect(self.start_download)

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, '选择存储路径')
        if directory:
            self.save_path = directory

    def start_download(self):
        download_url = self.url_input.text()
        if not download_url:
            print("请输入下载链接.")
            return

        if not hasattr(self, 'save_path') or not self.save_path:
            print("请选择存储路径.")
            return

        # 创建下载线程
        download_thread = DownloadThread(download_url, self.save_path)
        # 将线程的进度信号连接到更新UI的槽函数
        download_thread.progress_signal.connect(self.update_progress)
        # 启动下载线程
        download_thread.start()

    def update_progress(self, value):
        # 更新进度条的值
        self.progress_bar.setValue(value)


class DownloadThread(QThread):
    # 定义一个带有整数参数的自定义信号
    progress_signal = pyqtSignal(int)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            response = requests.head(self.url)
            if response.status_code != 200:
                print(f"Failed to fetch the video information. Status code: {response.status_code}")
                return

            content_disposition = response.headers.get('Content-Disposition')
            filename = content_disposition.split('filename=')[-1].strip('"') if content_disposition else 'video.mp4'

            self.download_file(self.url, self.save_path, filename)
        except Exception as e:
            print(f"An error occurred: {e}")

    def download_file(self, url, path, filename, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
            except RequestException as e:
                print(f"Failed to download file on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    print(f"Max retries reached. Failed to download file: {url}")
                    return
            else:
                break

        full_path = os.path.join(path, filename)
        if not os.path.exists(path):
            os.makedirs(path)

        print(f"Downloading {full_path}")

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        downloaded_size = 0

        with open(full_path, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded_size += len(data)
                progress_percentage = (downloaded_size / total_size) * 100
                # 发送进度信号
                self.progress_signal.emit(int(progress_percentage))

        print(f"File downloaded successfully: {full_path}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader_ui = VideoDownloaderUI()
    downloader_ui.show()
    sys.exit(app.exec_())
