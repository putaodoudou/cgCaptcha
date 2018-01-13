from pymongo import MongoClient

def openConnection():
    client = MongoClient('localhost', 27017)
    db = client.captcha
    collection = db.image
    return collection

def addImageToCollection(collection, origionalImage, matrix, value):
    collection.insert({'img': origionalImage, 'matrix': matrix, 'value': value})

