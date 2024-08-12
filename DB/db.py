import pymongo

client = pymongo.MongoClient("localhost", 27017)

db = client["Doofenshmirtz"]

testService = db["testService"]
category = db["category"]
medicalInstructions = db["medicalInstructions"]
user = db["user"]