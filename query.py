import twint, os, csv
import nest_asyncio
from datetime import date, timedelta,datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd


def gettweets(fromdate, todate, keywords):
    c = twint.Config()
    c.Custom["tweet"] = ["date", "time", "username", "tweet", "language", "replies_count", "retweets_count",
                         "likes_count", "hashtags", "cashtags"]
    c.Search = keywords
    nest_asyncio.apply()
    c.Store_csv = True
    c.Since = fromdate
    c.Until = todate
    c.Hide_output = True
    current_dir = os.path.dirname(os.path.realpath(__file__))
    c.Output = (current_dir + "\\Data\\" + fromdate + "-" + todate + keywords + ".csv")
    twint.run.Search(c)


def getWeeksOfTweets(endYear, endMonth, endDay, weeksToGet, keywords):
    end = date(endYear, endMonth, endDay)
    for i in range(weeksToGet):
        start = end - timedelta(days=7)
        gettweets(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), keywords)
        end -= timedelta(days=7)


def crawlSandP():
    baseURL = "https://stooq.com/q/d/?s=%5Espx&c=0"
    fromDate = "20200619"
    toDate = "20210619"
    url = baseURL + "&d1=" + fromDate + "&d2=" + toDate

    date = []
    dailyAvg = []
    for page in range(1, 7):
        soup = getSoup(url + "&l=" + str(page))
        print("here " + url + "&l=" + str(page))
        table = soup("table", attrs={"class": "fth1"})[0]
        first = True
        for row in table("tr"):
            if first:
                first = False
            else:
                cells = row("td")
                date_object = datetime.strptime(cells[1].get_text(), "%d %b %Y")
                date.append(date_object.strftime("%Y-%m-%d"))
                print("Date: " + date_object.strftime("%Y-%m-%d"))
                dailyAvg.append((float(cells[3].get_text()) + float(cells[4].get_text()))/2)
                print("daily avg: ", ((float(cells[3].get_text()) + float(cells[4].get_text()))/2))

    current_dir = os.path.dirname(os.path.realpath(__file__))
    outputFile = open(current_dir + "\\data\\" + fromDate + "_" + toDate + "_" + "S&P_Daily_avg.csv", 'w', newline='')
    writer = csv.writer(outputFile)

    writer.writerow(["date", "SPAvg"])
    for row in range(len(date)):
        writer.writerow([date[row], dailyAvg[row]])
    outputFile.close()







def getSoup(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=user_agent)
    return BeautifulSoup(response.content, "html.parser")
