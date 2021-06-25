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
    """
        normalize(df, column_name)
        Normalizes the data frame to make it visually easier to display and understand in charts

        arguments:
        df:the data frame we want to normalize

        column_name: the column we want to normalize

        :returns a dataframe with an added normalized column to be displayed visually
        """
    #Calculates the normal using the max and the min values
    max_value = df[column_name].max()
    min_value = df[column_name].min()
    #Adds a new column that includes the normalized values
    df[column_name + "_normalized"] = (df[column_name] - min_value) / (max_value - min_value)
    return df


#We've set our major change to be at 5%
MAJOR_CHANGE=5
warnings.filterwarnings("ignore")

#fills a data frame with the tweet stats using getTweetStatsDF
statsDF = getTweetStatsDF()
#fills a data frame with the coin price stats using a csv file that contains them
coinPriceDF = pd.read_csv("data\\BTC-USD.csv")
#fills a data frame with the SPAVG price stats using a csv file that contains them
SPAvgDF = pd.read_csv("data\\20200619_20210619_S&P_Daily_avg.csv")
#syncronizes the way the date column is displayed to avoid errors
statsDF['datetime'] = pd.to_datetime(statsDF['date'],format="%Y-%m-%d", errors='ignore' )
#joins the coinprice and the SPavgDF data frames into one dataframe depending on the date column
df = statsDF.set_index('date').join(coinPriceDF.set_index('date'))
df = df.join(SPAvgDF.set_index('date'))


#adds additional columns to the data frame(e.g. averages)
df = getExtendedStatsDF(df, MAJOR_CHANGE)


#cleans the data frame (removes NULL values and fills in the SPAVG weekend values)
df = cleanDF(df)

#list of columns that we want to normalize for the visualization
toNormalize = ["diamondhands_count_avg","sell_count_avg","tesla_count_avg","SPAvg","gold_count",
               "elon_musk_count_avg","buy_count_avg","hodl_count","elon_musk_count","referral_count_avg","buy_count"]

#normalizing each column
for column in toNormalize:
    normalize(df, column)
normalize(df, "BTCAvg")
#prints the dataframe
print(tabulate(df, headers='keys', tablefmt='psql'))

#normalized columns to visualize
normalized = ["diamondhands_count_avg_normalized","sell_count_avg_normalized","tesla_count_avg_normalized","SPAvg_normalized","gold_count_normalized",
               "elon_musk_count_avg_normalized","buy_count_avg_normalized","hodl_count_normalized","elon_musk_count_normalized","referral_count_avg_normalized","buy_count_normalized"]

#plots the normalized data for us to study
for column in normalized:
    g_results = sns.lineplot(data=df[["datetime",column, "BTCAvg_normalized"]])
    plt.show()