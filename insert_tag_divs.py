from bs4 import BeautifulSoup
import re
import os
import glob

# ファイル名から行クラスを抽出（例: 01_a_tags.html → row-a）
def extract_row_class(filename):
    match = re.search(r'\d{2}_(\w+)_tags\.html', filename)
    if match:
        return f"row-{match.group(1)}"
    return "row-a"  # 万一抽出できない場合はあ行に

# タグHTMLを処理して class を追加
def process_tag_file(input_path, output_path):
    filename = os.path.basename(input_path)
    row_class = extract_row_class(filename)

    with open(input_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # <div id="〇〇"> に class を追加
    for div in soup.find_all("div", id=True):
        div["class"] = div.get("class", []) + [row_class]

    # 保存
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

# 他の行も処理したい場合はループで回せます

for path in glob.glob("tags_html_folder/*_tags.html"):
    output = path.replace("_tags.html", "_tags_processed.html")
    process_tag_file(path, output)
