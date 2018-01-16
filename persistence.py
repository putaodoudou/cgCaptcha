from pymongo import MongoClient
import time
from numpy import *

def openConnection():
    client = MongoClient('localhost', 27017)
    db = client.captcha
    collection = db.image
    return collection

def addImageToCollection(collection, origionalImage, matrix, value):
    ts = '%d' % time.time()
    collection.insert({'timestamp': ts, 'img': origionalImage, 'matrix': matrix, 'value': value})
    return ts

def querySets(collection):
    result = collection.distinct('value')
    return result

def querySet(collection, key):
    result = []
    for item in collection.find({'value': key}):
        result.append(item['img'])
    return result

def boolToFloat(sValue):
    if sValue == 'True':
        return 1
    else:
        return 0

def allData(collection):
    all = []
    labels = []
    for item in collection.find():
        matrix = item['matrix'].split(',')
        pixMatrix = list(map(boolToFloat, list(matrix)))
        all.append(pixMatrix)
        labels.append(item['value'])
    return all, labels

