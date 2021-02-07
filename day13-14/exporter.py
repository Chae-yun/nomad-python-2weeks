import csv

def export_to_csv(term, jobs):
  file = open(f"{term}.csv", mode = "w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  file.close()
  return 