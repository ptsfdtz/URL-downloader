import requests

def get_api_data(topic_id, cookies):
    url = f"https://online.njtech.edu.cn/api/v1/url/list?page=1&pageSize=400&topicId={topic_id}&genre=video&sort=asc"
    response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return None
