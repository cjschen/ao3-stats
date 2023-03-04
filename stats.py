from bs4 import BeautifulSoup 
from work import Work 
from models import recreate_db

if __name__ == "__main__":
    recreate_db()
    # for filename in os.listdir(f"data/html/{FANDOM}"):
    soup = BeautifulSoup(open("/mnt/c/Users/Sijia/workspace/webscraper/data/html/少女☆歌劇 レヴュー・スタァライト | Shoujo Kageki Revue Starlight (Anime)/少女☆歌劇 レヴュー・スタァライト | Shoujo Kageki Revue Starlight (Anime)_1_20221030.html"), features="html.parser")
    works = soup.select("li.work")
    print(Work(works[0]))
    print(Work(works[1]))


# 
