import requests
from bs4 import BeautifulSoup
import csv  # 內建套件，不需要 pip install

url = "https://tw.news.yahoo.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('h3 a') or soup.select('.Storylink') or soup.select('a.stream-title')
    
    # 建立一個清單來存資料
    news_list = []
    
    for news in items:
        title_text = news.get_text().strip()
        link = news.get('href')
        if title_text and link:
            if not link.startswith('http'):
                link = "https://tw.news.yahoo.com" + link
            news_list.append([title_text, link]) # 將標題和連結存入

    # --- 存檔邏輯開始 ---
    filename = "yahoo_news.csv"
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["新聞標題", "新聞連結"]) # 寫入標題列
        writer.writerows(news_list[:10])       # 寫入前 10 則新聞
    
    print(f"--- 抓取成功！已存檔至: {filename} ---")
    # --- 存檔邏輯結束 ---
else:
    print(f"連線失敗：{response.status_code}")