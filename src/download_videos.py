import os
import requests
from tqdm import tqdm

def download_videos(result_dict, download_folder):
    os.makedirs(download_folder, exist_ok=True)

    for name, url in result_dict.items():
        file_path = os.path.join(download_folder, name + '.mkv')
        print(f"Downloading {name} from {url}...")
        response = requests.get(url, stream=True)
        with open(file_path, 'wb') as file, tqdm(
                desc=name,
                total=int(response.headers.get('content-length', 0)),
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                bar.update(len(data))
        print(f"{name} 下载成功")

    print("全部下载完成")
