from __future__ import absolute_import

import json
import itertools

from eth_utils import (
    force_bytes,
    force_obj_to_text,
    force_text,
)

from web3.middleware import (
    GethFormattingMiddleware,
)


class BaseProvider(object):
    middleware_classes = None

    def make_request(self, method, params):
        raise NotImplementedError("Providers must implement this method")

    def isConnected(self):
        raise NotImplementedError("Providers must implement this method")

    def get_middleware_classes(self):
        if self.middleware_classes is None:
            return []
        else:
            return self.middleware_classes


class JSONBaseProvider(BaseProvider):
    middleware_classes = [GethFormattingMiddleware]

    def __init__(self):
        self.request_counter = itertools.count()

    def decode_rpc_response(self, response):
        return json.loads(force_text(response))

    def encode_rpc_request(self, method, params):
        return force_bytes(json.dumps(force_obj_to_text({
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": next(self.request_counter),
        })))

    def isConnected(self):
        try:
            response_raw = self.make_request('web3_clientVersion', [])
            response = json.loads(force_text(response_raw))
        except IOError:
            return False
        else:
            assert response['jsonrpc'] == '2.0'
            assert 'error' not in response
            return True
        assert False
