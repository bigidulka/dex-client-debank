from __future__ import annotations

from typing import Any

from .core import Json, SignedHTTPClient, drop_empty


class DeBankClient(SignedHTTPClient):
    def raw_get(self, path: str, **params: Any) -> Json:
        return self.get(path, params=drop_empty(params))

    def chain_list(self) -> Json:
        return self.raw_get("/chain/list")

    def total_net_curve(self, user_addr: str, days: int = 1) -> Json:
        return self.raw_get("/asset/total_net_curve", user_addr=user_addr, days=days)

    def wallet_balance_usd(self, user_addr: str, days: int = 1) -> float:
        payload = self.total_net_curve(user_addr, days=days)
        points = ((payload.get("data") or {}).get("usd_value_list") or [])
        if not points:
            return 0.0
        return float(points[-1][1])

    def asset_classify(self, user_addr: str) -> Json:
        return self.raw_get("/asset/classify", user_addr=user_addr)

    def asset_history_init(self, user_addr: str) -> Json:
        return self.raw_get("/asset/history_init", user_addr=user_addr)

    def asset_history_status(self, user_addr: str) -> Json:
        return self.raw_get("/asset/history_status", user_addr=user_addr)

    def used_chains(self, wallet: str) -> Json:
        return self.raw_get("/user/used_chains", id=wallet)

    def user(self, wallet: str) -> Json:
        return self.raw_get("/user", id=wallet)

    def user_banner(self, wallet: str) -> Json:
        return self.raw_get("/user/banner", id=wallet)

    def user_config(self, wallet: str) -> Json:
        return self.raw_get("/user/config", id=wallet)

    def user_received_vip_list(self, wallet: str) -> Json:
        return self.raw_get("/user/received_vip_list", id=wallet)

    def user_total_balance(self, wallet: str) -> Json:
        return self.raw_get("/user/total_balance", id=wallet)

    def user_effective_usd_value(self, wallet: str) -> Json:
        return self.raw_get("/user/effective_usd_value", id=wallet)

    def user_history_usd_values(self, wallet: str) -> Json:
        return self.raw_get("/user/history_usd_values", id=wallet)

    def user_badge_count(self, wallet: str) -> Json:
        return self.raw_get("/user/badge_count", id=wallet)

    def user_badge_list(self, wallet: str) -> Json:
        return self.raw_get("/user/badge_list", id=wallet)

    def token_cache_balance_list(self, user_addr: str) -> Json:
        return self.raw_get("/token/cache_balance_list", user_addr=user_addr)

    def token_balance_list(self, user_addr: str, chain: str) -> Json:
        return self.raw_get("/token/balance_list", user_addr=user_addr, chain=chain)

    def token_list(self, user_addr: str, chain: str | None = None) -> Json:
        return self.raw_get("/token/list", user_addr=user_addr, chain=chain)

    def token_history_list(self, user_addr: str, token_id: str | None = None, chain: str | None = None) -> Json:
        return self.raw_get("/token/history_list", user_addr=user_addr, token_id=token_id, chain=chain)

    def token_history_price_dict(self, token_ids: str, chain: str | None = None) -> Json:
        return self.raw_get("/token/history_price_dict", token_ids=token_ids, chain=chain)

    def history_list(self, user_addr: str, chain: str = "", start_time: int = 0, page_count: int = 20) -> Json:
        return self.raw_get("/history/list", user_addr=user_addr, chain=chain, start_time=start_time, page_count=page_count)

    def all_history(self, user_addr: str, chain: str = "", page_count: int = 20, max_pages: int = 50) -> Json:
        pages = []
        seen = set()
        start_time = 0
        merged: dict[str, Any] = {"history_list": []}
        for _ in range(max_pages):
            page = self.history_list(user_addr, chain=chain, start_time=start_time, page_count=page_count)
            data = page.get("data") or {}
            items = data.get("history_list") or []
            if not items:
                break
            pages.append(data)
            for key in ("cate_dict", "cex_dict", "memo_dict", "project_dict", "token_dict"):
                merged.setdefault(key, {}).update(data.get(key) or {})
            for item in items:
                item_key = f"{item.get('id')}:{item.get('idx')}"
                if item_key not in seen:
                    seen.add(item_key)
                    merged["history_list"].append(item)
            if len(items) < page_count:
                break
            last_time = items[-1].get("time_at")
            if not last_time or last_time == start_time:
                break
            start_time = int(last_time)
        return {"data": merged, "pages": len(pages)}

    def history_token_search(self, user_addr: str, q: str) -> Json:
        return self.raw_get("/history/token_search", user_addr=user_addr, q=q)

    def portfolio_app_list(self, user_id: str) -> Json:
        return self.raw_get("/portfolio/app_list", user_id=user_id)

    def portfolio_project_list(self, user_addr: str) -> Json:
        return self.raw_get("/portfolio/project_list", user_addr=user_addr)

    def portfolio_all_token_list(self, user_addr: str) -> Json:
        return self.raw_get("/portfolio/all_token_list", user_addr=user_addr)

    def portfolio_list(self, user_addr: str) -> Json:
        return self.raw_get("/portfolio/list", user_addr=user_addr)

    def portfolio_project_ids(self, user_addr: str) -> Json:
        return self.raw_get("/portfolio/project_ids", user_addr=user_addr)

    def wallet_snapshot(self, user_addr: str, page_count: int = 20) -> Json:
        return {
            "address": user_addr,
            "balance_usd": self.wallet_balance_usd(user_addr),
            "used_chains": self.used_chains(user_addr).get("data", {}).get("chains", []),
            "tokens": self.token_cache_balance_list(user_addr).get("data", []),
            "apps": self.portfolio_app_list(user_addr).get("data", {}),
            "projects": self.portfolio_project_list(user_addr).get("data", []),
            "history": self.history_list(user_addr, page_count=page_count).get("data", {}),
        }

    def nft_list(self, user_addr: str, chain: str | None = None) -> Json:
        return self.raw_get("/nft/list", user_addr=user_addr, chain=chain)

    def web3_id_gift(self, receiver_id: str) -> Json:
        return self.raw_get("/web3_id_gift", receiver_id=receiver_id)

    def bundle_history_list(self, user_addr: str, start_time: int = 0, page_count: int = 20) -> Json:
        return self.raw_get("/bundle/history_list", user_addr=user_addr, start_time=start_time, page_count=page_count)

    def bundle_history_asset_init(self, user_addr: str) -> Json:
        return self.raw_get("/bundle/history_asset_init", user_addr=user_addr)

    def bundle_history_asset_status(self, user_addr: str) -> Json:
        return self.raw_get("/bundle/history_asset_status", user_addr=user_addr)
