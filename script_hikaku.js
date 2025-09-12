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