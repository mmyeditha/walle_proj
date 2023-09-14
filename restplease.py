import firebase_admin
import time
import liquidcrystal_i2c
import threading
from firebase_admin import firestore

lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
default_app = firebase_admin.initialize_app()
db = firestore.client()

id = "Risha"
doc = db.collection("messages").document("Merwie").get()

callback_done = threading.Event()

def write_to_disp(text):
    line = ''
    lineNo = 0
    for i, char in enumerate(text):
        if i % 20 == 0:
            lcd.printline(lineNo, line)
            lineNo += 1
            line = ''
        line += char
    lineNo += 1
    lcd.printline(lineNo, line)
    print(line)


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        print(doc.to_dict())
    callback_done.set()

col_query = db.collection("messages").document("Merwie")

query_watch = col_query.on_snapshot(on_snapshot)

while True:
    # time.sleep(1)
    callback_done.wait()
    callback_done.clear()
    print("done")
