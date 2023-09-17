import firebase_admin
import socket
import time
import liquidcrystal_i2c
import threading
from firebase_admin import firestore

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return IP

lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
lcd.printline(0, get_ip())
time.sleep(2)
default_app = firebase_admin.initialize_app()
db = firestore.client()

id = "Risha"
doc = db.collection("messages").document(id).get()
callback_done = threading.Event()


def write_to_disp(text):
    lcd.clear()
    line = ''
    lineNo = 0
    for i, word in enumerate(text.split(' ')):
        if len(line)  + len(word) >= 20:
            lcd.printline(lineNo, line.center(20))
            lineNo += 1
            line = ''
        line += word + ' '
    lcd.printline(lineNo, line.center(20))
    print(line)


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        write_to_disp(doc.to_dict()['msg'])
    callback_done.set()

col_query = db.collection("messages").document(id)

query_watch = col_query.on_snapshot(on_snapshot)

while True:
    # time.sleep(1)
    callback_done.wait()
    callback_done.clear()
    print("done")
