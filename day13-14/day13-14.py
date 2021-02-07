"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from flask import Flask, render_template, request, redirect, send_file
from stackoverflow import get_so_jobs
from wework import get_ww_jobs
from remoteok import get_ro_jobs
from exporter import export_to_csv

app = Flask("DayThirteen")

db = {}

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/search")
def search():
  term = request.args.get("term")
  if term:
    term = term.lower()
    existing_jobs = db.get(term)
    if existing_jobs:
      jobs = existing_jobs
    else:
      jobs = get_so_jobs(term) + get_ww_jobs(term) + get_ro_jobs(term)
      db[term] = jobs
  else:
    return redirect("/")
  return render_template(
    "search.html", 
    resultsNumber = len(jobs), 
    term = term,
    jobs = jobs
  )

@app.route("/export")
def export():
  try:
    term = request.args.get("term")
    if not term:
      raise Exception
    term = term.lower()
    jobs = db.get(term)
    # 리스트가 빈 경우에는 빈 파일을 만들어주어야 함
    if jobs is None:
      raise Exception
    export_to_csv(term, jobs)
    return send_file(
      f"{term}.csv", 
      mimetype = "text/csv", 
      attachment_filename = f"{term}.csv", 
      as_attachment = True
    )
  except:
    return redirect("/")

app.run(host = "0.0.0.0")