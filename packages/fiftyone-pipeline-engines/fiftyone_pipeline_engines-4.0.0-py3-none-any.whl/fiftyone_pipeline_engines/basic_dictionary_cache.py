from fiftyone_pipeline_engines.datakeyed_cache import DataKeyedCache

class BasicDictionaryCache(DataKeyedCache):
    
    def __init__(self):

        self.cache = {}

    def get_cache_value(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            return None

    def set_cache_value(self, key, value):
        self.cache[key] = value
