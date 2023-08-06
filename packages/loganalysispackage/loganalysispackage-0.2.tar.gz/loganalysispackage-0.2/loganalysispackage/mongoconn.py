from pymongo import MongoClient
import configreader as cfgr


def getMongoConn(filePath):

    dataconfig = cfgr.dataconfigread(filePath)
    mongoClient = MongoClient(dataconfig['mongodb']['url'])
    db = mongoClient[dataconfig['mongodb']['database']]
    collection = db[dataconfig['mongodb']['collection']]

    return collection

