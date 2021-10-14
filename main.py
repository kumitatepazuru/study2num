import bs4
import requests

# ===== study高校受験の部活絞り込みページから学校を取得する =====
res = requests.get('https://www.studyh.jp/kanto/special/club/cultural/club.html?c=computer')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
elems = soup.select("#club_boy .club-list .clubl_name a")
school_list = list(map(lambda n: n.text, elems))
# elems = soup.select("#club_boy .club-list .clubl_name a")
# school_list += list(map(lambda n: n.text, elems))
elems = soup.select("#club_mix .club-list .clubl_name a")
school_list += list(map(lambda n: n.text, elems))

# ===== みんなの高校情報から、最新の首都圏高偏差値一覧を取得する =====
res = requests.get('https://www.minkou.jp/hischool/exam/shutoken/deviation/')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
elems = soup.select("#main > div:nth-child(7) > div > .mod-table1.mod-table1__exam")
data = {}
for elem in elems:
    for i, j in enumerate(elem.select("tr")):
        if i != 0:
            for k in j.select("li a"):
                data[k.text] = int(j.select_one(".tx-ac.tx-wb").text)
            # data.append({int(j.select_one(".tx-ac.tx-wb").text): list(map(lambda n: n.text, j.select("li a")))})

print(data)
d = ""
for i in school_list:
    l_in = [s for s in data.keys() if i.split("県立")[-1].split("都立")[-1] in s]
    if len(l_in) == 0:
        print("警告：みんなの高校情報に検索中の学校名が存在しませんでいた。高校名:" + i)
        continue
    elif len(l_in) != 1:
        print("警告：みんなの高校情報に検索中の学校名が一致するものが複数ありました。どちらにするか指定してください。もとの学校名:"+i)
        print("\n".join(list(map(lambda n: str(n[0] + 1) + " " + n[1], list(enumerate(l_in))))))
        name = l_in[int(input("> "))-1]
    else:
        name = l_in[0]
    d += str(data[name])+","+name+"\n"

with open("data.csv","w") as f:
    f.write(d)
