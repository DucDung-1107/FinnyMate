import pandas as pd
import numpy as np
df=pd.read_csv(r"C:\Users\Admin\Downloads\all_news_20250426 (1).csv")

import pandas as pd
df['date'] = pd.to_datetime(df['date'])
#sắp xếp theo cột date
df = df.sort_values(by='date')
import pandas as pd
import numpy as np

# Assuming df and the 'source' column already exist from previous code
df['source'] = df['source'].str.replace('/rss', '', regex=False)
#reset index
df = df.reset_index(drop=True)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# --- HÀM TẠO CHROME DRIVER ---
def create_driver():
    options = Options()
    options.add_argument("--headless=new")  # headless chế độ mới
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

# --- HÀM LẤY NỘI DUNG BÀI BÁO ---
def get_real_article_content(driver, news_google_url):
    try:
        driver.get(news_google_url)
        time.sleep(random.uniform(2, 4))  # Random thời gian chờ

        real_article_url = driver.current_url
        print(f"✅ Link bài báo gốc: {real_article_url}")

        if "news.google.com" in real_article_url:
            print("⚠️ Không lấy được link bài báo gốc.")
            return None

        driver.get(real_article_url)
        time.sleep(random.uniform(2, 4))

        soup = BeautifulSoup(driver.page_source, "html.parser")

        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        full_text = soup.get_text(separator="\n", strip=True)

        return full_text

    except Exception as e:
        print(f"❌ Lỗi khi lấy bài báo: {e}")
        return None


df['content'] = pd.Series(dtype=str)

# --- CHẠY QUÉT DỮ LIỆU ---
driver = create_driver()

for i in range(len(df)):
    try:
        if pd.isnull(df.loc[i, 'content']):
            url = df.loc[i, 'source']
            full_text = get_real_article_content(driver, url)

            if full_text:
                df.loc[i, 'content'] = full_text
                print(f"✅ Đã lưu nội dung bài {i}")

            else:
                print(f"⚠️ Không lấy được nội dung bài {i}")

            # Pause random mỗi bài
            time.sleep(random.uniform(5, 10))

            # Restart driver mỗi 5 bài
            if (i + 1) % 5 == 0:
                driver.quit()
                print("🔄 Restart driver...")
                time.sleep(random.uniform(5, 8))
                driver = create_driver()

    except Exception as e:
        print(f"❌ Lỗi ở bài {i}: {e}")
        continue  # Bỏ qua lỗi, chạy tiếp

driver.quit()

print(df)
df.to_csv('outputnews.csv', index=False)  # Save nếu cần
