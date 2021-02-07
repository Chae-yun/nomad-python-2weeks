import requests
from bs4 import BeautifulSoup

base_url = "https://stackoverflow.com/jobs"

def get_last_page(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")
  pagination = soup.find("div", {"class": "s-pagination"})
  if not pagination:
    return 1
  pages = pagination.find_all("a")
  last_page = pages[-2].get_text(strip = True)
  return int(last_page)

def extract_job(html):
  title = html.find("h2", {"class": "mb4"}).find("a")["title"]
  company = html.find("h3", {"class": "mb4"}).find("span", {"class": ""}).get_text(strip = True)
  job_id = html["data-jobid"]
  return {
    "title": title,
    "company": company,
    "link": f"{base_url}/{job_id}"
  }

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping StackOverFlow: Page {page}")
    r = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("div", {"class": "listResults"}).find_all("div", recursive = False)
    for result in results:
      try:
        # jobid가 없으면 익셉션
        if result["data-jobid"]:
          job = extract_job(result)
          jobs.append(job)
      except:
        # 결과가 적은 경우에 나오는 'You might be interested in these jobs:'부터는 제외
        if result.find("div", {"class": "ml24"}) is not None:
          break
  return jobs

def get_so_jobs(term):
  term = term.replace(' ', '+')
  url = f"{base_url}?r=true&q={term}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs