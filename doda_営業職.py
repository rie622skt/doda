import tls_client
from bs4 import BeautifulSoup
import re
import pandas as pd

session = tls_client.Session(
    client_identifier="chrome112",
    random_tls_extension_order=True
)
url = "https://doda.jp/DodaFront/View/JobSearchList/j_oc__01L/-preBtn__3/"
response = session.get(url)

soup = BeautifulSoup(response.text, "html.parser")
ele = soup.find_all("h2", class_="title clrFix")
elems = [element.find("a") for element in ele]

url_list = []
df = pd.DataFrame(columns=["会社名","URL"])
for elem in elems:
    company = elem.get_text()
    url_pd = elem.attrs["href"]
    dict = {"会社名":[company],"URL":[url_pd]}
    df = pd.concat([df,pd.DataFrame(dict,index=[0])], ignore_index=True)

url_part = 1
for url in range(885):
    url = "https://doda.jp/DodaFront/View/JobSearchList/j_oc__01L/-preBtn__3/-page__"
    url_part = url_part + 1
    url = url + str(url_part)
    print(url)
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ele = soup.find_all("h2", class_="title clrFix")
    elems = [element.find("a") for element in ele]
    for elem in elems:
        company = elem.get_text()
        url_pd = elem.attrs["href"]
        dict = {"会社名":[company],"URL":[url_pd]}
        df = pd.concat([df,pd.DataFrame(dict,index=[0])], ignore_index=True)

def func(url_pd):
    url_pd = url_pd.removesuffix("-tab__pr/")
    url_pd = url_pd.removesuffix("-tab__jd/")
    url_pd = url_pd + "-tab__jd/-fm__jobdetail/-mpsc_sid__10/"
    response = session.get(url_pd)
    soup = BeautifulSoup(response.text, "html.parser")
    if None == re.search(r'ご指定の求人情報は掲載が終了', response.text):
        elems = soup.find_all("tr")
        elems = re.sub(r"\s+","",str(elems))
        pattern = re.compile("<li.*/li>")
        atags = re.findall(pattern,str(elems))
        elems_2 = re.sub(pattern,"",str(elems))
        pattern_2 = re.compile("<.*?>")
        atags_2 = re.findall(pattern_2,str(elems_2))
        elems_3 = re.sub(pattern_2,"",str(elems_2))
        print(url_pd)
        return elems_3
    else:
        pass

df["概要"] = df["URL"].apply(func)
df.to_csv('doda,営業職1.csv', index=False)
print(df)
