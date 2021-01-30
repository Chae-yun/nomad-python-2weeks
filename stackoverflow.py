import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
  r = requests.get(URL)
  soup = BeautifulSoup(r.text, "html.parser")
  pagination = soup.find("div", {"class": "s-pagination"})
  links = pagination.find_all("a")
  pages = []
  for link in links[:-1]:
    print(link.find("span"))
    pages.append(int(link.find("span").string))
  last_page = pages[-1]
  print(last_page)
  return last_page

def get_so_jobs():
  last_page = get_last_page()
  return []