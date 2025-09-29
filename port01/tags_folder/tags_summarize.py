import json
import re
import os

INPUT_JSON = "tags_folder/01_a_row_results.json"
OUTPUT_HTML = "tags_folder/a_tags.html"

def split_outside(text: str, seps: tuple[str, ...]) -> list[str]:
    """
    括弧外の区切り文字だけで text を分割するユーティリティ。
    対応括弧：(), （）, 「」, 『』, [], {}, 〈〉, 《》, “”（全角/半角）
    """
    pairs = {
        '(': ')', '（': '）', '「': '」', '『': '』',
        '[': ']', '{': '}', '〈': '〉', '《': '》', '“': '”', '‘': '’'
    }
    opens = set(pairs.keys())
    closes = set(pairs.values())
    stack = []
    buf = []
    out = []

    for ch in text:
        if ch in opens:
            stack.append(pairs[ch])
            buf.append(ch)
        elif ch in closes and stack and ch == stack[-1]:
            stack.pop()
            buf.append(ch)
        elif not stack and ch in seps:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)

    if buf:
        out.append("".join(buf))
    return out

def parse_staff(staff_str: str) -> list[tuple[str,str]]:
    """
    '役職:担当者' セグメントを抽出して (役職, 担当者) のリストを返す。
    - トップレベルの "／" で分割（括弧外のみ）
    - 役職は "・" で分割（括弧外のみ）
    - 担当者は "・", "、", "," で分割（括弧外のみ）
    """
    if not staff_str:
        return []

    # 1) セクションを括弧外の "／" で分割
    sections = split_outside(staff_str, ("／",))
    results = []

    for sec in sections:
        if ":" not in sec:
            continue
        role_part, name_part = sec.split(":", 1)

        # 2) 役職部分を括弧外の "・" で分割
        roles = [r.strip() for r in split_outside(role_part, ("・",)) if r.strip()]

        # 3) 担当者部分を括弧外の "・", "、", "," で分割
        names = [n.strip() for n in split_outside(name_part, ("・","、",",")) if n.strip()]

        # 4) 全組み合わせを結果に追加
        for r in roles:
            for n in names:
                results.append((r, n))

    return results

def safe_id(title: str) -> str:
    """
    HTML id 属性やファイル名に使える形に変換。
    空白・記号をアンダースコアに置換。
    """
    return re.sub(r"[^\w一-龥ぁ-んァ-ヶ]", "_", title)

def main():
    # JSON 読み込み
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        records = json.load(f)

    # HTML ブロックを生成
    blocks = []
    for item in records:
        title = item.get("title", "").strip()
        staff_str = item.get("スタッフ", "").strip()
        year = item.get("製作年", "").strip()
        div_id = safe_id(title)

        html = [f'<div id="{div_id}">', f'  <h3>{title}</h3>', '  <ul>']

        # スタッフタグを分割・追加
        for role, name in parse_staff(staff_str):
            html.append(f'    <li><strong>{role}:</strong> {name}</li>')

        # 製作年タグを追加
        if year:
            html.append(f'    <li><strong>製作年:</strong> {year}</li>')

        html.append('  </ul>')
        html.append('</div>\n')
        blocks.append("\n".join(html))

    # ファイル出力
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write("\n".join(blocks))

    print(f"✅ {OUTPUT_HTML} を生成しました")

if __name__ == "__main__":
    main()