import hashlib
import uuid
from typing import Any, cast
from urllib.parse import unquote, urlencode

import httpx
import jwt

from .errors import APIError, CreateOrderError, UnderMinTotalOrderError
from .types import (
    Account,
    Market,
    Order,
    OrderBy,
    OrderChance,
    OrderInList,
    OrderSide,
    OrderState,
    OrderType,
    PlaceOrderResponse,
    TickerSnapshot,
)

UPBIT_API_URL = "https://api.upbit.com"


class Client:
    def __init__(self, access_key: str = "", secret_key: str = ""):
        self._access_key = access_key
        self._secret_key = secret_key

    async def get_accounts(self) -> list[Account]:
        """내가 보유한 자산 리스트를 보여줍니다."""
        return cast(list[Account], await self._get_for_exchange("v1/accounts"))

    async def get_order_chance(self, market: str):
        """마켓별 주문 가능 정보를 확인합니다.

        Args:
            market: 마켓 ID (ex. KRW-BTC)
        """
        return cast(
            OrderChance,
            await self._get_for_exchange("v1/orders/chance", {"market": market}),
        )

    #
    async def get_order(self, uuid: str | None = None, identifier: str | None = None):
        """개별 주문 조회

        Args:
            uuid: 주문의 UUID
            identifier: 조회용 사용자 지정 값
        """
        params: dict[str, str] = {}
        if uuid:
            params["uuid"] = uuid
        if identifier:
            params["identifier"] = identifier

        return cast(
            Order,
            await self._get_for_exchange("v1/order", params),
        )

    async def get_orders(
        self,
        *,
        market: str | None = None,
        uuids: list[str] | None = None,
        identifiers: list[str] | None = None,
        state: OrderState | None = None,
        states: list[OrderState] | None = None,
        page: int = 1,
        limit: int = 100,
        order_by: OrderBy = "desc",
    ):
        """주문 리스트 조회

        Args:
            market: Market ID
            uuids: 주문 UUID의 목록
            identifiers: 주문 identifier의 목록
            state: 주문 상태
            states: 주문 상태의 목록 (* 미체결 주문(wait, watch)과 완료 주문(done, cancel)은 혼합하여 조회하실 수 없음)
            page: 요청 페이지
            limit: 요청 개수
            order_by: 정렬
        """

        params: dict[str, Any] = {
            "page": page,
            "limit": limit,
            "order_by": order_by,
        }

        if market:
            params["market"] = market
        if uuids:
            params["uuids[]"] = uuids
        if identifiers:
            params["identifiers"] = identifiers
        if state:
            params["state"] = state
        if states:
            params["states[]"] = states

        return cast(
            list[OrderInList],
            await self._get_for_exchange("v1/orders", params),
        )

    async def place_order(
        self,
        *,
        market: str,
        side: OrderSide,
        ord_type: OrderType,
        volume: str | None = None,
        price: str | None = None,
        identifier: str | None = None,
    ):  # -> Any:
        """주문을 요청합니다.

        Args:
            market: 마켓 ID (ex. KRW-BTC)
            side: 주문 종류 (bid : 매수, ask : 매도)
            volume: 주문량
            price: 주문 가격
            ord_type: 주문 타입 (limit : 지정가 주문, price : 매수 시장가 주문, market : 매도 시장가 주문)
            identifier: 조회용 사용자 지정 값 (선택)
        """
        params = {
            "market": market,
            "side": side,
            "ord_type": ord_type,
        }

        if volume:
            params["volume"] = volume

        if price:
            params["price"] = price

        if identifier:
            params["identifier"] = identifier

        return cast(
            PlaceOrderResponse,
            await self._exchange_post("v1/orders", params),
        )

    def _headers_for_exchange(self, query_params: dict[str, Any] = {}):
        if query_params:
            query_string = unquote(urlencode(query_params, doseq=True)).encode("utf-8")
            m = hashlib.sha512()
            m.update(query_string)
            query_hash = m.hexdigest()
            payload = {
                "access_key": self._access_key,
                "nonce": str(uuid.uuid4()),
                "query_hash": query_hash,
                "query_hash_alg": "SHA512",
            }
        else:
            payload = {
                "access_key": self._access_key,
                "nonce": str(uuid.uuid4()),
            }

        jwt_token = jwt.encode(payload, self._secret_key)  # type: ignore

        return {"Authorization": f"Bearer {jwt_token}"}

    async def _get_for_exchange(
        self,
        path: str,
        params: dict[str, Any] = {},
    ):
        client = httpx.AsyncClient()
        headers = self._headers_for_exchange(params)
        response = await client.get(
            f"{UPBIT_API_URL}/{path}", headers=headers, params=params
        )

        raise_for_status(response)

        return response.json()

    async def _exchange_post(self, path: str, data: dict[str, Any]):
        client = httpx.AsyncClient()
        headers = self._headers_for_exchange(data)
        response = await client.post(
            f"{UPBIT_API_URL}/{path}", headers=headers, json=data
        )

        raise_for_status(response)

        return response.json()

    async def get_markets(self, is_details: bool = False):
        """마켓 코드 조회

        Args:
            is_details: 유의종목 필드과 같은 상세 정보 노출 여부
        """

        return cast(
            list[Market],
            await self._get_for_quotation("/v1/market/all", {"isDetails": is_details}),
        )

    async def get_ticker_snapshots(self, markets: list[str]):
        """요청 당시 종목들의 스냅샷을 반환한다.

        Args:
            markets: 마켓 코드 목록 (ex. KRW-BTC)
        """
        return cast(
            list[TickerSnapshot],
            await self._get_for_quotation("/v1/ticker", {"markets": markets}),
        )

    async def _get_for_quotation(self, path: str, params: dict[str, Any] = {}):
        client = httpx.AsyncClient()
        headers = {
            "Accept": "application/json",
        }
        response = await client.get(
            f"{UPBIT_API_URL}/{path}", headers=headers, params=params
        )

        raise_for_status(response)

        return response.json()


def raise_for_status(response: httpx.Response):
    """상태코드가 200이 아니면 예외를 발생시킵니다.

    [참고] https://docs.upbit.com/docs/api-%EC%A3%BC%EC%9A%94-%EC%97%90%EB%9F%AC-%EC%BD%94%EB%93%9C-%EB%AA%A9%EB%A1%9D
    """
    if response.status_code != 200:
        try:
            data = response.json()

            error_name = data["error"]["name"]
            error_message = data["error"]["message"]

            if error_name in ["create_ask_error", "create_bid_error"]:
                raise CreateOrderError(
                    response.status_code,
                    error_name,
                    error_message,
                ) from None
            elif error_name in ("insufficient_funds_ask", "insufficient_funds_bid"):
                raise UnderMinTotalOrderError(
                    response.status_code,
                    error_name,
                    error_message,
                ) from None
            elif error_name in ("under_min_total_ask", "under_min_total_bid"):
                raise UnderMinTotalOrderError(
                    response.status_code,
                    error_name,
                    error_message,
                ) from None
            else:
                raise APIError(
                    response.status_code,
                    data["error"]["name"],
                    data["error"]["message"],
                ) from None
        except APIError:
            raise
        except Exception:
            response.raise_for_status()
