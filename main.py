import json
from src.get_data import get_api_data
from src.parse_data import parse_api_data
from src.download_videos import download_videos

def load_cookies(file_path):
    cookies = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split('=', 1)
            cookies[name] = value
    return cookies

def main():
    topic_id = input("请输入剧集Id: ")

    cookies = load_cookies('cookie.txt')
    data = get_api_data(topic_id, cookies)

    print("API返回的数据:")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    result_dict = parse_api_data(data)
    if result_dict:
        print("以下是剧集名称:")
        for name in result_dict:
            print(name)

        download_folder = input("请输入要下载的剧集名称: ")
        download_videos(result_dict, download_folder)
    else:
        print("解析数据失败。")

if __name__ == "__main__":
    main()