import re

def split_outside(text: str, seps: tuple[str, ...]) -> list[str]:
    """
    括弧外の区切り文字（seps）だけで text を分割する。
    対応括弧：(), （）, 「」, 『』, [], {}, 〈〉, 《》, “” （全角/半角）
    """
    pairs = {
        '(': ')', '（': '）', '「': '」', '『': '』',
        '[': ']', '{': '}', '〈': '〉', '《': '》', '“': '”', '『': '』'
    }
    opens = set(pairs.keys())
    closes = set(pairs.values())
    stack = []
    buf = []
    out = []

    i = 0
    while i < len(text):
        ch = text[i]

        # 括弧の開閉処理
        if ch in opens:
            stack.append(pairs[ch])
            buf.append(ch)
        elif ch in closes:
            # 対応閉じ括弧がスタックにある場合のみpop
            if stack and ch == stack[-1]:
                stack.pop()
            buf.append(ch)
        else:
            # 括弧外なら区切りを判定
            if not stack and ch in seps:
                out.append(''.join(buf))
                buf = []
            else:
                buf.append(ch)
        i += 1

    if buf:
        out.append(''.join(buf))
    return out


def parse_staff(staff_str: str):
    """
    '役職:担当者' の繰り返しをパースして (役職, 担当者) のタプル列を返す。
    - トップレベルは '／' を括弧外のみで分割
    - 役職側は '・' を括弧外のみで分割
    - 担当者側は '・' および '、'（必要なら '，' や半角 ',' も）を括弧外のみで分割
    - 前後の空白を除去
    """
    if not staff_str:
        return []

    # 1) セクション分割（括弧外の "／"）
    sections = split_outside(staff_str, ('／',))

    results = []
    for sec in sections:
        if ':' not in sec:
            # まれに「製作:○○委員会」の後に説明だけのセクションが来るケースを無視
            continue

        role_part, name_part = sec.split(':', 1)

        # 2) 役職分割（括弧外の "・"）
        roles = [r.strip() for r in split_outside(role_part, ('・',)) if r.strip()]

        # 3) 担当者分割（括弧外の "・" と "、" と必要なら "，" ","）
        names = [n.strip() for n in split_outside(name_part, ('・', '、', '，', ',')) if n.strip()]

        # 4) 組み合わせ展開
        for r in roles:
            for n in names:
                results.append((r, n))

    return results

staff = "原作:原 ゆたか（「かいけつゾロリのだ・だ・だ・だいぼうけん！」）／監督・シリーズ構成:望月智充／音楽:小西香葉・近藤由紀夫／アニメーション制作:サンライズ、亜細亜堂"

for role, name in parse_staff(staff):
    print(role, ":", name)