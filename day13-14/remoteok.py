import requests
from bs4 import BeautifulSoup

base_url = "https://remoteok.io"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def extract_job(html):
  td = html.find("td", {"class": "company_and_position"})
  title = td.find("a").find("a", {"class": "preventLink"}).find("h2").string
  company = td.find("a", {"class": "companyLink"}).find("h3").string
  href = html["data-href"]
  return {
    "title": title,
    "company": company,
    "link": f"{base_url}{href}"
  }

def extract_jobs(url):
  jobs = []
  print("Scrapping Remote OK")
  r = requests.get(url, headers=headers)
  soup = BeautifulSoup(r.text, "html.parser")
  results = soup.find_all("tr", {"class": "job"})
  for result in results:
    # closed된 job 제외
    if "closed" not in result["class"]:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_ro_jobs(term):
  term = term.replace(' ', '-')
  url = f"{base_url}/remote-dev+{term}-jobs"
  jobs = extract_jobs(url)
  return jobs