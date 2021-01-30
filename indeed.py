import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=qython&limit={LIMIT}"

def get_last_page():
  # 사이트 개편으로 인해 뒤에 더 존재해도 5페이지까지밖에 얻어오지 못함.
  # Because of renewing of site, it gets until 5 pages even it has more.
  r = requests.get(URL)
  soup = BeautifulSoup(r.text, "html.parser")
  pagination = soup.find("div", {"class": "pagination"})
  links = pagination.find_all("a")
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  last_page = pages[-1]
  return last_page

def extract_job(html):
  title = html.find("h2", {"class": "title"}).find("a")["title"]
  company = html.find("span", {"class": "company"})
  company_anchor = company.find("a")
  if company_anchor is not None:
    company = company_anchor.string.strip()
  else:
    company = company.string.strip()
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  return {
    "title": title, 
    "company": company, 
    "location": location, 
    "link": f"{URL}&vjk={job_id}"
  }

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    r = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_indeed_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs