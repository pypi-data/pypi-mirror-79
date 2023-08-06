from . import mongoconn as mc, elasticsearchconn
from elasticsearchconn import getlogs


def classify(client, filePath):

    alllogs = getlogs(client, filePath)
    allinput = {}
    alloutput = {}
    alltimestamp = {}

    collection = mc.getMongoConn(filePath)
    log_details = collection.find({'client': client}, {'_id': 0})
    log_details = list(log_details)
    keywords = log_details[0]['keywords'].split(',')

    for logs in alllogs:
        input = []
        timestamp = []
        for i in range (0, len(alllogs[logs])):
            val = 0
            for word in keywords:
                if word.lower() in alllogs[logs][i]['message'].lower():
                    val = 1
            input.append(val)
            timestamp.append(alllogs[logs][i]['timestamp'])
        allinput[logs] = input
        alltimestamp[logs] = timestamp

    for logs in allinput:
        output = []
        for i in range (0, len(allinput[logs])):
            if allinput[logs][i] == 1:
                output.append(1)
            else:
                output.append(0)
        alloutput[logs] = output

    return allinput, alloutput, alltimestamp