import requests
from bs4 import BeautifulSoup
import re
import json

def fetch_danime_tags(work_id):
    url = f"https://animestore.docomo.ne.jp/animestore/ci_pc?workId={work_id}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    tags = {}

    # 🎯 ジャンル
    genre_section = soup.find('div', class_='work-tag')
    if genre_section:
        tags['ジャンル'] = [a.text.strip() for a in genre_section.find_all('a')]

    # 🎬 スタッフ・原作・制作会社・監督
    staff_section = soup.find('div', class_='staff')
    if staff_section:
        staff_text = staff_section.get_text(separator='\n')
        for line in staff_text.split('\n'):
            line = line.strip()
            if '監督' in line or 'ディレクター' in line:
                tags['監督'] = line
            elif '制作' in line:
                tags['制作会社'] = line
            elif '原作' in line:
                tags['原作会社'] = line


    # 📦 新構造：castContainerからキャスト・スタッフ・製作年を抽出
    cast_container = soup.find('div', class_='castContainer')
    if cast_container:
        for p in cast_container.find_all('p'):
            text = p.get_text()
            if '[キャスト]' in text:
                cast_line = text.split('[キャスト]')[1].strip()
                tags['キャスト'] = cast_line.replace('\n', '').replace('出演:', '').strip()
            elif '[スタッフ]' in text:
                tags['スタッフ詳細'] = text.split('[スタッフ]')[1].strip()
            elif '[製作年]' in text:
                year_match = re.search(r'\d{4}', text)
                if year_match:
                    tags['製作年'] = f"{year_match.group(0)}年"

    # 💰 optionIconContainerから画質・レンタル
    option_section = soup.find('ul', class_='optionIconContainer')
    if option_section:
        options = [li.text.strip() for li in option_section.find_all('li', class_='optionText')]
        for opt in options:
            if re.match(r'\d{3,4}p', opt):
                tags['画質'] = opt
            elif 'レンタル' in opt:
                tags['レンタル'] = 'あり'
        if 'レンタル' not in tags:
            tags['レンタル'] = 'なし'
    else:
        tags['レンタル'] = 'なし'

    return tags

def save_tags_to_json(work_list, output_file='tags.json'):
    all_data = []
    for entry in work_list:
        work_id = entry['workId']
        print(f"取得中: {entry['title']} (ID: {work_id})")
        try:
            tags = fetch_danime_tags(work_id)
            all_data.append({
                'title': entry['title'],
                'workId': work_id,
                'url': entry['url'],
                'tags': tags
            })
        except Exception as e:
            print(f"取得失敗: {entry['title']} → {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 保存完了: {output_file}")

work_list = [
    {
        'title': 'ンめねこ',
        'url': 'https://animestore.docomo.ne.jp/animestore/ci_pc?workId=27900',
        'workId': '27900'
    }
]
save_tags_to_json(work_list)