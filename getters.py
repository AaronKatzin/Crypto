import twint, os, csv
import pandas as pd
from datetime import datetime
import numpy as np


def getExtendedStatsDF(df, MAJOR_CHANGE):
    """
    getExtendedStatsDF(df, MAJOR_CHANGE)

    calculates additional statistics

    arguments:
    df: a pandas dataframe
    MAJOR_CHANGE: a number representing the percent change considered to be major

    :returns a dataframe which includes additional columns (e.g. averages)
    """
    # calculate averages
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
    df['BTCAvg'] = (df['Open'] + df['Close']) / 2

    # calculate changes (major, minor, etc)
    df['increase_open'] = np.where(df['Open'].shift(1) < df['Open'], 1, 0)
    df['percent_change'] = (df['Open'] - df['Open'].shift(1)) / df['Open'] * 100
    df['increase'] = np.where(df['percent_change'] > 0, 1, 0)
    df['decrease'] = np.where(df['percent_change'] < 0, 1, 0)
    df['major_increase'] = np.where(df['percent_change'] > MAJOR_CHANGE, 1, 0)
    df['major_decrease'] = np.where(df['percent_change'] < - MAJOR_CHANGE, 1, 0)
    df['major_change'] = np.where(df['percent_change'] > MAJOR_CHANGE, 1, 0) + np.where(
        df['percent_change'] < - MAJOR_CHANGE, 1, 0)

    # calculate changes for next day (major, minor, etc)
    df['percent_change_tomorrow'] = df['percent_change'].shift(-1)
    df['increase_tomorrow'] = df['increase'].shift(-1)
    df['decrease_tomorrow'] = df['decrease'].shift(-1)
    df['major_increase_tomorrow'] = df['major_increase'].shift(-1)
    df['major_decrease_tomorrow'] = df['major_decrease'].shift(-1)
    df['major_change_tomorrow'] = df['major_change'].shift(-1)

    # return the updated dataframe
    return df


def getTweetStatsDF():
    """
    getTweetStatsDF()
    reads all the tweetstats files and returns a single dataframe with their contents

    arguments:
    none

    :returns a dataframe which includes all the daily tweet stats
    """

    # location of the tweets stats files
    directory = os.path.dirname(os.path.realpath(__file__)) + "\\data"
    # empty dataframe
    df = pd.DataFrame()
    # loop over files in the directory
    for entry in os.scandir(directory):
        # if the file is a tweet stats file
        if entry.path.endswith(".csv_tweetStats") and entry.is_file():
            # append to the dataframe
            df = df.append(pd.read_csv(entry.path))
    return df


def getFollowers(username):
    """
    getFollowers(username)
    helper function that gets the number of followers a given twitter user has

    arguments:
    username

    :returns the number of followers the user has
    """
    c = twint.Config()
    c.Username = username
    c.Store_object = True
    c.Hide_output = True
    c.Format = "ID {id} | Username {username} | Followers {followers}"
    twint.run.Lookup(c)
    return twint.output.users_list[0].followers


def getHashtags(filename):
    """
    getHashtags(filename)
    gets all hashtags in a given file and the number of times they appeared for exploratory purposes

    arguments:
    filename

    :returns nothing. A CSV file is written with the results
    """
    # set current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # empty dictionary
    hashtagDict = {}
    #open file for reading
    with open(current_dir + "\\" + filename, encoding="utf8") as csv_file:
        # for debug/logging purposes
        print("Opening file for hashtags: " + current_dir + "\\" + filename)
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True
        # iterate over the file
        for line in csv_reader:
            # deal with header row
            if first:
                header = line
                first = False
            else:
                # get list of hashtags for each tweet
                hashtags = line[8]
                hashtagsList = hashtags.split("\', ")
                # iterate of the hashtags of the specific tweet
                for hashtag in hashtagsList:
                    # get the hashtag
                    strippedHashtag = hashtag.strip("[]\'")
                    # increment counter for that hashtag
                    hashtagDict[strippedHashtag] = hashtagDict.get(strippedHashtag, 0) + 1
    csv_file.close()

    # write output into _hashtags file
    outputFile = open(current_dir + "\\" + filename + "_hashtags", 'w', encoding="utf8", newline='')
    writer = csv.writer(outputFile)
    # write header
    writer.writerow(["hashtag", "count"])
    # sortedHashtagDict  = sorted(hashtagDict, key=hashtagDict.get)
    # iterate over dictionary
    for key, value in hashtagDict.items():
        # write each hashtag and number of times it appeared
        writer.writerow([key, value])
    outputFile.close()


def getAllFilesStats():
    """
    getAllFilesStats()
    # parses raw tweet data to create daily stats files

    arguments: none

    :returns nothing. A CSV file is written with the results
    """
    # set current directory
    directory = os.path.dirname(os.path.realpath(__file__)) + "\\data"
    # iterate over files in the directory
    for entry in os.scandir(directory):
        # if it's a tweet stats file
        if entry.path.endswith("OR bitcoin.csv") and entry.is_file():
            # call single file helper function
            getStats(entry.path)


def getStats(filename):

    """
    getAllFilesStats()
    # a helper function that parses raw tweet data to create a daily stats file

    arguments:
    filename

    :returns nothing. A CSV file is written with the results
    """
    # open raw tweets files for parsing
    with open(filename, encoding="utf8") as csv_file:
        # for debug/logging purposes
        print("Opening file for getStats: " + filename)
        csv_reader = csv.reader(csv_file, delimiter=',')
        first = True
        second = False

        # initialize stats counters and arrays
        count = 1
        replies_count = 0
        i = 0
        retweets_count = 0
        likes_count = 0

        date_arr = []
        count_arr = []
        replies_count_arr = []
        avg_replies_arr = []
        retweets_count_arr = []
        avg_retweets_arr = []
        likes_count_arr = []
        avg_likes_arr = []

        # initialize hashtag counters and arrays
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
        diamondhands_count = 0

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

        # iterate over file
        for line in csv_reader:
            # deal with header
            if first:
                header = line
                first = False
                second = True

            else:
                # deal with second row, needs special handling for because we usually save the prev row's date
                if second:
                    prev_date = datetime.date(datetime.strptime(line[0], "%Y-%m-%d"))
                    second = False

                # deal with all rows
                # get date for calculating end of each day
                date = datetime.date(datetime.strptime(line[0], "%Y-%m-%d"))
                # print(date)

                # add to counters
                count += 1
                replies_count += int(line[5])
                retweets_count += int(line[6])
                likes_count += int(line[7])

                # save hashtags of this tweet
                hashtags = line[8]
                # turn hashtags into list
                hashtagsList = hashtags.split("\', ")

                # deal with hashtags off this tweet
                # iterate over hashtag list
                for hashtag in hashtagsList:
                    # clean hashtag
                    strippedHashtag = hashtag.strip("[]\'")
                    # add to relevant counter
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

                # identify end of day
                if prev_date > date:

                    # capture counters, append their values to the end of relevant arrays
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

                    # zero counters so that they can be used in next day
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
                    diamondhands_count = 0

                    # iterate date
                    prev_date = date
                    i += 1

        # deal with last (partial) day bugfix:https://github.com/AaronKatzin/Crypto/issues/2
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

    # create output file
    outputFile = open(filename + "_tweetStats", 'w', encoding="utf8", newline='')
    # for debug/logging
    print("Opening file fow writing: " + filename + "_tweetStats")
    writer = csv.writer(outputFile)
    # write header
    writer.writerow(["date", "tweet_count", "replies", "avg_replies", "retweets", "average_retweets", "likes",
                     "average_likes", "diamondhands_count", "investing_count", "hodl_count", "hold_count",
                     "tesla_count",
                     "sell_count", "buy_count", "elon_musk_count", "shorttesla_count", "referral_count", "gold_count",
                     "moon_count"])
    # iterate over each day that was captured
    for row in range(len(date_arr)):
        # write that day's counters
        writer.writerow([date_arr[row], count_arr[row], replies_count_arr[row], avg_replies_arr[row],
                         retweets_count_arr[row], avg_retweets_arr[row], likes_count_arr[row], avg_likes_arr[row],
                         diamondhands_count_arr[row], investing_count_arr[row], hodl_count_arr[row], hold_count_arr[row]
                            , tesla_count_arr[row], sell_count_arr[row], buy_count_arr[row], elon_musk_count_arr[row]
                            , shorttesla_count_arr[row], referral_count_arr[row], gold_count_arr[row],
                         moon_count_arr[row]])
    outputFile.close()
