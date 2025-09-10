from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# ChromeDriverのパス
service = Service("C:/Users/0602JP/Desktop/port/d_test/chromedriver.exe")  # または絶対パス指定

# オプション設定（ヘッドレスモードも可能）
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 画面非表示で実行したい場合

# ブラウザ起動
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.google.com")

print("ページタイトル:", driver.title)
driver.quit()