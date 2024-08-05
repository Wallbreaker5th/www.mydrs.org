from bs4 import BeautifulSoup
import os
import re

# get all `list-id=xxx.htm` files in the `www.mydrs.org` directory
files = [f for f in os.listdir('./www.mydrs.org') if f.startswith('list-id=') and f.endswith('.htm')]

info = []

# loop through each file and extract the information
for file in files:
    with open(os.path.join('./www.mydrs.org', file), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        idx = file.split('.')[0].split('=')[-1]
        title = "".join(soup.title.string.split('-')[:-1]).strip()
        # find the first <center/>
        date_block = soup.find('center')
        # find the date in the format &nbsp;&nbsp;10/24/2006&nbsp;&nbsp; with re
        date = re.search(r'\d{1,2}/\d{1,2}/\d{4}', date_block.text).group()
        # reformat the date to yyyy-mm-dd
        m, d, y = date.split('/')
        m = f'{int(m):02d}'
        d = f'{int(d):02d}'
        date = f'{y}-{m}-{d}'

        info.append({'idx': idx, 'title': title, 'date': date})

# sort the information by idx
info = sorted(info, key=lambda x: int(x['idx']))

with open("tmp.txt", "w", encoding="utf-8") as f:
    f.write("| 编号 | 标题 | 日期（yyyy-mm-dd） |\n")
    f.write("|---|---|---|\n")
    for item in info:
        f.write(f"| {item['idx']} | {item['title']} | {item['date']} |\n")
    f.write(f"共 {len(info)} 条信息\n")
