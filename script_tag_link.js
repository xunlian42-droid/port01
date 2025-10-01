(() => {
  let tagDoc = null;
  const tagIndex = {};

  // 初回ロード
  async function loadTagDoc() {
    if (tagDoc) return tagDoc;
    const res = await fetch("tags_html_folder");
    const text = await res.text();
    tagDoc = new DOMParser().parseFromString(text, "text/html");
    buildTagIndex();
    return tagDoc;
  }

  // tagDoc から「役職:担当者」→作品リストをマップ化
  function buildTagIndex() {
    tagDoc.querySelectorAll("div[id]").forEach(div => {
      const id = div.id;
      const title = div.querySelector("h3").textContent;
      div.querySelectorAll("li").forEach(li => {
        const role = li.querySelector("strong").textContent.replace(/:$/, "");
        const name = li.textContent.replace(li.querySelector("strong").textContent, "").trim();
        const key = `${role}:${name}`;
        if (!tagIndex[key]) tagIndex[key] = [];
        tagIndex[key].push({ id, title });
      });
    });
  }

  // モーダルに指定作品のタグ一覧を表示
  async function openPopup(id) {
    const modal = document.getElementById("modal");
    const body = document.getElementById("popup-body");
    modal.style.display = "block";
    body.innerHTML = "読み込み中…";

    try {
      const doc = await loadTagDoc();
      const block = doc.getElementById(id);
      if (!block) throw new Error("情報が見つかりません");
      const frag = document.createDocumentFragment();

      block.querySelectorAll("li").forEach(li => {
        const clone = li.cloneNode(true);
        const role = clone.querySelector("strong").textContent.replace(/:$/, "");
        const name = clone.textContent.replace(clone.querySelector("strong").textContent, "").trim();
        const key = `${role}:${name}`;
        const span = document.createElement("span");
        span.className = "tag-item";
        span.textContent = `${role}: ${name}`;
        span.dataset.tagKey = key;
        frag.appendChild(span);
      });

      body.innerHTML = "";
      body.appendChild(frag);

      // タグクリックで結果表示
      body.querySelectorAll(".tag-item").forEach(el => {
        el.addEventListener("click", () => showTagResults(el.dataset.tagKey));
      });
    } catch (err) {
      body.textContent = "読み込みエラー: " + err.message;
    }
  }

  // 選択タグで共通作品リストを表示
  function showTagResults(tagKey) {
    const body = document.getElementById("popup-body");
    const entries = tagIndex[tagKey] || [];
    if (entries.length === 0) {
      body.innerHTML = "<p>該当作品がありません。</p>";
      return;
    }

    body.innerHTML = `<h4>タグ「${tagKey}」を持つ作品</h4>`;
    const ul = document.createElement("ul");
    entries.forEach(({ id, title }) => {
      const li = document.createElement("li");
      li.className = "result-item";
      const a = document.createElement("a");
      a.textContent = title;
      a.dataset.id = id;
      a.addEventListener("click", () => openPopup(id));
      li.appendChild(a);
      ul.appendChild(li);
    });
    body.appendChild(ul);
  }

  // モーダルを閉じるハンドラ
  document.addEventListener("click", e => {
    if (e.target.id === "close-btn") {
      document.getElementById("modal").style.display = "none";
    }
  });

  // 比較表のタイトルリンクにハンドラを設定
  document.querySelectorAll("a.title-link").forEach(a => {
    a.addEventListener("click", () => openPopup(a.dataset.id));
  });
})();

document.addEventListener('DOMContentLoaded', function () {
  // フィルタ機能
  const filterBtns = document.querySelectorAll('.filter-btn');
  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filterBtns.forEach(b => b.classList.remove('active'));
      if (btn.dataset.filter !== "all") btn.classList.add('active');
      const filter = btn.getAttribute('data-filter');
      document.querySelectorAll('tbody tr').forEach(function (row) {
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
});