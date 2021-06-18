import twint
import nest_asyncio
from datetime import date,timedelta

from query import gettweets
print(date(2021,6,13).strftime("%Y-%m-%d"))
end = date(2021,6,18)
for i in range (52):
    start = end - timedelta(days=7)
    gettweets(start.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d"),"btc OR bitcoin")
    end -= timedelta(days=7)




