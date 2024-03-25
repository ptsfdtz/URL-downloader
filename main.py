import os
import sys
import requests
import time
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
        self.speed_label = QLabel('下载速度: 0 B/s')  # 新增的标签用于显示下载速度

        self.browse_button.clicked.connect(self.browse_directory)
        self.download_button.clicked.connect(self.start_download)

        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.speed_label)

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

        # 如果已经存在下载线程，则不再创建新的线程
        if hasattr(self, 'download_thread') and self.download_thread.isRunning():
            print("下载已经在进行中...")
            return

        # 如果不存在下载线程，创建并启动下载线程
        self.download_thread = DownloadThread(download_url, self.save_path)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.start()

    def update_progress(self, value, speed):
        self.progress_bar.setValue(value)
        self.speed_label.setText(f'下载速度: {speed} B/s')


class DownloadThread(QThread):
    progress_signal = pyqtSignal(int, int)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.start_time = time.time()
        self.last_downloaded_size = 0

    def run(self):
        try:
            response = requests.head(self.url)
            if response.status_code != 200:
                print(f"Failed to fetch the video information. Status code: {response.status_code}")
                return

            content_disposition = response.headers.get('Content-Disposition')
            filename = content_disposition.split('filename=')[-1].strip('"') if content_disposition else 'video.mp4'

            replacement_digit = 1
            while True:
                modified_url = self.replace_last_digit(self.url, replacement_digit)
                success = self.download_file(modified_url, self.save_path, filename)
                if not success:
                    break
                replacement_digit += 1
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
                    return False
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

                current_time = time.time()
                elapsed_time = current_time - self.start_time
                if elapsed_time > 0:
                    speed = (downloaded_size - self.last_downloaded_size) / elapsed_time
                    self.progress_signal.emit(int((downloaded_size / total_size) * 100), int(speed))

                self.last_downloaded_size = downloaded_size

        print(f"File downloaded successfully: {full_path}")
        return True

    @staticmethod
    def replace_last_digit(url, replacement):
        last_digit_index = url.rfind('/')
        if last_digit_index != -1:
            modified_url = url[:last_digit_index+1] + str(replacement) + url[last_digit_index + 2:]
            return modified_url
        else:
            return url

def main():
    app = QApplication(sys.argv)
    downloader_ui = VideoDownloaderUI()
    downloader_ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
