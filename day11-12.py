import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

app = Flask("DayEleven")
base_url = "https://www.reddit.com"

@app.route("/")
def home():
  return render_template("home.html", subreddits = subreddits)

@app.route("/read")
def read():
  posts = []
  selects = list(request.args.keys())

  for select in selects:
    r = requests.get(f"{base_url}/r/{select}/top/?t=month", headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    posts_div = soup.find_all("div", {"class": "_1oQyIsiPHYt6nx7VOmd1sz"})

    for post in posts_div:
      # 광고 제외
      if "promotedlink" in post["class"]:
        continue
      anchor = post.find("a", {"class": "SQnoC3ObvgnGjWt90zD9Z"})
      link = base_url + anchor["href"]
      title = anchor.find("h3").string
      upvotes = post.find("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"})
      upvotes_anim = post.find("span", {"class": "D6SuXeSnAAagG8dKAb4O4"})
      # 추천수 올라가는 애니메이션이 적용된 경우
      if upvotes_anim is not None:
        upvotes = upvotes_anim
      upvotes = upvotes.string
      # 추천수가 1000이 넘어 k로 표시된 경우
      if 'k' in upvotes:
        upvotes = upvotes.replace('k', '')
        upvotes = float(upvotes)*1000
      upvotes = int(upvotes)
      subreddit = "r/" + select

      posts.append({
        "link": link, 
        "title": title, 
        "upvotes": upvotes, 
        "subreddit": subreddit
      })

  # 추천수 내림차순 정렬
  posts.sort(key=lambda x : x["upvotes"], reverse=True)

  return render_template(
    "read.html", 
    selects = selects, 
    posts = posts
  )

app.run(host="0.0.0.0")