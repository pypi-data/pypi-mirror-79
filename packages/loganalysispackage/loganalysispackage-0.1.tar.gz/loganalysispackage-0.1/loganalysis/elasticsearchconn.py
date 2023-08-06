from elasticsearch import Elasticsearch
import mongoconn as mc


def getlogs(client, filePath):

    collection = mc.getMongoConn(filePath)
    log_details = collection.find({'client': client}, {'_id': 0})
    log_details = list(log_details)

    es_hosts = log_details[0]['hosts'].split(',')

    es_client = Elasticsearch(hosts=es_hosts)
    all_indices = es_client.indices.get_alias('*')

    indices = []
    alllogs = {}

    for index in all_indices:
        if "logstash" in index:
            indices.append(index)

    for i in range (0, len(indices)):
        logs = []
        data = es_client.search(index=indices[i], body = {
                    'size' : 10000,
                    'query': {
                        'match_all' : {}
                    }
                })

        hits = data['hits']['hits']

        for hit in hits:
            logs.append({'timestamp': hit['_source']['@timestamp'], 'message': hit['_source']['message']})

        alllogs[indices[i]] = logs

    return alllogs