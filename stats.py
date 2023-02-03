from bs4 import BeautifulSoup 
from constants import FANDOM
import os 
from work import Work 

def process_work(work):
    id = work['id'].split("_")[1]
    rating = ""
    author = work.select("a[rel=author]")[0].string
    kudos = work.select("#kudos > a")[0].string
    
    pass


if __name__ == "__main__":
    # for filename in os.listdir(f"data/html/{FANDOM}"):
    soup = BeautifulSoup(open("/mnt/c/Users/Sijia/workspace/webscraper/data/html/少女☆歌劇 レヴュー・スタァライト | Shoujo Kageki Revue Starlight (Anime)/少女☆歌劇 レヴュー・スタァライト | Shoujo Kageki Revue Starlight (Anime)_1_20221030.html"), features="html.parser")
    works = soup.select("li.work")
    print(Work(works[0]))


# 
