import json

name_emb = {'a': '1111', 'b': '2222', 'c': '3333', 'd': '4444'}

emb_filename = '/Users/luweiping/PycharmProjects/emb_json.json'

jsObj = json.dumps(name_emb)

with open(emb_filename, "w") as f:
    f.write(jsObj)
    f.close()