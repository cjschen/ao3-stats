import argparse

from email.mime import base
from fileinput import filename
from time import sleep
from bs4 import BeautifulSoup
import requests
from os import path, mkdir
from datetime import datetime
from constants import FANDOM, BASE_URL, START, END

# https://archiveofourown.org/tags/Naruto/works?commit=Sort+and+Filter&page=2&utf8=%E2%9C%93&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D=kudos_count&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=


date = datetime.now().strftime("%Y%m%d")
# FANDOM_page_datedownloaded

if not path.exists(f"data/html/{FANDOM}"):
    mkdir(f"data/html/{FANDOM}")

for i in range(START, END + 1):
    print(f"Downloading page {i} of {END}")
    file_name= f"data/html/{FANDOM}/{FANDOM}_{i}_{date}.html"
    # get initial
    url = f"{BASE_URL}?page={i}"
    resp = requests.get(BASE_URL)

    if not resp.ok:
        print(f"API error on request to {url} failed")
        print(f"Failed at page: {i}")
        print(resp.text)
        exit(-1)

    
    soup = BeautifulSoup(resp.content, features="html.parser")
    if not len(soup.select("ol .work")):
        print(f"failed to find works on url {i}")
        exit(-1)

    with open(file_name, "w") as file:
        file.write(resp.text)
    print(f"Finished downloading page {i} of {END}. Sleeping for 40s")

    sleep(40)