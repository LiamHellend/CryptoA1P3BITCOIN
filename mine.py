import os
from pathlib import Path
import json
import hashlib
import datetime
import base64
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileModifiedHandler(FileSystemEventHandler):

    def __init__(self, path, file_name, callback):
        self.file_name = file_name
        self.callback = callback

        # set observer to watch for changes in the directory
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=False)
        self.observer.start()
        self.observer.join()

    def on_modified(self, event): 
        # only act on the change that we're looking for
        if not event.is_directory and event.src_path.endswith(self.file_name):
            self.observer.stop() # stop watching
            self.callback() # call callback


def createGenisisBlock():
    file = Path("blockchain.json")
    if (file.is_file() != True or os.stat("blockchain.json").st_size == 0):
        with open("blockchain.json", "w") as file:

            block_data = "first block"

            block = {
            "Index": 0,
            "Data": block_data,
            "Timestamp": datetime.datetime.now().isoformat(),
            "PreviousHash": 0,
            "Hash": hashlib.sha256(block_data.encode('utf-8')).hexdigest(),
            "Nonce": 0
            }

            json.dump(block, file)
            file.write("\n")
            file.close()
            return
    else:
        return
    

def createRegularBlock():

    with open("transactions.json", "r") as transac_file:
        transaction = transac_file.readlines()[-1]
        transaction = json.loads(transaction)
        transac_file.close()

    
    with open("blockchain.json", "r") as block_file:
        previousBlock = block_file.readlines()[-1]
        previousBlock = json.loads(previousBlock)
        print(previousBlock)
        block_file.close()


    with open("blockchain.json", "a") as block_file:

        nonce = 0
        while True:

            block = {
            "Index": previousBlock["Index"]+1,
            "Data": transaction,
            "Timestamp": datetime.datetime.now().isoformat(),
            "PreviousHash": previousBlock["Hash"],
            "Hash": hashlib.sha256(str(transaction).encode('utf-8')).hexdigest(),
            "Nonce": nonce
            }

            block_bytes = json.dumps(block, sort_keys=True).encode()

            block_hash = hashlib.sha256(block_bytes).hexdigest()

            print(block_hash)

            if(block_hash[:4] == "0"*4):
                print("found nonce")
                break
            nonce += 1


        json.dump(block, block_file)
        block_file.write("\n")
        block_file.close()

def callback():
    createRegularBlock()


createGenisisBlock()

while True:
    FileModifiedHandler('.', "transactions.json", callback)