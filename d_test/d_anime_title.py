import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 環境変数 'CHROMEDRIVER_PATH' から取得。なければデフォルト値
driver_path = os.environ.get("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver")
service = Service(driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1200,3000")  
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# 対象URL（あ行ページ）
url = "https://animestore.docomo.ne.jp/animestore/c_all_pc?initialCollectionKey=1&vodTypeList=svod_tvod"
driver.get(url)

# 出力用ディレクトリ
os.makedirs("output", exist_ok=True)

# 五十音タブの data-value と対応する仮名
kana_map = {
    "0": "あ",
    "1": "い",
    "2": "う",
    "3": "え",
    "4": "お"
}

# 結果格納用
groups = {kana: [] for kana in kana_map.values()}

# 各タブを順番にクリックして抽出
for data_value, kana in kana_map.items():
    try:
        # ブラウザを毎回起動
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # タブ要素が存在するか確認
        try:
            tab = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f"li[data-value='{data_value}']"))
            )
        except Exception as e:
            print(f"{kana}行タブが見つかりません: {e}")
            driver.quit()
            continue

        tab.click()
        print(f"{kana}行 tab class: {tab.get_attribute('class')}")
        time.sleep(5)  # タブ切り替え待機

        # listContainerを少しずつスクロールして全件読み込む
        scroll_target = driver.find_element(By.CSS_SELECTOR, "div#listContainer")
        last_count = 0
        same_count = 0
        max_retry = 30
        while same_count < max_retry:
            elements = driver.find_elements(By.CSS_SELECTOR, "div#listContainer a.textContainer")
            for el in elements[-10:]:  # 直近10件を順番に表示
                driver.execute_script("arguments[0].scrollIntoView();", el)
                time.sleep(1)  # 少し待つ
            time.sleep(1)  # 少し待つ
            new_elements = driver.find_elements(By.CSS_SELECTOR, "div#listContainer a.textContainer")
            if len(new_elements) == last_count:
                same_count += 1
            else:
                same_count = 0
                last_count = len(new_elements)
        elements = driver.find_elements(By.CSS_SELECTOR, "div#listContainer a.textContainer")
        print(f"{kana}行 a.textContainer要素数: {len(elements)}")
        for el in elements[:5]:
            print(f"{kana}行 el.text: {el.text}")
        for el in elements:
            try:
                title_span = el.find_element(By.CSS_SELECTOR, "span.ui-clamp.webkit2LineClamp")
                title = title_span.text.strip()
                link = el.get_attribute("href")
                # 条件を削除し、全て追加
                groups[kana].append((title, link))
            except Exception as e:
                print(f"タイトルの抽出に失敗しました: {e}")
                continue
        driver.quit()
    except Exception as e:
        print(f"{kana}の抽出に失敗しました: {e}")
        try:
            driver.quit()
        except:
            pass

driver.quit()


for kana in ["あ", "い", "う", "え", "お"]:
    count = len(groups[kana])  # タイトル数を取得
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>あ行の作品一覧</title>
    <style>
        body {{
            font-family: 'Segoe UI', 'Hiragino Sans', 'Meiryo', sans-serif;
            background: #f9f9f9;
            color: #222;
            margin: 40px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            background: #fff;
            margin: 8px 0;
            padding: 12px 16px;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            transition: background 0.2s;
        }}
        li:hover {{
            background: #eaf6ff;
        }}
        a {{
            color: #2980b9;
            text-decoration: none;
            font-size: 1.1em;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>『{kana}』から始まる作品一覧（{count}件）</h1>
    <ul>
"""
    for title, link in sorted(groups[kana]):
        html += f'        <li><a href="{link}" target="_blank">{title}</a></li>\n'

    html += """    </ul>
</body>
</html>"""

    with open(f"output/{kana}.html", "w", encoding="utf-8") as f:
        f.write(html)

print("あ〜おの作品一覧HTMLを output フォルダに生成しました。")