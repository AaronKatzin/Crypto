import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import warnings

from datetime import date, timedelta,datetime
from getters import getHashtags, getStats, getTweetStatsDF, getAllFilesStats,getExtendedStatsDF
from cleaning import cleanDF

from tabulate import tabulate
import matplotlib.pyplot as plt

def normalize(df, column_name):

    max_value = df[column_name].max()
    min_value = df[column_name].min()
    df[column_name + "_normalized"] = (df[column_name] - min_value) / (max_value - min_value)
    return df

from predict import predict,predictList

MAJOR_CHANGE=5
warnings.filterwarnings("ignore")

statsDF = getTweetStatsDF()
coinPriceDF = pd.read_csv("data\\BTC-USD.csv")
SPAvgDF = pd.read_csv("data\\20200619_20210619_S&P_Daily_avg.csv")

statsDF['datetime'] = pd.to_datetime(statsDF['date'],format="%Y-%m-%d", errors='ignore' )
df = statsDF.set_index('date').join(coinPriceDF.set_index('date'))
df = df.join(SPAvgDF.set_index('date'))



#print(tabulate(df, headers='keys', tablefmt='psql'))

df = getExtendedStatsDF(df, MAJOR_CHANGE)



df = cleanDF(df)

toNormalize = ["diamondhands_count_avg","sell_count_avg","tesla_count_avg","SPAvg","gold_count",
               "elon_musk_count_avg","buy_count_avg","hodl_count","elon_musk_count","referral_count_avg","buy_count"]

for column in toNormalize:
    normalize(df, column)
normalize(df, "BTCAvg")

print(tabulate(df, headers='keys', tablefmt='psql'))

normalized = ["diamondhands_count_avg_normalized","sell_count_avg_normalized","tesla_count_avg_normalized","SPAvg_normalized","gold_count_normalized",
               "elon_musk_count_avg_normalized","buy_count_avg_normalized","hodl_count_normalized","elon_musk_count_normalized","referral_count_avg_normalized","buy_count_normalized"]
for column in normalized:
    g_results = sns.lineplot(data=df[["datetime",column, "BTCAvg_normalized"]])
    plt.show()