import os
import pickle

class Cache:
    def __init__(self, path):
        self.path = path
        self.cache = {}
        self.load()

    def load(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, "rb") as cache_file:
            self.cache = pickle.load(cache_file)

    def save(self):
        with open(self.path, "bw+") as cache_file:
            pickle.dump(self.cache, cache_file)

    def delete(self):
        os.remove(self.path)

    def __contains__(self, key):
        return key in self.cache

    def get(self, key):
        return self.cache[key]

    def add(self, key, data):
        self.cache[key] = data
        self.save()
