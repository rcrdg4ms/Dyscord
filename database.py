import json


class _localdb:
    def get(self, key: str = None):
        if key != None:
            return json.load(open('local.json', 'r'))[key]
        return json.load(open('local.json', 'r'))

    def change(self, key, value):
        db = self.get()
        db[key] = value
        json.dump(db, open('local.json', 'w'), indent=4)

class _db:
    def get(self, num: int = None):
        if num != None:
            return json.load(open('Database.json', 'r'))[num]
        return json.load(open('Database.json', 'r'))
    
db = _db()
localdb = _localdb()
