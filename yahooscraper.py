import requests
from bs4 import BeautifulSoup
import pandas as pd  # 這裡一定要加，否則會報錯

url = "https://tw.news.yahoo.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('h3 a') or soup.select('.Storylink') or soup.select('a.stream-title')
    
    # 1. 先把所有新聞抓下來存進 news_list
    all_news = []
    for news in items:
        title_text = news.get_text().strip()
        link = news.get('href')
        if title_text and link:
            if not link.startswith('http'):
                link = "https://tw.news.yahoo.com" + link
            all_news.append((title_text, link))
    
    # 2. 定義關鍵字並過濾
    keywords = ["川普", "股市", "台灣", "天氣"] # 這裡多加幾個關鍵字，比較容易測試成功
    filtered_news = [
        (title, link) for title, link in all_news 
        if any(word in title for word in keywords)
    ]

    # 3. 判斷是否有抓到符合的新聞並存檔
    if filtered_news:
        # 存成 CSV
        df = pd.DataFrame(filtered_news, columns=['新聞標題', '新聞連結'])
        df.to_csv('yahoo_news.csv', index=False, encoding='utf-8-sig')
        
        # 產生可點擊連結的 Markdown 日報
        with open("news_list.md", "w", encoding="utf-8") as md_file:
            md_file.write(f"# 今日關鍵字動態：{', '.join(keywords)}\n\n")
            for i, (title, link) in enumerate(filtered_news, 1):
                md_file.write(f"{i}. [{title}]({link})\n")
        
        print(f"--- 成功！抓到 {len(filtered_news)} 則相關新聞，已更新 csv 與 md 檔 ---")
    else:
        # 如果沒抓到關鍵字新聞，我們至少產生一個說明文件
        with open("news_list.md", "w", encoding="utf-8") as md_file:
            md_file.write(f"# 今日關鍵字動態\n\n今天沒有關於 {', '.join(keywords)} 的新聞。")
        print("今天沒有包含這些關鍵字的新聞。")
else:
    print(f"連線失敗：{response.status_code}")