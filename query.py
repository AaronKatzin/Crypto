import twint,os
import nest_asyncio

def gettweets(fromdate,todate,keywords):
    c = twint.Config()
    c.Custom["tweet"] = ["date","time","username","tweet","language","replies_count","retweets_count",
                         "likes_count","hashtags","cashtags"]
    c.Search = keywords
    nest_asyncio.apply()
    c.Store_csv = True
    c.Since = fromdate
    c.Until = todate
    c.Hide_output = True
    current_dir = os.path.dirname(os.path.realpath(__file__))
    c.Output = (current_dir + "\\Data\\"+fromdate+"-"+todate+keywords+".csv")
    twint.run.Search(c)