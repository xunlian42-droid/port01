from bs4 import BeautifulSoup

input_files = [
    {'file': 'C:/Users/0602JP/Desktop/port/output/dani_46_WA.html', 'tag': 'わ'},
    {'file': 'C:/Users/0602JP/Desktop/port/output/dani_47_WO.html', 'tag': 'を'},
    {'file': 'C:/Users/0602JP/Desktop/port/output/dani_48_N.html', 'tag': 'ん'},
]

output_file = '020_wa_gyo_comparison.html'

html_header = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ワ行の作品比較</title>
  <style>
    body { font-family: sans-serif; padding: 20px; background: #f9f9f9; }
    table { width: 100%; border-collapse: collapse; background: #fff; }
    th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
    th { background-color: #e0e0e0; }
    tr:nth-child(even) { background-color: #f2f2f2; }
    .no-link { color: gray; }
    .custom-tooltip {
      display: none;
      position: absolute;
      background: #fffbe7;
      color: #333;
      border: 1px solid #ffd700;
      border-radius: 6px;
      padding: 8px 16px;
      font-size: 1em;
      z-index: 1000;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
      pointer-events: auto;
      white-space: nowrap;
      min-width: 200px;
    }
    .tooltip-tag {
      display: inline-block;
      background: #ffd700;
      color: #333;
      border-radius: 4px;
      padding: 2px 10px;
      margin: 2px 4px;
      font-size: 1em;
      cursor: pointer;
    }
    .tooltip-tag-remove {
      color: #f00;
      margin-left: 4px;
      cursor: pointer;
      font-weight: bold;
    }
    .tooltip-tag-input {
      margin-top: 8px;
      width: 120px;
      font-size: 1em;
      padding: 2px 6px;
    }
    .tooltip-tag-add-btn {
      margin-left: 4px;
      padding: 2px 8px;
      font-size: 1em;
      cursor: pointer;
    }
    .filter-bar {
      margin-bottom: 16px;
    }
    .filter-btn {
      display: inline-block;
      background: #ffd700;
      color: #333;
      border-radius: 4px;
      padding: 4px 14px;
      margin-right: 8px;
      font-size: 1em;
      cursor: pointer;
      border: none;
      outline: none;
      transition: background 0.2s;
    }
    .filter-btn.active {
      background: #ff9800;
      color: #fff;
    }
    .filter-btn.reset {
      background: #e0e0e0;
      color: #333;
    }
  </style>
</head>
<body>
  <h1>📺 ワ行の作品比較</h1>
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
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      // フィルタ機能
      const filterBtns = document.querySelectorAll('.filter-btn');
      filterBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
          filterBtns.forEach(b => b.classList.remove('active'));
          if(btn.dataset.filter !== "all") btn.classList.add('active');
          const filter = btn.getAttribute('data-filter');
          document.querySelectorAll('tbody tr').forEach(function(row) {
            const titleSpan = row.querySelector('.title-span[data-tag]');
            if (!titleSpan) return;
            const tag = titleSpan.getAttribute('data-tag');
            if (filter === 'all' || tag === filter) {
              row.style.display = '';
            } else {
              row.style.display = 'none';
            }
          });
        });
      });

      // ポップアップの表示・非表示制御用フラグ
      let tooltipHover = false;

      // タイトルクリックでポップアップ
      const tooltip = document.getElementById('custom-tooltip');
      let lastTarget = null;
      document.querySelectorAll('td > span[data-tag].title-span').forEach(function(span) {
        span.addEventListener('click', function(e) {
          e.stopPropagation();
          const tag = span.getAttribute('data-tag');
          let tags = [];
          try {
            tags = JSON.parse(span.getAttribute('data-tags') || '[]');
          } catch { tags = []; }
          if (lastTarget === span && tooltip.style.display === 'block') {
            tooltip.style.display = 'none';
            lastTarget = null;
            return;
          }
          // 固定タグ（五十音）と追加タグを分けて表示
          let tagsHtml = '<span class="tooltip-tag" data-fixed="1" data-tag="' + tag + '">' + tag + '</span>';
          tagsHtml += tags.map(function(t, idx) {
            return '<span class="tooltip-tag">' + t +
              '<span class="tooltip-tag-remove" data-idx="' + idx + '">×</span></span>';
          }).join('');
          tagsHtml += '<div><input class="tooltip-tag-input" type="text" placeholder="タグを追加">' +
                      '<button class="tooltip-tag-add-btn">追加</button></div>';
          tooltip.innerHTML = tagsHtml;
          const rect = span.getBoundingClientRect();
          tooltip.style.left = (window.scrollX + rect.left) + 'px';
          tooltip.style.top = (window.scrollY + rect.bottom + 4) + 'px';
          tooltip.style.display = 'block';
          lastTarget = span;

          // 入力欄やポップアップ上での操作で消えないように
          tooltip.onmouseenter = function() { tooltipHover = true; };
          tooltip.onmouseleave = function() { tooltipHover = false; setTimeout(function(){
            if(!tooltipHover) { tooltip.style.display = 'none'; lastTarget = null; }
          }, 100); };
          // 入力欄でのクリック・入力時も消えないように
          const input = tooltip.querySelector('.tooltip-tag-input');
          if (input) {
            input.addEventListener('mousedown', function(ev) { ev.stopPropagation(); });
            input.addEventListener('click', function(ev) { ev.stopPropagation(); });
            input.addEventListener('keydown', function(ev) { ev.stopPropagation(); });
          }

          // 固定タグクリックでフィルタ
          tooltip.querySelectorAll('.tooltip-tag[data-fixed="1"]').forEach(function(btn) {
            btn.onclick = function(ev) {
              ev.stopPropagation();
              const tag = btn.getAttribute('data-tag');
              document.querySelector('.filter-btn[data-filter="' + tag + '"]').click();
              tooltip.style.display = 'none';
              lastTarget = null;
            };
          });

          // タグ追加
          tooltip.querySelector('.tooltip-tag-add-btn').onclick = function(ev) {
            ev.stopPropagation();
            const input = tooltip.querySelector('.tooltip-tag-input');
            const newTag = input.value.trim();
            if (newTag && !tags.includes(newTag)) {
              tags.push(newTag);
              span.setAttribute('data-tags', JSON.stringify(tags));
              input.value = '';
              span.click();
            }
          };
          // タグ削除
          tooltip.querySelectorAll('.tooltip-tag-remove').forEach(function(btn) {
            btn.onclick = function(ev) {
              ev.stopPropagation();
              const idx = parseInt(btn.getAttribute('data-idx'));
              tags.splice(idx, 1);
              span.setAttribute('data-tags', JSON.stringify(tags));
              span.click();
            };
          });
        });
      });

      // ポップアップ自体での操作で消えないように
      tooltip.addEventListener('mousedown', function(ev) { ev.stopPropagation(); });
      tooltip.addEventListener('click', function(ev) { ev.stopPropagation(); });

      // どこかクリックでポップアップ閉じる（ただしポップアップ上は除外）
      document.addEventListener('mousedown', function(e) {
        if (!tooltipHover) {
          tooltip.style.display = 'none';
          lastTarget = null;
        }
      });
    });
  </script>
</body>
</html>
'''

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
                d_anime_cell = f'<a href="{url}" target="_blank">◎</a>'
                dmm_cell = '<span class="no-link">✖</span>'
                # タイトルspanにdata-tags属性（初期空）を追加
                title_html = f'<span class="title-span" data-tag="{tag}" data-tags="[]" style="cursor:pointer;text-decoration:underline;">{title}</span>'
                rows_html += f'<tr><td>{title_html}</td><td>{d_anime_cell}</td><td>{dmm_cell}</td></tr>\n'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_header + rows_html + html_footer)