import json

def to_json(id, model, status, target, port, charge, products):
    dictionary = {
            "id": id,
            "model": model,
            "status_id": status,
            "target_id": target,
            "port": port,
            "charge": charge,
            "products_ids": products
    }
    with open('data.json', 'w') as f:
        json.dump(dictionary, f)
    # в результате получаем строк JSON:

    f = open('data.json',)
    data = json.load(f)
    for i in data:
        print(i +":", data[i])
    
    f.close()
