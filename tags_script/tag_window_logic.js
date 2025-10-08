(async () => {
    const hashId = decodeURIComponent(location.hash.slice(1));
    const allTags = document.getElementById("all-tags");
    const container = document.getElementById("tag-container");
    let currentId = null;

    // 1. 全ブロックをインデックス化
    const tagIndex = {};
    allTags.querySelectorAll("div[id]").forEach(div => {
        const workId = div.id;
        const title = div.querySelector("h3")?.textContent.trim() || workId;
        div.querySelectorAll("li").forEach(li => {
            const strong = li.querySelector("strong");
            if (!strong) return;
            const role = strong.textContent.replace(/:$/, "");
            const name = li.textContent.replace(strong.textContent, "").trim();
            const key = `${role}:${name}`;
            ; (tagIndex[key] = tagIndex[key] || []).push({ id: workId, title });
        });
    });

    // 2. 初期表示ブロックを見つけ、currentId にセット
    if (!allTags.querySelector(`#${CSS.escape(hashId)}`)) {
        container.innerHTML = "<p>タグ情報が見つかりません。</p>";
        return;
    }
    currentId = hashId;

    // 3. 作品タグ一覧を container に描画
    function showTagsFor(workId) {
        const blk = allTags.querySelector(`#${CSS.escape(workId)}`);
        if (!blk) return;
        const frag = document.createDocumentFragment();
        blk.querySelectorAll("li").forEach(li => {
            const strong = li.querySelector("strong");
            if (!strong) return;
            const role = strong.textContent.replace(/:$/, "");
            const name = li.textContent.replace(strong.textContent, "").trim();
            const key = `${role}:${name}`;
            const span = document.createElement("span");
            span.className = "tag-item";
            span.textContent = `${role}: ${name}`;
            span.dataset.tagKey = key;
            frag.appendChild(span);
        });
        // containerを書き換え
        container.innerHTML = `<h3>${blk.querySelector("h3")?.textContent}</h3>`;
        container.appendChild(frag);
        // タグクリックを再アタッチ
        container.querySelectorAll(".tag-item").forEach(el => {
            el.addEventListener("click", () => showTagResults(el.dataset.tagKey));
        });
    }

    // 4. 絞り込み結果を container に描画
    function showTagResults(tagKey) {
        const entries = tagIndex[tagKey] || [];
        if (!entries.length) {
            container.innerHTML = `<p>タグ「${tagKey}」を持つ作品は見つかりません。</p>`;
            return;
        }
        container.innerHTML = `<h4>タグ「${tagKey}」を持つ作品</h4>`;
        const ul = document.createElement("ul");
        entries.forEach(({ id, title }) => {
            const li = document.createElement("li");
            const a = document.createElement("a");
            a.textContent = title;
            a.href = "#";
            a.addEventListener("click", e => {
                e.preventDefault();
                if (window.opener && !window.opener.closed) {
                    window.opener.scrollToTitle(id);
                    window.close();
                }
            });
            li.appendChild(a);
            ul.appendChild(li);
        });
        // 戻るリンク
        const back = document.createElement("a");
        back.href = "#";
        back.textContent = "← タグ一覧に戻る";
        back.className = "back-to-tags";
        back.addEventListener("click", e => {
            e.preventDefault();
            showTagsFor(currentId);
        });

        container.appendChild(ul);
        container.appendChild(back);
    }

    // 5. 行ジャンプ・検索も container 外でそのまま動作
    // document.querySelectorAll(".gojuon-nav button").forEach(btn => {
    //     btn.addEventListener("click", () => {
    //         const row = btn.dataset.row;
    //         const target = allTags.querySelector(`.row-${row}`);
    //         if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    //     });
    // });

    // document.getElementById("search-box")?.addEventListener("input", e => {
    //     const kw = e.target.value.trim();
    //     allTags.querySelectorAll("div[id]").forEach(div => {
    //         const t = div.querySelector("h3")?.textContent || "";
    //         div.style.display = t.includes(kw) ? "" : "none";
    //     });
    // });

    // 6. 初期表示
    showTagsFor(currentId);
})();
