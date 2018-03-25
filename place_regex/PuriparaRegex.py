import re

class PuriparaRegex(object):
    def matching(self, query):
        place = re.search(r".+都(.+?)[市|区]", query)
        if place:
            return place.group(1)
        return ""
