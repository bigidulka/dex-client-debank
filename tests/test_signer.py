import json
from dex_client_debank import DeBankClient


def test_signer_generates_debank_headers():
    client = DeBankClient()
    headers = client.sign_headers('/asset/total_net_curve', {'user_addr': '0x0000000000000000000000000000000000000000', 'days': 1})
    assert headers['X-API-Key']
    assert headers['x-api-sign']
    assert headers['x-api-ver'] == 'v2'
    assert json.loads(headers['account'])['user_addr'] is None
