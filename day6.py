import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

def input_country(question):
  while(True):
    print(question,"\n")
    try:
      answer = int(input("#: "))
      if answer in range(len(countries)):
        return answer
      else:
        print("Choose a number from the list.\n")
    except:
      print("That wasn't a number.\n")

def input_money(question):
  while(True):
    print(question)
    try:
      answer = float(input())
      return answer
    except:
      print("That wasn't a number.\n")

os.system("clear")
URL_codes = "https://www.iban.com/currency-codes"
URL_convert = "https://transferwise.com/gb/currency-converter/"

r_codes = requests.get(URL_codes)
soup_codes = BeautifulSoup(r_codes.text, "html.parser")
table = soup_codes.find("tbody")
rows = table.find_all("tr")
countries = []
currency_codes = []
answer = ""

for row in rows:
  columns = row.find_all("td")
  if columns[2].string != None:
    countries.append(columns[0].string.capitalize())
    currency_codes.append(columns[2].string)

print("Welcome to CurrencyConvert PRO 2000\n")

for index, country in enumerate(countries):
  print(f"# {index} {country}")
print("\n")

from_country = input_country("Where are you from? Choose a country by number.")
print(countries[from_country], "\n")
from_code = currency_codes[from_country]

to_country = input_country("Now choose another country.")
print(countries[to_country], "\n")
to_code = currency_codes[to_country]

from_money = input_money(f"How many {from_code} do you want to conver to {to_code}?")

r_convert = requests.get(f"{URL_convert}{from_code.lower()}-to-{to_code.lower()}-rate?amount={from_money}")
soup_convert = BeautifulSoup(r_convert.text, "html.parser")
rate = float(soup_convert.find("span", {"class": "text-success"}).string)

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

to_money = format_currency(from_money * rate, to_code, locale='ko_KR')
from_money = format(from_money, ',')
print(f"{from_code}{from_money} is {to_money}")