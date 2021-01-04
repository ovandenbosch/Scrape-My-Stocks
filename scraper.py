# When deploying on Raspberry Pi, change file handling mode to w instead of r+ in line 18
import requests
from bs4 import BeautifulSoup
import time
import csv
import sendmail
from datetime import date


urls = ["https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch",
       "https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch",
       "https://finance.yahoo.com/quote/PYPL?p=PYPL&.tsrc=fin-srch",
       "https://finance.yahoo.com/quote/ZM?p=ZM&.tsrc=fin-srch"]
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15"}

today = str(date.today()) + ".csv"
csv_file = open(today, "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Stock Name", "Current Price", "Previous Close", "Open", "Bid", "Ask", "Day's Range", "52 Week Range", "Volume", "Avg. Volume", "Market Cap", "Beta (5Y Monthly)", "PE Ratio (TTM)", "EPS (TTM)", "Earnings Date", "Forward and Dividend & Yield", "Ex-Dividend Date", "1y Target Est"])


for url in urls:
    stock = []
    html_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_page.content, "lxml")

    header_info = soup.find_all("div", id ="quote-header-info")[0]

    stock_title = header_info.find("h1").get_text()
    stock_price = header_info.find("div", class_="My(6px) Pos(r) smartphone_Mt(6px)").find("span").get_text()

    stock.append(stock_title)
    stock.append(stock_price)
# Two table info because there is two parts of the table in in different classes
    table_info1 = soup.find_all("div", class_= "D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)")[0].find_all("tr")
    table_info2 = soup.find_all("div", class_= "D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)")[0].find_all("tr")

    for i in range(0, 8):
        value = table_info1[i].find_all("td")[1].get_text()
        stock.append(value)

    for i in range(0, 8):
        value = table_info2[i].find_all("td")[1].get_text()
        stock.append(value)

    csv_writer.writerow(stock)
    time.sleep(5)

csv_file.close()
#
# # This obtains the function written in sendmail.py
sendmail.send_email(filename=today)
print("Email sent successfully")