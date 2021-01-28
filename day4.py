import requests
import os

start_over = "y"

while(start_over == "y"):

  print("Welcome to IsItDown.py!")
  print("Please write a URL or URLs you want to check. (separated by comma)")

  urls = input()
  urls = urls.split(',')

  for url in urls:
    url = url.strip()
    if not "." in url:
      print(f"{url} is not a valid URL.")
    else:
      if not url.startswith("http"):
        url = "http://" + url
      try:
        r = requests.get(url)
        if r.status_code is requests.codes.ok:
          print(f"{url} is up!")
        else:
          print(f"{url} is down!")
      except:
        print(f"{url} is down!")

  while(True):
    start_over = input("Do you want to start over? y/n ")
    if start_over != "y" and start_over != "n":
      print("That's not a valid answer.")
      continue
    else:
      if start_over == "y":
        os.system("clear")
      else:
        print("k. bye!")
      break