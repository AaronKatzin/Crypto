import twint, os, csv
import nest_asyncio
from datetime import date, timedelta,datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd


def gettweets(fromdate, todate, keywords):
    """
        gettweets(fromdate, todate, keywords)

        Farms and collects tweets from and to a specific date that contain specific hashtags/keywords

        arguments:
        fromdate: the lower date bound that we want to collect our data from
        todate: the upper date bound that we want to collect our data from
        keywords: specific hashtags/keywords that the tweet must include for it to be saved

        :returns saves the tweets in csv files
        """
    c = twint.Config()
    #specific data we want to save alongside with our tweet
    c.Custom["tweet"] = ["date", "time", "username", "tweet", "language", "replies_count", "retweets_count",
                         "likes_count", "hashtags", "cashtags"]
    c.Search = keywords
    nest_asyncio.apply()
    c.Store_csv = True
    c.Since = fromdate
    c.Until = todate
    c.Hide_output = True
    current_dir = os.path.dirname(os.path.realpath(__file__))
    #the file is named neatly to represent the dates of the tweets it includes and the keywords that were searched for
    c.Output = (current_dir + "\\Data\\" + fromdate + "-" + todate + keywords + ".csv")
    twint.run.Search(c)


def getWeeksOfTweets(endYear, endMonth, endDay, weeksToGet, keywords):
    """
            getWeeksOfTweets(endYear, endMonth, endDay, weeksToGet, keywords)

            uses gettweets to farm a specific amount of weeks worth of tweets

            arguments:
            endYear: the upper year bound that we want to collect our data from
            endMonth: the upper month bound that we want to collect our data from
            endDay: the upper day bound that we want to collect our data from
            weeksToGet: amount of weeks worth of tweets we want to farm
            keywords: specific hashtags/keywords that the tweet must include for it to be saved
            """
    end = date(endYear, endMonth, endDay)
    for i in range(weeksToGet):
        start = end - timedelta(days=7)
        gettweets(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), keywords)
        end -= timedelta(days=7)


def crawlSandP():
    """
                crawlSandP()

                crawls the SPAVG data from https://stooq.com (https://stooq.com/q/d/?s=%5Espx&c=0 specifically)

                arguments:
                none

                :returns saves the crawled data in a csv file
                """

    baseURL = "https://stooq.com/q/d/?s=%5Espx&c=0"
    #the time period we wanted to crawl our data from
    fromDate = "20200619"
    toDate = "20210619"
    url = baseURL + "&d1=" + fromDate + "&d2=" + toDate
    #initializing arrays we want to save our wanted data in
    date = []
    dailyAvg = []
    for page in range(1, 7):
        soup = getSoup(url + "&l=" + str(page))
        print("here " + url + "&l=" + str(page))
        table = soup("table", attrs={"class": "fth1"})[0]
        first = True
        for row in table("tr"):
            #The first row doesn't interest us so we're skipping it using the boolean "first"
            if first:
                first = False
            else:
                #crawling and appending the data we're interested in into arrays
                cells = row("td")
                date_object = datetime.strptime(cells[1].get_text(), "%d %b %Y")
                date.append(date_object.strftime("%Y-%m-%d"))
                print("Date: " + date_object.strftime("%Y-%m-%d"))
                dailyAvg.append((float(cells[3].get_text()) + float(cells[4].get_text()))/2)
                print("daily avg: ", ((float(cells[3].get_text()) + float(cells[4].get_text()))/2))
    #saving the data we crawled into a csv file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    outputFile = open(current_dir + "\\data\\" + fromDate + "_" + toDate + "_" + "S&P_Daily_avg.csv", 'w', newline='')
    writer = csv.writer(outputFile)

    writer.writerow(["date", "SPAvg"])
    for row in range(len(date)):
        writer.writerow([date[row], dailyAvg[row]])
    outputFile.close()







def getSoup(url):
    """
                    getSoup(url)

                    creates and returns the soup object

                    arguments:
                    URL that we want to turn into the soup object

                    :returns returns a soup object corresponding to the given URL
                    """
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=user_agent)
    return BeautifulSoup(response.content, "html.parser")
