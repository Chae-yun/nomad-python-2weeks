import requests
from bs4 import BeautifulSoup

base_url = "https://weworkremotely.com"

def extract_job(html):
  title = html.find("span", {"class": "title"}).string
  company = html.find("span", {"class": "company"}).string
  href = html.find("a", recursive = False)["href"]
  return {
    "title": title,
    "company": company,
    "link": f"{base_url}{href}"
  }

def extract_jobs(url):
  jobs = []
  print("Scrapping We Work Remotely")
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")
  # 간혹 Programming Jobs와 DevOps and Sysadmin Jobs 등 여러 섹션으로 나오는 경우가 있음
  sections = soup.find_all("section", {"class": "jobs"})
  for section in sections:
    results = section.find_all("li")
    for result in results:
      # view-all 제외
      if "view-all" not in result["class"]:
        job = extract_job(result)
        jobs.append(job)
  return jobs

def get_ww_jobs(term):
  term = term.replace(' ', '+')
  url = f"{base_url}/remote-jobs/search?term={term}"
  jobs = extract_jobs(url)
  return jobs