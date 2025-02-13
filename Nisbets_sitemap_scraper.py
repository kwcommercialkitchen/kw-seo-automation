import requests
import xml.etree.ElementTree as ET
import time
import pandas as pd

# 模拟登录 Nisbets 获取 Session
login_url = "https://www.nisbets.com.au/login"
sitemap_url = "https://www.nisbets.com.au/au_sitemapindex.xml"

# 登录信息
payload = {
    "j_username": "admin@kwonline.com.au",  # 你的用户名
    "j_password": "12345qwert",  # 你的密码
}

# 模拟登录并获取 session
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"
}
response = session.post(login_url, data=payload, headers=headers)

if response.status_code != 200:
    print(f"登录失败！状态码：{response.status_code}")
    exit()

print("登录成功，开始抓取 sitemap...")

# 抓取 sitemap 内容
response = session.get(sitemap_url, headers=headers)
if response.status_code != 200:
    print(f"请求失败！状态码：{response.status_code}")
    exit()

# 解析 sitemap XML
sitemaps = []
root = ET.fromstring(response.content)
for sitemap in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap"):
    loc = sitemap.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
    if "product" in loc:
        sitemaps.append(loc)

print(f"共找到 {len(sitemaps)} 个产品子 sitemap。")

# 抓取产品 URL 并保存到 CSV
all_product_urls = []
for sitemap in sitemaps:
    print(f"正在抓取 {sitemap}...")
    response = session.get(sitemap, headers=headers)
    if response.status_code != 200:
        print(f"子 sitemap 请求失败！状态码：{response.status_code}")
        continue
    root = ET.fromstring(response.content)
    for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
        all_product_urls.append(loc)
    time.sleep(1)  # 防止请求过于频繁

# 保存产品链接到 CSV
df = pd.DataFrame(all_product_urls, columns=["Product URL"])
df.to_csv("nisbets_product_urls.csv", index=False)
print("产品链接已保存到 nisbets_product_urls.csv")
