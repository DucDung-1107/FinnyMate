import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fetch_news(queries, start_year, end_year):
    all_articles = []

    for year in range(start_year, end_year + 1):
        print(f"Đang lấy tin tức năm {year}...")

        for query in queries:
            search_query = f"{query} {year}"
            rss_url = f"https://news.google.com/rss/search?q={search_query}&hl=vi&gl=VN&ceid=VN:vi"

            response = requests.get(rss_url)
            if response.status_code != 200:
                print(f"Lỗi {response.status_code} khi lấy RSS năm {year} với từ khóa {query}")
                continue

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all('item')

            for item in items:
                all_articles.append({
                    "year": year,
                    "title": item.title.text,
                    "date": item.pubDate.text,
                    "source": item.link.text,   # Thêm link bài báo
                })

    return all_articles

# ----------- CHẠY -------------
queries = ["FPT"]  # Thêm các từ khóa vào đây
start_year = 2017
end_year = 2025

# Lấy tất cả bài
news_data = fetch_news(queries, start_year, end_year)

# Lưu ra file CSV
df = pd.DataFrame(news_data)

if not df.empty:
    today = datetime.now().strftime("%Y%m%d")
    filename = f"all_news_{today}.csv"  # Đổi tên file để phản ánh nội dung
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"✅ Đã lưu {len(df)} bài viết vào file {filename}")
else:
    print("⚠️ Không có bài viết nào được tìm thấy.")
