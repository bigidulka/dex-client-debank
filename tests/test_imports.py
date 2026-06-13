import inspect
from dex_client_debank import DeBankClient


def test_client_imports_and_methods_present():
    client = DeBankClient()
    assert client is not None
    methods = [name for name, value in inspect.getmembers(DeBankClient, inspect.isfunction) if not name.startswith('_')]
    assert set(['raw_get', 'chain_list', 'total_net_curve', 'wallet_balance_usd', 'asset_classify', 'asset_history_init', 'asset_history_status', 'used_chains', 'user', 'user_banner', 'user_config', 'user_received_vip_list', 'user_total_balance', 'user_effective_usd_value', 'user_history_usd_values', 'user_badge_count', 'user_badge_list', 'token_cache_balance_list', 'token_balance_list', 'token_list', 'token_history_list', 'token_history_price_dict', 'history_list', 'all_history', 'history_token_search', 'portfolio_app_list', 'portfolio_project_list', 'portfolio_all_token_list', 'portfolio_list', 'portfolio_project_ids', 'wallet_snapshot', 'nft_list', 'web3_id_gift', 'bundle_history_list', 'bundle_history_asset_init', 'bundle_history_asset_status']) <= set(methods)
