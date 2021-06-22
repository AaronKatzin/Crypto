import twint,os,csv
import pandas as pd
from datetime import datetime
import numpy as np

def getExtendedStatsDF(df, MAJOR_CHANGE):
    df['diamondhands_count_avg'] = df['diamondhands_count'] / df['tweet_count']
    df['investing_count_avg'] = df['investing_count'] / df['tweet_count']
    df['hodl_count_avg'] = df['hodl_count'] / df['tweet_count']
    df['hold_count_avg'] = df['hold_count'] / df['tweet_count']
    df['tesla_count_avg'] = df['tesla_count'] / df['tweet_count']
    df['sell_count_avg'] = df['sell_count'] / df['tweet_count']
    df['buy_count_avg'] = df['buy_count'] / df['tweet_count']
    df['elon_musk_count_avg'] = df['elon_musk_count'] / df['tweet_count']
    df['shorttesla_count_avg'] = df['shorttesla_count'] / df['tweet_count']
    df['referral_count_avg'] = df['referral_count'] / df['tweet_count']
    df['gold_count_avg'] = df['gold_count'] / df['tweet_count']
    df['moon_count_avg'] = df['moon_count'] / df['tweet_count']

    df['increase_open'] = np.where(df['Open'].shift(1) < df['Open'], 1, 0)
    df['percent_change'] = (df['Open'] - df['Open'].shift(1)) / df['Open'] * 100
    df['increase'] = np.where(df['percent_change'] > 0, 1, 0)
    df['decrease'] = np.where(df['percent_change'] < 0, 1, 0)
    df['major_increase'] = np.where(df['percent_change'] > MAJOR_CHANGE, 1, 0)
    df['major_decrease'] = np.where(df['percent_change'] < - MAJOR_CHANGE, 1, 0)
    df['major_change'] = np.where(df['percent_change'] > MAJOR_CHANGE, 1, 0) + np.where(
        df['percent_change'] < - MAJOR_CHANGE, 1, 0)

    df['percent_change_tomorrow'] = df['percent_change'].shift(-1)
    df['increase_tomorrow'] = df['increase'].shift(-1)
    df['decrease_tomorrow'] = df['decrease'].shift(-1)
    df['major_increase_tomorrow'] = df['major_increase'].shift(-1)
    df['major_decrease_tomorrow'] = df['major_decrease'].shift(-1)
    df['major_change_tomorrow'] = df['major_change'].shift(-1)

    return df

def getTweetStatsDF():

    directory = os.path.dirname(os.path.realpath(__file__)) + "\\data"
    df = pd.DataFrame()
    for entry in os.scandir(directory):
        if entry.path.endswith(".csv_tweetStats") and entry.is_file():
            df = df.append(pd.read_csv(entry.path))
    return df


def getFollowers(username):
    """"TODO: add error handling in case username doesn't exist"""
    c = twint.Config()
    c.Username = username
    c.Store_object= True
    c.Hide_output = True
    c.Format = "ID {id} | Username {username} | Followers {followers}"
    twint.run.Lookup(c)
    return twint.output.users_list[0].followers

def getHashtags(filename):
    """get all hastags in a given file for exploratory purposes"""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    hashtagDict = {}
    with open(current_dir + "\\" + filename, encoding="utf8") as csv_file:
        print("Opening file for hashtags: " + current_dir + "\\" + filename)
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True

        for line in csv_reader:
            if first:
                header = line
                first = False
            else:
                hashtags = line[8]
                hashtagsList = hashtags.split("\', ")
                for hashtag in hashtagsList:
                    strippedHashtag = hashtag.strip("[]\'")
                    #increment counter for that hashtag
                    hashtagDict[strippedHashtag] = hashtagDict.get(strippedHashtag, 0) + 1
    csv_file.close()

    outputFile = open(current_dir + "\\" + filename + "_hashtags", 'w', encoding="utf8", newline='')
    writer = csv.writer(outputFile)
    writer.writerow(["hashtag", "count"])
    #sortedHashtagDict  = sorted(hashtagDict, key=hashtagDict.get)
    for key,value in hashtagDict.items():
        writer.writerow([key,value])
    outputFile.close()

def getAllFilesStats():
    directory = os.path.dirname(os.path.realpath(__file__)) + "\\data"
    for entry in os.scandir(directory):
        if entry.path.endswith("OR bitcoin.csv") and entry.is_file():
            getStats(entry.path)


def getStats(filename):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(filename, encoding="utf8") as csv_file:
        print("Opening file for getStats: " + filename)
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True
        second = False

        count = 1
        replies_count = 0
        i = 0
        retweets_count = 0
        likes_count = 0
        date_arr= []
        count_arr = []
        replies_count_arr = []
        avg_replies_arr = []
        retweets_count_arr = []
        avg_retweets_arr = []
        likes_count_arr = []
        avg_likes_arr = []

        #hastag counters and arrays
        investing_count=0
        hodl_count=0
        hold_count=0
        tesla_count=0
        sell_count=0
        buy_count=0
        elon_musk_count=0
        shorttesla_count=0
        referral_count=0
        gold_count=0
        moon_count=0
        diamondhands_count=0

        investing_count_arr = []
        hodl_count_arr = []
        hold_count_arr = []
        tesla_count_arr = []
        sell_count_arr = []
        buy_count_arr = []
        elon_musk_count_arr = []
        shorttesla_count_arr = []
        referral_count_arr = []
        gold_count_arr = []
        moon_count_arr = []
        diamondhands_count_arr = []

        for line in csv_reader:

            if first:
                header = line
                first = False
                second = True

            else:
                if second:
                    prev_date = datetime.date(datetime.strptime(line[0], "%Y-%m-%d"))
                    second = False


                date = datetime.date(datetime.strptime(line[0],"%Y-%m-%d"))
                #print(date)
                count += 1
                replies_count += int(line[5])
                retweets_count += int(line[6])
                likes_count += int(line[7])
                hashtags = line[8]

                hashtagsList = hashtags.split("\', ")
                for hashtag in hashtagsList:
                    strippedHashtag = hashtag.strip("[]\'")
                    if strippedHashtag == "investing":
                        investing_count += 1
                    elif strippedHashtag == "hodl":
                        hodl_count += 1
                    elif strippedHashtag == "hold":
                        hold_count += 1
                    elif strippedHashtag == "tesla":
                        tesla_count += 1
                    elif strippedHashtag == "sell":
                        sell_count += 1
                    elif strippedHashtag == "buy":
                        buy_count += 1
                    elif strippedHashtag == "elon_musk":
                        elon_musk_count += 1
                    elif strippedHashtag == "shorttesla":
                        shorttesla_count += 1
                    elif strippedHashtag == "referral":
                        referral_count += 1
                    elif strippedHashtag == "gold":
                        gold_count += 1
                    elif strippedHashtag == "moon":
                        moon_count += 1
                    elif strippedHashtag == "diamondhands":
                        diamondhands_count += 1

                if prev_date > date:

                    #new day identified

                    date_arr.append(date)
                    count_arr.append(count)
                    replies_count_arr.append(replies_count)
                    avg_replies_arr.append(replies_count / count)
                    retweets_count_arr.append(retweets_count)
                    avg_retweets_arr.append(retweets_count/ count)
                    likes_count_arr.append(likes_count)
                    avg_likes_arr.append(likes_count/ count)

                    investing_count_arr.append(investing_count)
                    hodl_count_arr.append(hodl_count)
                    hold_count_arr.append(hold_count)
                    tesla_count_arr.append(tesla_count)
                    sell_count_arr.append(sell_count)
                    buy_count_arr.append(buy_count)
                    elon_musk_count_arr.append(elon_musk_count)
                    shorttesla_count_arr.append(shorttesla_count)
                    referral_count_arr.append(referral_count)
                    gold_count_arr.append(gold_count)
                    moon_count_arr.append(moon_count)
                    diamondhands_count_arr.append(diamondhands_count)

                    count = 1
                    replies_count = 0
                    retweets_count = 0
                    likes_count = 0
                    investing_count = 0
                    hodl_count = 0
                    hold_count = 0
                    tesla_count = 0
                    sell_count = 0
                    buy_count = 0
                    elon_musk_count = 0
                    shorttesla_count = 0
                    referral_count = 0
                    gold_count = 0
                    moon_count = 0
                    diamondhands_count=0

                    prev_date = date
                    i += 1

        #deal with last (partial) day bug:https://github.com/AaronKatzin/Crypto/issues/2
        date_arr.append(date)
        count_arr.append(count)
        replies_count_arr.append(replies_count)
        avg_replies_arr.append(replies_count / count)
        retweets_count_arr.append(retweets_count)
        avg_retweets_arr.append(retweets_count / count)
        likes_count_arr.append(likes_count)
        avg_likes_arr.append(likes_count / count)

        investing_count_arr.append(investing_count)
        hodl_count_arr.append(hodl_count)
        hold_count_arr.append(hold_count)
        tesla_count_arr.append(tesla_count)
        sell_count_arr.append(sell_count)
        buy_count_arr.append(buy_count)
        elon_musk_count_arr.append(elon_musk_count)
        shorttesla_count_arr.append(shorttesla_count)
        referral_count_arr.append(referral_count)
        gold_count_arr.append(gold_count)
        moon_count_arr.append(moon_count)
        diamondhands_count_arr.append(diamondhands_count)

    csv_file.close()
    outputFile = open(filename + "_tweetStats", 'w', encoding="utf8", newline='')
    print("Opening file fow writing: " + filename + "_tweetStats")
    writer = csv.writer(outputFile)
    writer.writerow(["date", "tweet_count", "replies", "avg_replies","retweets","average_retweets","likes",
                     "average_likes", "diamondhands_count","investing_count","hodl_count","hold_count","tesla_count",
                     "sell_count","buy_count","elon_musk_count","shorttesla_count","referral_count","gold_count",
                     "moon_count"])


    for row in range(len(date_arr)):
        writer.writerow([date_arr[row], count_arr[row],replies_count_arr[row],avg_replies_arr[row],
                         retweets_count_arr[row],avg_retweets_arr[row],likes_count_arr[row],avg_likes_arr[row],
                         diamondhands_count_arr[row],investing_count_arr[row],hodl_count_arr[row],hold_count_arr[row]
                            ,tesla_count_arr[row],sell_count_arr[row],buy_count_arr[row],elon_musk_count_arr[row]
                            ,shorttesla_count_arr[row],referral_count_arr[row],gold_count_arr[row],moon_count_arr[row]])
    outputFile.close()