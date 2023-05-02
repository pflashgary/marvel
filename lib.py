import hashlib
import time
import requests
import logging
import sys

class MarvelService:
    def __init__(self, public_key, private_key, api_prefix = "http://gateway.marvel.com"):

        self.public_key = public_key
        self.private_key = private_key
        self.api_prefix = api_prefix
        self.logger = logging.getLogger(__name__)
        self.limit = 100 # maximum for the marvel api
        self.session = requests.Session()

    def _hash(self, nonce: str, public_key: str, private_key: str):
        # this will be used as the nonce (each request to the marvel API key needs to have a different apikey)
        #ts = str(time.time_ns())
        hash = hashlib.md5(nonce.encode() + private_key.encode() + public_key.encode())
        return hash.hexdigest()

    def _get(self, endpoint, **kwargs):
        # make a nonce, it has to be different for every request
        ts = str(time.time_ns())
        hash = self._hash(ts, self.public_key, self.private_key)
        url = f"{self.api_prefix}{endpoint}"
        params = {
            "ts": ts,
            "apikey": self.public_key,
            "hash": hash,
            "limit": self.limit,
            **kwargs
        }
        self.logger.debug(f"making a request to {url} with {params}")
        response = self.session.get(url, params=params)
        if response.status_code != requests.codes.ok:
            raise Exception(f"unexpected response from server: {response.status_code}, {response.json()}")
        return response.json()

    def _get_paginated(self, endpoint):
        results = []
        offset = 0
        total = sys.maxsize # fake an initial max size until we get the real one from the first API response
        self.logger.debug(f"paging through {endpoint}")

        # find the .data.total, then loop over each page until we're done
        while offset < total:
            body = self._get(endpoint, offset=offset)
            total = body["data"]["total"]
            offset += body["data"]["count"]
            self.logger.debug(f'got {body["data"]["count"]} from offset {offset}')
            results += body["data"]["results"]
        self.logger.debug(f"finished paging, got {len(results)} results")
        return results

    def get_characters(self):
        endpoint = "/v1/public/characters"
        self.logger.info(f"getting characters")
        return self._get_paginated(endpoint)

    def get_comics(self):
        endpoint = "/v1/public/comics"
        self.logger.info(f"getting comics")
        return self._get_paginated(endpoint)
