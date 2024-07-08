import json
from get_data import get_api_data
from parse_data import parse_api_data
from download_videos import download_videos

def load_cookies(file_path):
    cookies = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split('=', 1)
            cookies[name] = value
    return cookies

topic_id = input("请输入剧集Id: ")

cookies = load_cookies('cookie.txt')

data = get_api_data(topic_id, cookies)

if data:
    result_dict = parse_api_data(data)
    
    print("以下是剧集名称:")
    for name in result_dict:
        print(name)
    
    download_folder = input("输入剧集名称:")
    download_videos(result_dict, download_folder)
else:
    print("未能获取到数据，请检查网络或API访问权限。")
