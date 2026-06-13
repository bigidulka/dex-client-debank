# DeBank Reverse Client

Minimal Python client for DeBank web API endpoints. It signs requests with the extracted DeBank browser signer module and exposes portfolio, token, chain, history, user, NFT, and raw signed GET helpers.

## Educational Use

This project is published as part of an educational process for studying web/API clients and data access patterns. It is unofficial, not affiliated with or endorsed by the upstream service, and should be used responsibly according to the target site's terms and applicable law.


## Install

```bash
pip install git+https://github.com/bigidulka/dex-client-debank.git
```

Node.js must be available in `PATH`; the Python client calls the bundled signer helper to generate DeBank `x-api-sign` headers.

## Quick start

```python
from dex_client_debank import DeBankClient

wallet = "0x3ec68709334f64ee4927891627f0b395c6ff6754"
client = DeBankClient()
print(client.wallet_balance_usd(wallet))
print(client.used_chains(wallet))
print(client.token_cache_balance_list(wallet))
print(client.history_list(wallet, page_count=5))
```

## Methods

- `raw_get`
- `chain_list`
- `total_net_curve`
- `wallet_balance_usd`
- `asset_classify`
- `asset_history_init`
- `asset_history_status`
- `used_chains`
- `user`
- `user_banner`
- `user_config`
- `user_received_vip_list`
- `user_total_balance`
- `user_effective_usd_value`
- `user_history_usd_values`
- `user_badge_count`
- `user_badge_list`
- `token_cache_balance_list`
- `token_balance_list`
- `token_list`
- `token_history_list`
- `token_history_price_dict`
- `history_list`
- `all_history`
- `history_token_search`
- `portfolio_app_list`
- `portfolio_project_list`
- `portfolio_all_token_list`
- `portfolio_list`
- `portfolio_project_ids`
- `wallet_snapshot`
- `nft_list`
- `web3_id_gift`
- `bundle_history_list`
- `bundle_history_asset_init`
- `bundle_history_asset_status`

## Browser-harness verified live endpoints

- `GET /asset/total_net_curve` params: `user_addr, days`
- `GET /chain/list` params: ``
- `GET /history/list` params: `user_addr, chain, start_time, page_count`
- `GET /portfolio/app_list` params: `user_id`
- `GET /portfolio/project_list` params: `user_addr`
- `GET /token/balance_list` params: `user_addr, chain`
- `OPTIONS /token/balance_list` params: `user_addr, chain`
- `GET /token/cache_balance_list` params: `user_addr`
- `GET /user` params: `id`
- `GET /user/banner` params: `id`
- `GET /user/config` params: `id`
- `GET /user/received_vip_list` params: `id`
- `GET /user/used_chains` params: `id`
- `GET /web3_id_gift` params: `receiver_id`

## Hidden path inventory

Browser-harness loaded the DeBank profile/history/portfolio pages and the fetched JS bundles were scanned for API paths. Full list is in [`endpoint_inventory.json`](endpoint_inventory.json). Use `raw_get(path, **params)` for paths without a dedicated convenience method.

## Notes

- No official SDK is used.
- Only read endpoints are wrapped as convenience methods.
- Some extracted JS paths are auth/session or write endpoints; those are listed but not wrapped.
- Do not commit wallet cookies or private credentials.
