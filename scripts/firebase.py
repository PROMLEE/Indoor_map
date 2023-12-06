import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate(
    "scripts\capston-design7-firebase-adminsdk-p4k7t-1579383ce6.json"
)
firebase_admin.initialize_app(cred)


def put_firebase(filename, item):
    db = firestore.client()
    buildingname = filename[:-3]
    floor = filename[-2:]
    docs = db.collection("buildings").stream()
    for doc in docs:
        if doc.to_dict()["BuildingName"] == buildingname:
            return (
                db.collection("buildings")
                .document(doc.id)
                .collection("stores")
                .document(f"{doc.id}_{floor}")
                .set(item)
            )


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
# get("CAU310")
