(() => {
    const rowKey = window.rowKey || "ya"; // ページごとの行キー（例: "a", "ka", ...）

    document.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll("a.title-link").forEach(a => {
            a.addEventListener("click", e => {
                e.preventDefault();
                const id = a.dataset.id;
                if (!id) return;

                // タグウインドウのURL（アンカーで作品IDを渡す）
                const tagWindowURL = `../tags_html_folder/08_${rowKey}_tags_processed.html#${encodeURIComponent(id)}`;

                // 別ウインドウを開く
                window.open(
                    tagWindowURL,
                    "tagWindow",
                    "width=700,height=800,scrollbars=yes,resizable=yes"
                );
            });
        });
    });

    // 比較表ページに作品IDでスクロールする関数（タグウインドウから呼ばれる）
    window.scrollToTitle = function (id) {
        const target = document.getElementById(id);
        if (target) {
            target.scrollIntoView({ behavior: "smooth", block: "center" });
        }
    };
})();
