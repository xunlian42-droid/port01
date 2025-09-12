from bs4 import BeautifulSoup
import re

input_files = [
    {'file': 'C:/Users/0602JP/Desktop/port/output/dani_46_WA.html', 'tag': 'わ'},
    {'file': 'C:/Users/0602JP/Desktop/port/output/dani_47_WO.html', 'tag': 'を'},
    {'file': 'C:/Users/0602JP/Desktop/port/output/dani_48_N.html', 'tag': 'ん'}
]

output_file = '020_wa_gyo_comparison.html'

html_header = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ワ行の作品比較</title>
  <link rel="stylesheet" href="style_hikaku.css">
  <style>
    
  </style>
</head>
<body>
  <h1>ワ行の作品比較</h1>
  <div class="filter-bar">
    <button class="filter-btn" data-filter="わ">わ</button>
    <button class="filter-btn" data-filter="を">を</button>
    <button class="filter-btn" data-filter="ん">ん</button>
    <button class="filter-btn reset" data-filter="all">すべて表示</button>
  </div>
  <table>
    <tr>
      <th>配信あり：◎</th>
      <th>配信なし：✖</th>
    </tr>
  </table>
  <table>
    <thead>
      <tr>
        <th>作品タイトル</th>
        <th>dアニメストア</th>
        <th>DMM TV</th>
      </tr>
    </thead>
    <tbody>
'''

html_footer = '''
    </tbody>
  </table>
  <a href="index.html">トップページに戻る</a>
  <div id="custom-tooltip" class="custom-tooltip"></div>
  <script src="script_hikaku.js"></script>
</body>
</html>
'''

def generate_id(title):
    # 許容する文字：ひらがな、カタカナ、漢字、英数字、長音符「ー」、星「☆★」、中点「・」など
    allowed_chars = r'[^\wぁ-んァ-ン一-龠ー☆★・]'
    clean = re.sub(allowed_chars, '', title)
    return clean[:30]

rows_html = ''
for entry in input_files:
    file = entry['file']
    tag = entry['tag']
    with open(file, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        for li in soup.select('ul li'):
            a_tag = li.find('a')
            if a_tag:
                title = a_tag.text.strip()
                url = a_tag['href']
                row_id = generate_id(title)
                d_anime_cell = f'<a href="{url}" target="_blank">◎</a>'
                dmm_cell = '<span class="no-link">✖</span>'
                title_html = f'<span class="title-span" data-tag="{tag}" data-tags="[]" style="cursor:pointer;text-decoration:underline;">{title}</span>'
                # trタグにid属性を追加
                rows_html += f'<tr id="{row_id}"><td>{title_html}</td><td>{d_anime_cell}</td><td>{dmm_cell}</td></tr>\n'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_header + rows_html + html_footer)