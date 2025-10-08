import os
from bs4 import BeautifulSoup

# 行キーと対応するファイル名（番号付き）
ROW_FILES = [
    ("a", "01_a_tags_processed.html"),
    ("ka", "02_ka_tags_processed.html"),
    ("sa", "03_sa_tags_processed.html"),
    ("ta", "04_ta_tags_processed.html"),
    ("na", "05_na_tags_processed.html"),
    ("ha", "06_ha_tags_processed.html"),
    ("ma", "07_ma_tags_processed.html"),
    ("ya", "08_ya_tags_processed.html"),
    ("ra", "09_ra_tags_processed.html"),
    ("wa", "010_wa_tags_processed.html"),
]

INPUT_FOLDER = "tags_html_folder"
OUTPUT_FILE = "all_tags_combined.html"

# 統合用の空の soup を作成
combined_soup = BeautifulSoup("<div id='all-tags'></div>", "html.parser")
all_tags_div = combined_soup.select_one("#all-tags")

for row_key, filename in ROW_FILES:
    path = os.path.join(INPUT_FOLDER, filename)
    if not os.path.exists(path):
        print(f"⚠️ ファイルが見つかりません: {filename}")
        continue

    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # 各作品ブロックに data-row を追加して統合
    for div in soup.select("div[id]"):
        div["data-row"] = row_key
        all_tags_div.append(div)

# HTML全体を整形して保存
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(combined_soup.prettify())

print(f"✅ 統合完了: {OUTPUT_FILE}")