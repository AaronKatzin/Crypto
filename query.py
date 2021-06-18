import twint
import nest_asyncio

def gettweets(fromdate,todate,keywords):
    """This is coded to only work on Razi's pcs for now"""
    """TODO: make the path more abstract"""
    c = twint.Config()
    c.Search = keywords
    nest_asyncio.apply()
    c.Store_csv = True
    c.Since = fromdate
    c.Until = todate
    c.Hide_output = True
    c.Output = ("C:\\Users\\PC\\Desktop\\Project\\Crypto\\Data\\"+fromdate+"-"+todate+keywords+".csv")
    twint.run.Search(c)