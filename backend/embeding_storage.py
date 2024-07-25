import json


class EmbeddingStorage:
    def __init__(self, path):
        self.path = path
        self.embeddings = {}
        self.load()

    def load(self):
        try:
            with open(self.path, 'r') as f:
                self.embeddings = json.load(f)
        except:
            pass

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.embeddings, f)

    def get(self, key):
        return self.embeddings.get(key)

    def set(self, key, value):
        self.embeddings[key] = value
        self.save()

    def delete(self, key):
        del self.embeddings[key]
        self.save()
