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
            # --- 從第 25 行開始取代 ---
# 定義你想追蹤的關鍵字
keywords = ["川普", "股市"]

# 關鍵字過濾：標題中只要出現任一關鍵字就保留
filtered_news = [
    (title, link) for title, link in news_list 
    if any(word in title for word in keywords)
]

# 判斷是否有抓到符合的新聞
if filtered_news:
    # 存成 CSV
    df = pd.DataFrame(filtered_news, columns=['標題', '連結'])
    df.to_csv('yahoo_news.csv', index=False, encoding='utf-8-sig')
    
    # 新增：同時產生可點擊的 Markdown 日報
    with open("news_list.md", "w", encoding="utf-8") as md_file:
        md_file.write(f"# 今日關鍵字動態：{', '.join(keywords)}\n\n")
        for i, (title, link) in enumerate(filtered_news, 1):
            md_file.write(f"{i}. [{title}]({link})\n")
    print(f"成功！抓到 {len(filtered_news)} 則相關新聞。")
else:
    print("今天沒有包含這些關鍵字的新聞。")

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