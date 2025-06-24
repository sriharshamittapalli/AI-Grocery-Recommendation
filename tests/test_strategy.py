import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Provide a minimal stub for the requests package so agents.py can be imported
import types as _types
requests_stub = _types.ModuleType('requests')
def _dummy_get(*args, **kwargs):
    class _Resp:
        def json(self):
            return {}
    return _Resp()
requests_stub.get = _dummy_get
sys.modules.setdefault('requests', requests_stub)

import urllib.parse
import agents


def test_create_maps_url_format():
    location = {"lat": 12.34, "lng": 56.78}
    stores = [{"address": "123 Main St"}]
    url = agents.create_Maps_url(location, stores)
    origin = f"{location['lat']},{location['lng']}"
    # Expect pattern https://www.google.com/maps/dir/<origin>/<addr1>/<origin>
    encoded_addr = urllib.parse.quote(stores[0]["address"])
    expected = f"https://www.google.com/maps/dir/{origin}/{encoded_addr}/{origin}"
    assert url == expected
