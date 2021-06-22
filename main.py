import twint,os
import nest_asyncio
import pandas as pd
from datetime import date, timedelta
from getters import getHashtags, getStats, getTweetStatsDF, getAllFilesStats,getExtendedStatsDF
from cleaning import cleanDF
from query import gettweets
import numpy as np
from tabulate import tabulate
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn import metrics as metrics
import matplotlib.pyplot as plt
from decisionTree import renderTree
import graphviz
from sklearn.ensemble import RandomForestClassifier
from predict import predict,predictList

MAJOR_CHANGE = 5

#only needed when there's new data
#getAllFilesStats()

statsDF = getTweetStatsDF()
coinPriceDF = pd.read_csv("data\\BTC-USD.csv")

df = statsDF.set_index('date').join(coinPriceDF.set_index('date'))

df = getExtendedStatsDF(df, MAJOR_CHANGE)



df = cleanDF(df)


print(tabulate(df, headers='keys', tablefmt='psql'))

used_features = ['tweet_count','replies','avg_replies','retweets','average_retweets','likes','average_likes',
                     'diamondhands_count','investing_count','hodl_count','hold_count','tesla_count','sell_count',
                     'buy_count','elon_musk_count','shorttesla_count','referral_count','gold_count','moon_count',
                     "diamondhands_count_avg","investing_count_avg","hodl_count_avg","hold_count_avg","tesla_count_avg",
                     "sell_count_avg","buy_count_avg","elon_musk_count_avg","shorttesla_count_avg","referral_count_avg",
                     "gold_count_avg","moon_count_avg"]

category_list = ["increase","decrease","major_increase","major_decrease","major_change","increase_tomorrow",
                 "decrease_tomorrow","major_increase_tomorrow","major_decrease_tomorrow","major_change_tomorrow"]
predictList(df, used_features,category_list)
