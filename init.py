from dotenv import dotenv_values
import json
import os.path

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

def init():
    if os.path.exists('data.json'):
        print('Already init')
        return 
    
    data = {
            "id": config['ID'],
            "model": config['MODEL'],
            "status": config['STATUS'],
            "target": None,
            "charge": config['charge'],
            "products_ids": []
    }
    with open('data.json', 'w') as f:
        json.dump(data, f)
    
    print('Data was init')