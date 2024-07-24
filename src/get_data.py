import requests
import json

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config('config.json')

def get_api_data(topic_id, cookies):
    url = (
        f"{config['base_url']}?page={config['page']}&pageSize={config['page_size']}&topicId={topic_id}&genre={config['genre']}&sort={config['sort']}"
    )
    response = requests.get(url, cookies=cookies)
    response.raise_for_status()  
    return response.json()
