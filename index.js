const fs = require('fs');
const readline = require('readline');

async function getData(url, token) {
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': `online_token=${token}`
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch data from ${url}: ${response.statusText}`);
    }

    return response.json();
}

async function fetchData(videoId) {
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiTkpURUNIIl0sImV4cCI6MTcyOTM0Mjg0MCwiaWF0IjoxNzI4NzM4MDQwLCJpc3MiOiJNQVJTIiwicmxlIjoidXNlciIsInN1YiI6IjIwMjIyMTAxOTA4MSIsInVpZCI6IjY2ZDA3MmY3OTk3ZWJjYzY1NGEwMmMwNyJ9.Omtptc0i9OxJbj0Lw7x5a8H4ZIrqOJ4kfp503QwcFAo';
    const url = `https://online.njtech.edu.cn/api/v2/videos/${videoId}?id=${videoId}`;

    try {
        const data = await getData(url, token);
        const apiUrl = `https://online.njtech.edu.cn/api/v2/video_seasons/${data.seasons[0]["id"]}?order=asc&orderBy=index`;

        const seasonData = await getData(apiUrl, token);

        fs.writeFileSync('api.json', JSON.stringify(seasonData, null, 2));
        console.log('数据已成功保存到 api.json');

    } catch (error) {
        console.error(error);
    }
}

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('请输入视频 ID: ', (videoId) => {
    if (!videoId) {
        console.error('视频 ID 不能为空');
        rl.close();
        return;
    }
    fetchData(videoId).finally(() => rl.close());
});
