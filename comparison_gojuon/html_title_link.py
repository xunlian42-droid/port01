from bs4 import BeautifulSoup
import re

INPUT_FILE  = "comparison_gojuon/comparison_10_wa.html"
OUTPUT_FILE = "comparison_10_wa_with_links.html"

def safe_id(title: str) -> str:
    """
    HTMLの id 属性に使える文字列を返す。
    英数字・日本語・アンダースコア以外をアンダースコアに置換。
    先頭末尾のアンダースコアを削除。
    """
    # 英数字・日本語・アンダースコア以外をアンダースコアに
    id_str = re.sub(r"[^\w一-龥ぁ-んァ-ヶ]", "_", title)
    # 連続アンダースコアを1つにまとめ、前後のアンダースコアを除去
    # id_str = re.sub(r"_+", "_", id_str).strip("_")
    return id_str

def main():
    # HTML読み込み
    with open(INPUT_FILE, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # <table> の1列目セルを処理（ヘッダ行はスキップ）
    for row in soup.select("table tr")[1:]:
        cols = row.find_all("td")
        if not cols:
            continue

        title_td = cols[0]
        title_text = title_td.get_text(strip=True)
        if not title_text:
            continue

        # 安全なidを生成
        anchor_id = safe_id(title_text)

        # tr自体にidを付与（スクロール用）
        row["id"] = anchor_id

        # aタグを作成
        a_tag = soup.new_tag("a", **{
            "class": "title-link",
            "data-id": safe_id(title_text)
        })
        a_tag.string = title_text

        # 既存のテキストをクリアしてaタグを挿入
        title_td.clear()
        title_td.append(a_tag)

    # 結果を書き出し
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"✅ {OUTPUT_FILE} を生成しました")

if __name__ == "__main__":
    main()