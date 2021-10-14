import json

import pandas as pd


def three2two(n, i, no):
    tmp_n = n[no]
    del n[no]
    for j in tmp_n:
        n.insert(no, j)
    j = 0
    while len(tmp_n) + j <= i:
        n.insert(len(tmp_n) + j + no, "")
        j += 1
    return n


with open("data.json") as f:
    data = json.load(f)

bunka_max = max(tuple(map(lambda n: len(n[7]), data)))
print("bunka max count:", bunka_max)
data = tuple(map(lambda n: three2two(n, bunka_max, 7), data))

undou_max = max(tuple(map(lambda n: len(n[6]), data)))
print("undou max count:", undou_max)
data = tuple(map(lambda n: three2two(n, undou_max, 6), data))

gakka_max = max(tuple(map(lambda n: len(n[3]), data)))
print("gakka max count:", gakka_max)
data = tuple(map(lambda n: three2two(n, gakka_max, 3), data))
# pprint.pprint(data)

df = pd.DataFrame(data)
df = df.rename(columns=lambda s: str(s), index=lambda s: str(s))
df = df[~df.duplicated()]
df_data = []
for j in ["パソコン部","コンピュータ部","コンピューター部"]:
    for i in range(bunka_max):
        df_data.append(df[df[str(7 + gakka_max + undou_max + i)] == j])

df = pd.concat(df_data)
# df = df[str(7 + gakka_max + undou_max)]
# print(7 + gakka_max + undou_max - 2)
print(df)

df.to_csv("syuturyoku.csv")
