    const pageList = [
      { href: "comparison_gojuon_with_links/comparison_01_a_with_links.html" },
      { href: "comparison_gojuon_with_links/comparison_02_ka_with_links.html" },
      { href: "comparison_gojuon_with_links/comparison_03_sa_with_links.html" },
      { href: "comparison_gojuon_with_links/comparison_04_ta_with_links.html" },
      { href: "comparison_gojuon_with_links/comparison_05_na_with_links.html" },
      { href: "comparison_gojuon_with_links/comparison_06_ha_with_links.html" },
      { href: "comparison_gojuon_with_links/comparison_07_ma_with_links.html" },
      { href: "comparison_gojuon_with_links/comparison_08_ya_with_links.html" },
      { href: "comparison_gojuon_with_links/comparison_09_ra_with_links.html" },
      { href: "comparison_gojuon_with_links/comparison_10_wa_with_links.html" }
    ];

    let titleIndex = [];

    function generateAnchorId(title) {
      // タイトルからアンカーIDを生成
      return title
        .replace(/[^\p{L}\p{N}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}_]/gu, "_");
    }

    async function buildTitleIndex() {
      titleIndex = [];
      for (const page of pageList) {
        try {
          const res = await fetch(page.href);
          if (!res.ok) continue;
          const html = await res.text();
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");

          // タイトルリンクだけを対象にする
          doc.querySelectorAll("tbody tr td").forEach(tr => {
            const title = tr.textContent.trim();
            if (title) {
              const anchor = generateAnchorId(title);
              titleIndex.push({
                title: title,
                page: page.href,
                anchor: anchor,
                id: tr.dataset.id || null
              });
            }
          });
        } catch (e) {
          console.warn("読み込み失敗:", page.href);
        }
      }
    }

        // タイトル検索用インデックス
    async function doSearch() {
      const query = document.getElementById('search-input').value.trim();
      const exclude = document.getElementById('exclude-input').value.trim();
      const words = query ? query.split(/\s+/) : [];
      const excludes = exclude ? exclude.split(/\s+/) : [];

      if (titleIndex.length === 0) {
        document.getElementById('result-count').textContent = "検索中...";
        await buildTitleIndex();
      }

      const results = titleIndex.filter(item => {
        const match = words.every(w => item.title.includes(w));
        const notExcluded = excludes.every(w => !item.title.includes(w));
        return match && notExcluded;
      });

      const ul = document.getElementById('result-list');
      ul.innerHTML = '';
      results.forEach(item => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = `${item.page}#${item.anchor}`; // ページ＋アンカーでジャンプ
        a.addEventListener("click", () => {
          sessionStorage.setItem("scrollToId", item.anchor);}); // anchor = data-id
        a.textContent = item.title;
        li.appendChild(a);
        ul.appendChild(li);
      });

      document.getElementById('result-count').textContent = `${results.length}件ヒット`;
    }





    document.getElementById('search-form').addEventListener('submit', doSearch);

    document.getElementById('reset-btn').addEventListener('click', function () {
      document.getElementById('search-input').value = '';
      document.getElementById('exclude-input').value = '';
      document.getElementById('result-count').textContent = '';
      const ul = document.getElementById('result-list');
      ul.innerHTML = `
    <li><a href="comparison_gojuon_with_links/comparison_01_a_with_links.html">ア行の作品比較</a></li>
    <li><a href="comparison_gojuon_with_links/comparison_02_ka_with_links.html">カ行の作品比較</a></li>
    <li><a href="comparison_gojuon_with_links/comparison_03_sa_with_links.html">サ行の作品比較</a></li>
    <li><a href="comparison_gojuon_with_links/comparison_04_ta_with_links.html">タ行の作品比較</a></li>
    <li><a href="comparison_gojuon_with_links/comparison_05_na_with_links.html">ナ行の作品比較</a></li>
    <li><a href="comparison_gojuon_with_links/comparison_06_ha_with_links.html">ハ行の作品比較</a></li>
    <li><a href="comparison_gojuon_with_links/comparison_07_ma_with_links.html">マ行の作品比較</a></li>
    <li><a href="comparison_gojuon_with_links/comparison_08_ya_with_links.html">ヤ行の作品比較</a></li>
    <li><a href="comparison_gojuon_with_links/comparison_09_ra_with_links.html">ラ行の作品比較</a></li>
    <li><a href="comparison_gojuon_with_links/comparison_10_wa_with_links.html">ワ行の作品比較</a></li>
  `;
    });



    // タグ検索用インデックス

    const tagIndex = {}; // { "役職:名前": [ { id, title, rowKey } ] }

    async function buildTagIndex() {
      const res = await fetch("tags_html_folder/all_tags_combined.html");
      const html = await res.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, "text/html");

      doc.querySelectorAll("#all-tags > div[id]").forEach(div => {
        const workId = div.id;
        const rowKey = div.dataset.row;
        const title = div.querySelector("h3")?.textContent.trim() || workId;

        div.querySelectorAll("li").forEach(li => {
          const strong = li.querySelector("strong");
          if (!strong) return;
          const role = strong.textContent.replace(/:$/, "");
          const name = li.textContent.replace(strong.textContent, "").trim();
          const key = `${role}:${name}`;
          (tagIndex[key] = tagIndex[key] || []).push({ id: workId, title, rowKey });
        });
      });
    }

    async function doTagSearch() {
      const query = document.getElementById("tag-input").value.trim();
      const keywords = query ? query.split(/\s+/).map(w => w.replace(/\s+/g, "")) : [];
      // 除外語句の取得
      const excludeQuery = document.getElementById("tag-exclude-input").value.trim();
      const excludeKeywords = excludeQuery ? excludeQuery.split(/\s+/).map(w => w.replace(/\s+/g, "")) : [];


      if (Object.keys(tagIndex).length === 0) {
        document.getElementById("tag-result-count").textContent = "タグ読み込み中...";
        await buildTagIndex();
      }


      const results = [];
      // タグキー全体を走査して部分一致
      Object.entries(tagIndex).forEach(([tagKey, entries]) => {
        const normalizedKey = tagKey.replace(/\s+/g, ""); // 空白除去
        const match = keywords.every(word => normalizedKey.includes(word));
        const excluded = excludeKeywords.some(ex => normalizedKey.includes(ex));
        if (match && !excluded) {
          results.push(...entries);
        }
      });


      // 結果表示
      const ul = document.getElementById("tag-result-list");
      ul.innerHTML = "";
      results.forEach(({ id, title, rowKey }) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        const pageHref = `comparison_gojuon_with_links/comparison_${getRowNumber(rowKey)}_${rowKey}_with_links.html`;
        a.href = `${pageHref}#${id}`;
        a.textContent = `${title}`;
        a.addEventListener("click", () => {
          sessionStorage.setItem("scrollToId", id);
        });
        li.appendChild(a);
        ul.appendChild(li);
      });

      document.getElementById("tag-result-count").textContent = `${results.length}件ヒット`;
    }

    document.getElementById("tag-search-form").addEventListener("submit", async (e) => {
      e.preventDefault(); // ページ遷移を防ぐ
      await doTagSearch(); // 検索処理を呼び出す
    });

    document.getElementById("tag-reset-btn").addEventListener("click", () => {
      document.getElementById("tag-input").value = "";
      document.getElementById("tag-result-count").textContent = "";
      document.getElementById("tag-result-list").innerHTML = "";
    });

    document.addEventListener("DOMContentLoaded", async () => {
      await buildTagIndex(); // タグインデックスを事前構築
    });


    // タグポップアップを開く関数
    function openTagPopup() {
      window.open("tag_popup.html", "tagPopup", "width=600,height=700,scrollbars=yes");
    }
    
    // タグポップアップから呼ばれる関数
    window.showTagResults = function (tagKey, entries) {
      const ul = document.getElementById("tag-result-list");
      ul.innerHTML = "";

      entries.forEach(({ id, title, rowKey }) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        const pageHref = `comparison_gojuon_with_links/comparison_${getRowNumber(rowKey)}_${rowKey}_with_links.html`;
        a.href = `${pageHref}#${id}`;
        a.textContent = `${title}`;
        a.addEventListener("click", () => {
          sessionStorage.setItem("scrollToId", id);
        });
        li.appendChild(a);
        ul.appendChild(li);
      });

      document.getElementById("tag-result-count").textContent = `タグ「${tagKey}」に一致する作品：${entries.length}件`;
    };

    function getRowNumber(rowKey) {
      const map = {
        "a": "01", "ka": "02", "sa": "03", "ta": "04", "na": "05",
        "ha": "06", "ma": "07", "ya": "08", "ra": "09", "wa": "10"
      };
      return map[rowKey] || "00";
    }
