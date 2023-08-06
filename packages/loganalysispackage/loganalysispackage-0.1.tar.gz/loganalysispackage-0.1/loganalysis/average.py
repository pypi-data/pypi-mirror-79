from datetime import datetime


def getAverage(outputs, timestamps):

    counts = {}
    for i in range (0, 24):
        counts[str(i)] = 0

    for log in outputs:
        counts = getCount(outputs[log], timestamps[log], counts)

    for count in counts:
        counts[count] = counts[count]/len(timestamps)

    return counts

def getCount(logs, timestamp, counts):

    for i in range (0, len(timestamp)):
        timestamp[i] = timestamp[i][:-5]
        timestamp[i] = datetime.strptime(timestamp[i], "%Y-%m-%dT%H:%M:%S")

        if(logs[i]==1):
            counts[str(timestamp[i].hour)] = counts[str(timestamp[i].hour)] + 1

    return counts
