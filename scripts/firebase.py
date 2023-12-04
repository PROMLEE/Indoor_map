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


class UploadJsonFileToFirestore:
    def __init__(self) -> None:
        self.start = timeit.default_timer()
        self.json_data = "result\CAU310\data\CAU310_02.json"

    @property
    def json_data(self):
        return self._json_data

    @json_data.setter
    def json_data(self, val):
        if val:
            try:
                f = open(
                    self.json_data,
                )
                data = json.load(f)
                f.close()
                self._json_data = data
            except Exception as e:
                print(f"FILE EXCEPTION: {str(e)}")
        else:
            print(f"Wrong file path {val}")

    def upload(self):
        dict = {}

    def add(self, item):
        return (
            db.collection(self.collectionname)
            .document("42485677")
            .collection("stores")
            .add(item)
        )


collectionname = "buildings"


floor = "B6"


def set(item):
    return (
        db.collection(collectionname)
        .document("42485677")
        .collection("stores")
        .document(f"42485677_{floor}")
        .set(item)
    )


f = open(f"result\CAU310\data\CAU310_{floor}.json")
data = json.load(f)
f.close()
dict = {}
for item in data:
    # print(item)
    if item["id"] in [-2, 1]:
        continue
    dict[str(item["id"])] = item["caption"]
print(dict)
set(dict)
