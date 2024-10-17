node ./src/index.js

$urls = Get-Content -Path 'urls.txt'

foreach ($url in $urls) {
    if ($url.Trim() -ne '') {
        # 确保不下载空行
        Write-Host "正在下载: $url"
        curl -O $url
    }
}

Read-Host -Prompt "下载完成。按任意键退出"
