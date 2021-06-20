import twint,os
import nest_asyncio
import pandas as pd
from datetime import date, timedelta
from getters import getHashtags, getStats, getTweetStatsDF
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
from predict import predict

MAJOR_CHANGE = 5

"""print(date(2021,6,13).strftime("%Y-%m-%d"))
end = date(2021,6,18)
for i in range (52):
    start = end - timedelta(days=7)
    gettweets(start.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d"),"btc OR bitcoin")
    end -= timedelta(days=7)"""

# getHashtags("data\\2021-06-11-2021-06-18btc OR bitcoin.csv")
"""getStats("data\\2021-04-23-2021-04-30btc OR bitcoin.csv")
getStats("data\\2021-04-30-2021-05-07btc OR bitcoin.csv")
getStats("data\\2021-05-07-2021-05-14btc OR bitcoin.csv")
getStats("data\\2021-05-14-2021-05-21btc OR bitcoin.csv")
getStats("data\\2021-05-21-2021-05-28btc OR bitcoin.csv")
getStats("data\\2021-05-28-2021-06-04btc OR bitcoin.csv")
getStats("data\\2021-06-04-2021-06-11btc OR bitcoin.csv")
getStats("data\\2021-06-11-2021-06-18btc OR bitcoin.csv")"""

statsDF = getTweetStatsDF()
coinPriceDF = pd.read_csv("data\\BTC-USD.csv")

df = statsDF.set_index('date').join(coinPriceDF.set_index('date'))

df['increase_open'] = np.where(df['Open'].shift(1) < df['Open'], 1, 0)
df['percent_change'] = (df['Open'] - df['Open'].shift(1)) / df['Open'] * 100
df['major_increase'] = np.where(df['percent_change'] > MAJOR_CHANGE, 1, 0)
df['major_decrease'] = np.where(df['percent_change'] < - MAJOR_CHANGE, 1, 0)
df['major_change'] = np.where(df['percent_change'] > MAJOR_CHANGE, 1, 0) + np.where(df['percent_change'] < - MAJOR_CHANGE, 1, 0)

#print(tabulate(df, headers='keys', tablefmt='psql'))

used_features = ['tweet_count','replies','avg_replies','retweets','average_retweets','likes','average_likes',
                 'diamondhands_count','investing_count','hodl_count','hold_count','tesla_count','sell_count','buy_count',
                 'elon_musk_count','shorttesla_count','referral_count','gold_count','moon_count']

predict(df, used_features, "major_increase")
predict(df, used_features, "major_decrease")
predict(df, used_features, "major_change")

"""
used_features = ['tweet_count','replies','avg_replies','retweets','average_retweets','likes','average_likes',
                 'diamondhands_count','investing_count','hodl_count','hold_count','tesla_count','sell_count','buy_count',
                 'elon_musk_count','shorttesla_count','referral_count','gold_count','moon_count']"""
"""print("Decision tree:")
XTrain, XTest, YTrain, YTest = train_test_split(df[used_features].values, df['major_change'].values, random_state=1, test_size=0.2)
max = 0


decisionTree = DecisionTreeClassifier(max_depth=2, min_samples_split=10)
decisionTree = decisionTree.fit(XTrain, YTrain)

y_pred_train = decisionTree.predict(XTrain)
#print("Split: " + str(split) + ". depth: " + str(depth) + ". Accuracy on training data = ", metrics.accuracy_score(y_true = YTrain, y_pred = y_pred_train))

y_pred  = decisionTree.predict(XTest)
accuracy = metrics.accuracy_score(y_true = YTest, y_pred = y_pred)
print(" Accuracy on test data = ", accuracy)


print("max: " + str(max))

text_representation = export_text(decisionTree)
print(text_representation)

print("\nRandom forest")



forest =  RandomForestClassifier(bootstrap=True, n_estimators=300, random_state=0)

trained_forest = forest.fit(XTrain, YTrain)

y_pred_train = trained_forest.predict(XTrain)
print('Accuracy on training data= ', metrics.accuracy_score(y_true = YTrain, y_pred = y_pred_train))

y_pred = trained_forest.predict(XTest)
print('Accuracy on test data= ', metrics.accuracy_score(y_true = YTest, y_pred = y_pred))
"""
"""print(statsDF.join(coinPriceDF, on = 'date'))"""
