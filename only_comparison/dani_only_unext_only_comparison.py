# タイトルをタイトル欄に、
# dアニメストア側に無いタイトルのunextのurlリンクをU-NEXTの欄に、
# unext側に無いタイトルのdアニメのurlリンクをdアニメの欄に、
# only_comparison/only_comparison.htmlに出力するスクリプト
import os
from bs4 import BeautifulSoup

INPUT_FILE  = os.path.join(os.path.dirname(__file__), "../comparison_gojuon_with_links/comparison_10_wa_with_links.html")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "10_wa_only_comparison.html")

def main():

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")


    output_soup = BeautifulSoup(
        "<table>"
        "  <thead><tr>"
        "    <th>タイトル</th>"
        "    <th>dアニメ</th>"
        "    <th>U-NEXT</th>"
        "  </tr></thead>"
        "  <tbody></tbody>"
        "</table>",
        "html.parser"
    )
    tbody = output_soup.tbody

    for tr in soup.select("table tbody tr"):
        tds = tr.find_all("td")
        if len(tds) != 3:
            continue

        title_td, dani_td, unext_td = tds

        dani_no_link  = dani_td.find("span", class_="no-link")
        unext_no_link = unext_td.find("span", class_="no-link")

        # dアニメストア側に無い or U-NEXT側に無いタイトルを抽出
        if dani_no_link is None and unext_no_link is None:
            continue

        new_tr = output_soup.new_tag("tr", id=tr.get("id"), **{"data-kana": tr.get("data-kana")})

        # 1列目：タイトル
        new_td1 = output_soup.new_tag("td")
        new_a1  = output_soup.new_tag(
            "a",
            **{"class": "title-link", "data-id": title_td.a.get("data-id") if title_td.a else ""}
        )
        new_a1.string = title_td.get_text(strip=True)
        new_td1.append(new_a1); new_tr.append(new_td1)

        # 2列目：dアニメ
        new_td2 = output_soup.new_tag("td", style="text-align:center;")
        if dani_no_link is not None:
            new_span = output_soup.new_tag("span", **{"class":"no-link"})
            new_span.string = "✖"
            new_td2.append(new_span)
        else:
            new_a2 = output_soup.new_tag("a", href=dani_td.a.get("href") if dani_td.a else "#", target="_blank")
            new_a2.string = "◎"
            new_td2.append(new_a2)
        new_tr.append(new_td2)

        # 3列目：U-NEXT
        new_td3 = output_soup.new_tag("td", style="text-align:center;")
        if unext_no_link is not None:  # U-NEXTにリンクが無い
            new_span = output_soup.new_tag("span", **{"class":"no-link"})
            new_span.string = "✖"
            new_td3.append(new_span)
        else:
            new_a3 = output_soup.new_tag("a", href=unext_td.a.get("href") if unext_td.a else "#", target="_blank")
            new_a3.string = "◎"
            new_td3.append(new_a3)
        new_tr.append(new_td3)

        tbody.append(new_tr)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(str(output_soup))
    
    # ログ
    total = len(output_soup.tbody.find_all("tr"))
    missing = len(output_soup.tbody.find_all("span", class_="no-link"))
    print(f"リンクが無いタイトル: {missing} 件")
    print(f"→ 書き出し完了: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
