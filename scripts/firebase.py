import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import timeit
cred = credentials.Certificate('capston-design7-firebase-adminsdk-p4k7t-1579383ce6.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

class UploadJsonFileToFirestore:
    def __init__(self) -> None:
        self.start = timeit.default_timer()
        self.json_data = "CAU310_05.json"
        self.collectionname = "buildings"

    @property
    def json_data(self):
        return self._json_data
    
    @json_data.setter
    def json_data(self, val):
        if val:
            try:
                f = open(self.json_data,)
                data = json.load(f)
                f.close()
                self._json_data = data
            except Exception as e:
                print(f'FILE EXCEPTION: {str(e)}')
        else:
            print(f'Wrong file path {val}')

    def upload(self):
        dict = {}
        for idx, item in enumerate(self.json_data):
            dict[str(item["id"])]=item["caption"]
        self.set(dict)

    def add(self, item):
        return db.collection("buildings").document("76232993").collection("stores").add(item)
    
    def set(self, item):
        return db.collection("buildings").document("42485677").collection("stores").document("42485677_5").set(item)

uploadjson = UploadJsonFileToFirestore()
uploadjson.upload()      