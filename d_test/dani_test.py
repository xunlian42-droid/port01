import requests

url = "https://anime.dmkt-sp.jp/animestore/rest/WS000103?rankingType=01"
response = requests.get(url)
data = response.json()

# タイトル抽出
titles = [item["workInfo"]["workTitle"] for item in data["data"]["workList"]]

# 五十音順にソート（日本語対応）
titles_sorted = sorted(titles, key=lambda x: x)

for title in titles_sorted:
    print(title)