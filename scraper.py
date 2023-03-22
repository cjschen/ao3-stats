import argparse

from email.mime import base
from fileinput import filename
from time import sleep
from bs4 import BeautifulSoup
import requests
from os import path, mkdir
from datetime import datetime
from constants import FANDOM, BASE_URL, START, END


date = datetime.now().strftime("%Y%m%d")
last_date = datetime.max
target_date = datetime.fromtimestamp(1679371365) # Mar 20

if not path.exists(f"data/html/{FANDOM}/{date}"):
    mkdir(f"data/html/{FANDOM}/{date}")

# target_date = datetime.fromtimestamp(1679198920) # Mar 19
# target_date = datetime.fromtimestamp(1679285320) # Nov 2022
index = 1

while(last_date > target_date):
        
    file_name= f"data/html/{FANDOM}/{date}/{FANDOM}_{index}.html"
    # get initial
    url = f"{BASE_URL}?page={index}"
    resp = requests.get(url)

    if not resp.ok:
        print(f"API error on request to {url} failed")
        print(f"Failed at page: {index}")
        print(resp.text)
        exit(-1)
    soup = BeautifulSoup(resp.content, features="html.parser")
    
    if not len(soup.select("ol .work")):
        print(f"failed to find works on url {index}")
        exit(-1)
    
    
    first_work_date = soup.select(".datetime")[0].string
    first_date = datetime.strptime(first_work_date, "%d %b %Y")
    if first_date < target_date:
        print(f"First work published on {first_work_date}. Skipping download")
        last_date = first_date
        break

    last_work_date = soup.select(".datetime")[-1].string
    last_date = datetime.strptime(last_work_date, "%d %b %Y")

    with open(file_name, "w") as file:
        file.write(resp.text)
    
    print(f"Finished downloading page {index}. Last date: {last_work_date}. Sleeping for 40s")

    sleep(40)
    index += 1