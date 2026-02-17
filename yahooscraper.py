import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://tw.news.yahoo.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('h3 a') or soup.select('.Storylink') or soup.select('a.stream-title')
    
    all_news = []
    for news in items:
        title_text = news.get_text().strip()
        link = news.get('href')
        if title_text and link:
            if not link.startswith('http'):
                link = "https://tw.news.yahoo.com" + link
            all_news.append((title_text, link))
    
    # --- 關鍵字過濾 ---
    keywords = ["川普", "股市", "台灣", "天氣"] 
    filtered_news = [
        (title, link) for title, link in all_news 
        if any(word in title for word in keywords)
    ]

    # --- 統一存檔邏輯 (只留這一段) ---
    if filtered_news:
        # 1. 更新 CSV (這會徹底覆蓋舊檔)
        df = pd.DataFrame(filtered_news, columns=['新聞標題', '新聞連結'])
        df.to_csv('yahoo_news.csv', index=False, encoding='utf-8-sig')
        
        # 2. 更新 Markdown
        with open("news_list.md", "w", encoding="utf-8") as md_file:
            md_file.write(f"# 今日關鍵字動態：{', '.join(keywords)}\n\n")
            for i, (title, link) in enumerate(filtered_news, 1):
                md_file.write(f"{i}. [{title}]({link})\n")
        
        print(f"成功！已過濾並更新 {len(filtered_news)} 則新聞。")
    else:
        print("今日無匹配關鍵字的新聞。")
else:
    print(f"連線失敗：{response.status_code}")