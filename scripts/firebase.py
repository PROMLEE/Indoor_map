import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import timeit

cred = credentials.Certificate(
    "scripts\capston-design7-firebase-adminsdk-p4k7t-1579383ce6.json"
)
firebase_admin.initialize_app(cred)

db = firestore.client()
collectionname = "buildings"
floor = "B6"


def set(item):
    docs = db.collection("buildings").stream()
    for doc in docs:
        print(doc.id, doc.to_dict())

    return (
        db.collection(collectionname)
        .document("42485677")
        .collection("stores")
        .document(f"42485677_{floor}")
        .set(item)
    )


def get(buildingname):
    docs = db.collection("buildings").stream()
    for doc in docs:
        if doc.to_dict()["BuildingName"] == buildingname:
            print(doc.id)


# f = open(f"result\CAU310\data\CAU310_{floor}.json")
# data = json.load(f)
# f.close()
# dict = {}
# for item in data:
#     # print(item)
#     if item["id"] in [-2, 1]:
#         continue
#     dict[str(item["id"])] = item["caption"]
# print(dict)
# set(dict)
print(get("CAU310"))
