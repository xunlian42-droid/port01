import requests

# ランキングAPI（非公式）
url = "https://animestore.docomo.ne.jp/animestore/c_all_pc?initialCollectionKey=1&vodTypeList=svod_tvod"
response = requests.get(url)
data = response.json()

# タイトル抽出
titles = [item["workInfo"]["workTitle"] for item in data["data"]["workList"]]

# 五十音順にソート（日本語対応）
titles_sorted = sorted(titles, key=lambda x: x)

# HTML生成
html = "<!DOCTYPE html>\n<html lang='ja'>\n<head>\n<meta charset='UTF-8'>\n<title>dアニメ作品一覧</title>\n</head>\n<body>\n<h1>配信作品（五十音順）</h1>\n<ul>\n"

for title in titles_sorted:
    html += f"<li>{title}</li>\n"

html += "</ul>\n</body>\n</html>"

# ファイルに保存（GitHub Pages用）
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTMLファイルを生成しました：index.html")