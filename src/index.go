package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

func encodeURLPartially(url string) string {
	url = strings.ReplaceAll(url, " ", "%20") // 编码空格
	url = strings.ReplaceAll(url, "(", "%28") // 编码左括号
	url = strings.ReplaceAll(url, ")", "%29") // 编码右括号
	return url
}

func getData(url, token string) (map[string]interface{}, error) {
	client := &http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Cookie", "online_token="+token)

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("error: received status code %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, err
	}

	return result, nil
}

func fetchData(videoId string) {
	token := "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiTkpURUNIIl0sImV4cCI6MTcyOTM0Mjg0MCwiaWF0IjoxNzI4NzM4MDQwLCJpc3MiOiJNQVJTIiwicmxlIjoidXNlciIsInN1YiI6IjIwMjIyMTAxOTA4MSIsInVpZCI6IjY2ZDA3MmY3OTk3ZWJjYzY1NGEwMmMwNyJ9.Omtptc0i9OxJbj0Lw7x5a8H4ZIrqOJ4kfp503QwcFAo"
	url := fmt.Sprintf("https://online.njtech.edu.cn/api/v2/videos/%s?id=%s", videoId, videoId)

	data, err := getData(url, token)
	if err != nil {
		fmt.Println("Error fetching video data:", err)
		return
	}

	seasons := data["seasons"].([]interface{})
	if len(seasons) == 0 {
		fmt.Println("No seasons found")
		return
	}
	apiUrl := fmt.Sprintf("https://online.njtech.edu.cn/api/v2/video_seasons/%s?order=asc&orderBy=index", seasons[0].(map[string]interface{})["id"].(string))

	seasonData, err := getData(apiUrl, token)
	if err != nil {
		fmt.Println("Error fetching season data:", err)
		return
	}

	episodes := seasonData["episodes"].([]interface{})
	var urls []string
	for _, episode := range episodes {
		urls = append(urls, encodeURLPartially(episode.(map[string]interface{})["url"].(string)))
	}

	fmt.Println(urls)
}

func main() {
	var videoId string
	fmt.Print("请输入视频 ID: ")
	fmt.Scanln(&videoId)

	if videoId == "" {
		fmt.Println("视频 ID 不能为空")
		os.Exit(1)
	}

	fetchData(videoId)
}
