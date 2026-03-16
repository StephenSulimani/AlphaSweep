from .harvard import HarvardClient

class MITClient(HarvardClient):
    def __init__(self, url):
        super().__init__(url)
