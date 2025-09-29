import json
import re
import unicodedata
from difflib import SequenceMatcher
import html

# — 正規化 & 類似度判定 — #

def normalize(text: str) -> str:
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'(TVアニメ|ＴＶアニメ|アニメ)', '', text)
    text = re.sub(r'[\s\(\)（）「」『』【】・♪★☆…〜～\-–\/／:：,，\.。!！\?？]+', '', text)
    text = text.translate({ord(k): ord(chr(ord(k) - 0x60)) for k in map(chr, range(ord('ァ'), ord('ン')+1))})
    return text.lower()

def similar(a: str, b: str, threshold: float = 0.8) -> bool:
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio() >= threshold

# — データ読み込み & マッチング — #

def build_groups(*unext_paths, danime_path, threshold=0.8):
    # U-NEXTデータを統合
    unext = []
    for path in unext_paths:
        with open(path, encoding='utf-8') as f:
            unext += json.load(f)

    # dアニメデータ
    with open(danime_path, encoding='utf-8') as f:
        danime = json.load(f)

    # 正規化付きリスト
    unext_list = [{'title': u['title'], 'url': u['url'], 'key': normalize(u['title'])} for u in unext]
    danime_list = [{'title': d['title'], 'url': d['url'], 'key': normalize(d['title'])} for d in danime]

    matched_danime = set()
    groups = []

    # U-NEXT をベースに dアニメと照合
    for u in unext_list:
        best_match = None
        best_score = 0.0
        for d in danime_list:
            if d['title'] in matched_danime:
                continue
            score = SequenceMatcher(None, u['key'], d['key']).ratio()
            if score > best_score:
                best_score = score
                best_match = d
        if best_score >= threshold:
            matched_danime.add(best_match['title'])
            groups.append({
                'title': best_match['title'],
                'danime_url': best_match['url'],
                'unext_url': u['url']
            })
        else:
            groups.append({
                'title': u['title'],
                'danime_url': None,
                'unext_url': u['url']
            })

    # dアニメ専用作品を追加
    for d in danime_list:
        if d['title'] not in matched_danime:
            groups.append({
                'title': d['title'],
                'danime_url': d['url'],
                'unext_url': None
            })

    # ソート（正規化キー順）
    groups.sort(key=lambda g: normalize(g['title']))
    return groups

# — HTML生成 — #

def render_html(groups, output_path):
    html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>U-NEXT × dアニメ配信比較表</title>
  <style>
    body {{ font-family: sans-serif; padding: 20px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background: #f0f0f0; }}
    .no-link {{ color: #999; }}
  </style>
</head>
<body>
  <h1>U-NEXT × dアニメ配信比較表</h1>
  <table>
    <thead>
      <tr><th>作品タイトル</th><th>dアニメストア</th><th>U-NEXT</th></tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>
"""
    row_html = []
    for g in groups:
        title = html.escape(g['title'])
        d_cell = f'<a href="{g["danime_url"]}" target="_blank">◎</a>' if g['danime_url'] else '<span class="no-link">✖</span>'
        u_cell = f'<a href="{g["unext_url"]}" target="_blank">◎</a>' if g['unext_url'] else '<span class="no-link">✖</span>'
        row = f"""      <tr>
        <td>{title}</td>
        <td style="text-align:center;">{d_cell}</td>
        <td style="text-align:center;">{u_cell}</td>
      </tr>"""
        row_html.append(row)

    html_content = html_template.format(rows="\n".join(row_html))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML出力完了 → {output_path}")

# — メイン処理 — #
if __name__ == '__main__':
    groups = build_groups(
        'unext_extraction/unext_titles_part_027.json',
        danime_path='dani_extraction/10_d_wa_title_comparison.json',
        threshold=0.8
    )
    render_html(groups, 'comparison_10_wa.html')