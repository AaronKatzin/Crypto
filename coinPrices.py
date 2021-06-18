import csv, sys, os



current_dir = os.path.dirname(os.path.realpath(__file__))
rawDataFileName = "BTC_USD_2020-06-19_2021-06-18-CoinDesk.csv"
outputFileName = "weeklyCoinAvg.csv"

outputFile = open(current_dir + "\\data\\" + outputFileName, 'w')

with open("data\\" + rawDataFileName) as csv_file:
    print(os.path.dirname(os.path.realpath(__file__)) + "\\data\\" + rawDataFileName)
    csv_reader = csv.reader(csv_file, delimiter=',')
    writer = csv.writer(outputFile)

    first = True
    day = 0
    weeklyTotal = 0
    weekNumber = 1
    for line in csv_reader:
        if first:
            header = line
            writer.writerow(["weekNumber", "weeklyAvg"])
            first = False
        else:
            Date = line[1]
            high = float(line[4])
            low = float(line[5])
            dailyAvg = (high + low) / 2
            weeklyTotal += dailyAvg

            if day == 6: #end of week, calculate weekly avg
                weeklyAvg = weeklyTotal/7
                writer.writerow([weekNumber,weeklyAvg])
                weekNumber+=1
                weeklyTotal = 0

            day = (day + 1) % 7 #increment day

outputFile.close()