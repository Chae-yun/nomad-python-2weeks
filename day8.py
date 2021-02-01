import os
import csv
import requests
from bs4 import BeautifulSoup

def get_hire_brands(url):
  hire_brands = []
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")
  main_super_brand = soup.find(id = "MainSuperBrand")
  hire_boxes = main_super_brand.find_all("a", {"class": "goodsBox-info"})
  
  for hire_box in hire_boxes:
    hire_brands.append({
      "link": hire_box["href"], 
      "name": hire_box.find("span", {"class": "company"}).string
    })
  return hire_brands

def get_hire_info(url):
  hire_info = []
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")

  jobCount = soup.find("p", {"class": "jobCount"})
  if jobCount is None:
    jobCount = soup.find("p", {"class": "listCount"})

  if jobCount.find("strong").string != "0":
    table = soup.find(id = "NormalInfo").find("tbody")
    rows = table.find_all("tr", {"class": ""})

    for row in rows:
      location_info = row.find("td", {"class": "local first"}).text.strip().replace("\xa0", " ")
      title_info = row.find("span", {"class": "company"}).string.strip()
      time_info = row.find("td", {"class": "data"}).string
      pay_info = row.find("span", {"class": "payIcon"}).string + row.find("span", {"class": "number"}).string
      date_info = row.find("td", {"class": "regDate"}).string
      hire_info.append({
        "location": location_info, 
        "title": title_info, 
        "time": time_info, 
        "pay": pay_info, 
        "date": date_info
      })
  return hire_info

def save_to_file(file_name, hire_info_list):
  file_name = file_name.translate(str.maketrans("\/:*?<>", "       "))
  file = open(f"{file_name}.csv", mode = "w")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])
  for hire_info in hire_info_list:
    writer.writerow(list(hire_info.values()))
  return

os.system("clear")
alba_url = "http://www.alba.co.kr"

hire_brands = get_hire_brands(alba_url)
for hire_brand in hire_brands:
  hire_info_list = get_hire_info(hire_brand["link"])
  save_to_file(hire_brand["name"], hire_info_list)