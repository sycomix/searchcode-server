import requests
import urllib

from .common import get_base_url
from .common import get_blns


def test_search_blns():
    for naughty in get_blns():
        url = f'{get_base_url()}v1/{naughty}'
        r = requests.get(url)

        assert r.status_code in {404, 400}, url
