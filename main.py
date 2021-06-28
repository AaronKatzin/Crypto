import pandas as pd
from getters import getHashtags, getStats, getTweetStatsDF, getAllFilesStats, getExtendedStatsDF
from cleaning import cleanDF
from tabulate import tabulate
from predict import predict, predictList

# setting major change percentage
MAJOR_CHANGE = 5

# to get new tweet data, only needs to run once
"""# getWeeksOfTweets(2020,4,16,52, "btc OR bitcoin")"""

# parse raw data to create daily stats files, only needed when there's new data
"""# getAllFilesStats()"""

# load daily stats files into a dataframe
statsDF = getTweetStatsDF()

# load daily coin price file into a dataframe
coinPriceDF = pd.read_csv("data\\BTC-USD.csv")

#crawl S&P for daily average, only needed to be done once
"""crawlSandP()"""

# load daily S&P 500 index file into a dataframe
SPAvgDF = pd.read_csv("data\\20200619_20210619_S&P_Daily_avg.csv")

# join daily stats files dataframe with the coin price and S&P daily avg
df = statsDF.set_index('date').join(coinPriceDF.set_index('date'))
df = df.join(SPAvgDF.set_index('date'))

# print dataframe for debugging
# print(tabulate(df, headers='keys', tablefmt='psql'))

# calculate additional stats columns (e.g. averages) and add them to the dataframe
df = getExtendedStatsDF(df, MAJOR_CHANGE)

# clean the dataframe of missing data, NULLs, etc
df = cleanDF(df)

# print dataframe for debugging
print(tabulate(df, headers='keys', tablefmt='psql'))

# choose features to be used in the ML algorithm
used_features = ['tweet_count', 'replies', 'avg_replies', 'retweets', 'average_retweets', 'likes', 'average_likes',
                 'diamondhands_count', 'investing_count', 'hodl_count', 'hold_count', 'tesla_count', 'sell_count',
                 'buy_count', 'elon_musk_count', 'shorttesla_count', 'referral_count', 'gold_count', 'moon_count',
                 "diamondhands_count_avg", "investing_count_avg", "hodl_count_avg", "hold_count_avg", "tesla_count_avg",
                 "sell_count_avg", "buy_count_avg", "elon_musk_count_avg", "shorttesla_count_avg", "referral_count_avg",
                 "gold_count_avg", "moon_count_avg", "SPAvg"]
used_features_avgs_only = ['tweet_count', 'avg_replies', 'average_retweets', 'average_likes',
                           "diamondhands_count_avg", "investing_count_avg", "hodl_count_avg", "hold_count_avg",
                           "tesla_count_avg",
                           "sell_count_avg", "buy_count_avg", "elon_musk_count_avg", "shorttesla_count_avg",
                           "referral_count_avg",
                           "gold_count_avg", "moon_count_avg"]

# choose categories we would like to predict
category_list = ["increase", "decrease", "major_increase", "major_decrease", "major_change", "increase_tomorrow",
                 "decrease_tomorrow", "major_increase_tomorrow", "major_decrease_tomorrow", "major_change_tomorrow"]

# train and test the model
predictList(df, used_features, category_list)
