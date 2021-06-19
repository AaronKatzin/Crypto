import twint,os,csv
from datetime import datetime

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

    outputFile = open(current_dir + "\\" + filename + "_hashtags", 'w', encoding="utf8")
    writer = csv.writer(outputFile)
    writer.writerow(["hashtag", "count"])
    sortedHashtagDict  = sorted(hashtagDict, key=hashtagDict.get)
    for key in sortedHashtagDict:
        writer.writerow([key])
    outputFile.close()

def getStats(filename):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(current_dir + "\\" + filename, encoding="utf8") as csv_file:
        print("Opening file for getStats: " + current_dir + "\\" + filename)
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

                    count = 1
                    replies_count = 0
                    retweets_count = 0
                    likes_count = 0

                    prev_date = date
                    i += 1
    csv_file.close()
    outputFile = open(current_dir + "\\" + filename + "_tweetStats", 'w', encoding="utf8")
    print("Opening file fow writing: " + current_dir + "\\" + filename + "_tweetStats")
    writer = csv.writer(outputFile)
    writer.writerow(["date", "tweet_count", "replies", "avg_replies","retweets","average_retweets","likes","average_likes"])
    for row in range(len(date_arr)):
        writer.writerow([date_arr[row], count_arr[row],replies_count_arr[row],avg_replies_arr[row],
                         retweets_count_arr[row],avg_retweets_arr[row],likes_count_arr[row],avg_likes_arr[row]])
    outputFile.close()