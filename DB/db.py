import pymongo

client = pymongo.MongoClient("localhost", 27017)

db = client["Doofenshmirtz"]

examService = db["examService"]
category = db["category"]
medicalInstructions = db["medicalInstructions"]
user = db["user"]