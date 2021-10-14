import json
from concurrent.futures import ThreadPoolExecutor

import bs4
import requests
from tqdm import tqdm

res = requests.get('https://www.minkou.jp/hischool/exam/shutoken/deviation/')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")
elems = soup.select("td.tx-al a")
print(elems)
# print(list(map(lambda n: n.text, elems)))
print("Done.")


def f(elem):
    url = "https://www.minkou.jp/hischool/school/" + elem.get("href").split("/")[-2]
    r = requests.get(url)
    r.raise_for_status()
    s = bs4.BeautifulSoup(r.text, "lxml")
    school_num = s.select_one("#main > div.mod-school > div.mod-school-inner > div > div.mod-school-top > h1").text
    school_kana = s.select_one(
        "#main > div.mod-school > div.mod-school-inner > div > div.mod-school-top > div.mod-school-caption").text[1:-1]
    hensachi_num = s.select_one(
        "#main > div.mod-school > div.mod-school-inner > div > div.mod-school-bottom > div > p.mod-school-hensa > span").text
    gakka = s.select_one(
        "table.table-binfo tr:nth-child(3) > td").text.split(
        "、")
    HP = s.select_one(
        "table.table-binfo tr:nth-child(5) > td > p > a").get(
        "href")
    location = s.select_one(
        "table.table-binfo tr:nth-child(7) > td > p").text.replace("\n","")
    bukatu_u = s.select_one(
        "table.table-binfo tr:nth-child(12) > td").text.split(
        "、")
    bukatu_b = s.select_one(
        "table.table-binfo tr:nth-child(13) > td").text.split(
        "、")
    return school_num, school_kana, hensachi_num, gakka, HP, location, bukatu_u, bukatu_b


with ThreadPoolExecutor(max_workers=12) as executor:
    data = list(tqdm(executor.map(f, elems), total=len(elems)))
with open("data.json","w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
