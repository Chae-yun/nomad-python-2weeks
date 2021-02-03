import requests
from flask import Flask, render_template, request, redirect

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

@app.route("/")
def index():
  order = request.args.get("order_by")
  if order:
    order.lower()
    if order == "popular":
      url = popular
    elif order == "new":
      url = new
    else:
      return redirect("/")
  else:
    order = "popular"
    url = popular

  existing_news = db.get(order)
  news = []
  if existing_news:
    news = existing_news
  else:
    results = requests.get(url).json()["hits"]
    for result in results:
      news.append({
        "title": result["title"], 
        "url": result["url"], 
        "points": result["points"], 
        "author": result["author"], 
        "num_comments": result["num_comments"], 
        "comments_link": f'/{result["objectID"]}'
      })
    db[order] = news

  return render_template(
    "index.html", 
    order = order.capitalize(),
    news_list = news
  )

@app.route("/<id>")
def detail(id):
  result = requests.get(make_detail_url(id)).json()
  news = {
    "title": result["title"], 
    "url": result["url"], 
    "points": result["points"], 
    "author": result["author"]
  }
  
  comments = []
  for comment in result["children"]:
    comments.append({
      "author": comment["author"], 
      "text": comment["text"]
    })

  return render_template(
    "detail.html", 
    news = news,
    comments = comments
  )

app.run(host="0.0.0.0")