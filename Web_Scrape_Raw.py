import pandas as pd
import os
from bs4 import BeautifulSoup
import requests

os.chdir("C:/Users/USER/Downloads/BlackCoffer")
df = pd.read_excel("Input.xlsx")
print(df)
count = 0
for i in range(df.shape[0]):
    temp = df.iloc[i]
    url = temp["URL"]
    url_id = temp["URL_ID"]
    count = count+1
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    try:
        source = requests.get(url, headers=headers)
        source.raise_for_status()

        soup = BeautifulSoup(source.text, "html.parser")

        article_title = soup.title.text

        paras_list = []
        li_list = []
        paras = soup.find_all("p", class_=False)
        for p in paras:
            a = p.get_text()
            paras_list.append(a)
        print(paras_list,"\n",len(paras))
        paras_li = soup.find_all("li", class_=False)
        for li in paras_li:
            a = li.get_text()
            li_list.append(a)
        print(li_list,"\n",len(li_list))


        file_name = url_id
        file_path = fr'C:/Users/USER/Downloads/BlackCoffer/Text_files/{file_name}.txt'
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(article_title)
            file.write("\n")
            for p in paras:
                text = p.get_text()
                print(text)
                file.write(text)
                file.write("\n")
            for li in li_list:
                file.write(li)
                file.write("\n")

        with open(file_path, 'r', encoding='utf-8') as file:
            text_new = []
            lines = file.readlines()
            for line in lines:
                if line == "Tags\n":
                    break
                elif line == "TAGS\n":
                    break
                elif line == "tags\n":
                    break
                elif line == "What We Think166\n":
                    break
                text_new.append(line)

        file_path2 = fr'C:/Users/USER/Downloads/BlackCoffer/Text_files_new/{file_name}.txt'
        with open(file_path2, 'a', encoding='utf-8') as file:
            for line in text_new:
                file.write(line)
                file.write("\n")


    except requests.exceptions.RequestException as e:
            print(f"Error while accessing {url}: {e}")