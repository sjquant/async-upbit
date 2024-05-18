from typing import Literal

from typing_extensions import NotRequired, TypedDict

"""
==========================
=== Exchange API Types ===
==========================
"""


class Account(TypedDict):
    currency: str  # 화폐를 의미하는 영문 대문자 코드
    balance: str  # 주문가능 금액/수량
    locked: str  # 주문 중 묶여있는 금액/수량
    avg_buy_price: str  # 매수평균가
    avg_buy_price_modified: bool  # 매수평균가 수정 여부
    unit_currency: str  # 평단가 기준 화폐


class OrderChanceOrder(TypedDict):
    currency: str  # 화폐를 의미하는 영문 대문자 코드
    price_unit: str  # 주문금액 단위
    min_total: str  # 최소 매도/매수 금액


OrderSide = Literal[
    "ask",  # 매도
    "bid",  # 매수
]

AskType = Literal[
    "limit",  # 지정가 주문
    "market",  # 시장가 주문 (매도)
]
BidType = Literal[
    "limit",  # 지정가 주문
    "price",  # 시장가 주문 (매수)
]

OrderType = AskType | BidType


class OrderChanceMarket(TypedDict):
    id: str  # 마켓의 유일 키
    name: str  # 마켓 이름
    order_types: list[OrderType]  # 지원 주문 방식 (만료)
    ask_types: list[AskType]  # 매도 주문 지원 방식
    bid_types: list[BidType]  # 매수 주문 지원 방식
    order_sides: list[str]  # 지원 주문 종류
    bid: dict[str, str]  # 매수 시 제약사항
    ask: dict[str, str]  # 매도 시 제약사항
    max_total: str  # 최대 매도/매수 금액
    state: str  # 마켓 운영 상태


class OrderChanceAccount(TypedDict):
    currency: str  # 화폐를 의미하는 영문 대문자 코드
    balance: str  # 주문가능 금액/수량
    locked: str  # 주문 중 묶여있는 금액/수량
    avg_buy_price: str  # 매수평균가
    avg_buy_price_modified: bool  # 매수평균가 수정 여부
    unit_currency: str  # 평단가 기준 화폐


class OrderChance(TypedDict):
    bid_fee: str  # 매수 수수료
    ask_fee: str  # 매도 수수료
    market: OrderChanceMarket
    bid_account: OrderChanceAccount  # 매수 시 사용하는 화폐의 계좌 상태
    ask_account: OrderChanceAccount  # 매도 시 사용하는 화폐의 계좌 상태


class Trade(TypedDict):
    market: str  # 마켓의 유일 키
    uuid: str  # 체결의 고유 아이디
    price: str  # 체결 가격
    volume: str  # 체결 양
    funds: str  # 체결된 총 가격
    side: str  # 체결 종류
    created_at: str  # 체결 시각


OrderState = Literal[
    "wait",  # 체결 대기 (default)
    "watch",  # 예약주문 대기
    "done",  # 전체 체결 완료
    "cancel",  # 주문 취소
]


class Order(TypedDict):
    uuid: str  # 주문의 고유 아이디
    side: OrderSide  # 주문 종류
    ord_type: OrderType  # 주문 방식
    price: str  # 주문 당시 화폐 가격
    state: str  # 주문 상태
    market: str  # 마켓의 유일키
    created_at: str  # 주문 생성 시간
    volume: str  # 사용자가 입력한 주문 양
    remaining_volume: str  # 체결 후 남은 주문 양
    reserved_fee: str  # 수수료로 예약된 비용
    remaining_fee: str  # 남은 수수료
    paid_fee: str  # 사용된 수수료
    locked: str  # 거래에 사용중인 비용
    executed_volume: str  # 체결된 양
    trades_count: int  # 해당 주문에 걸린 체결 수
    trades: list[Trade]  # 체결 내역


class OrderInList(TypedDict):
    uuid: str  # 주문의 고유 아이디
    side: OrderSide  # 주문 종류
    ord_type: OrderType  # 주문 방식
    price: str  # 주문 당시 화폐 가격
    state: str  # 주문 상태
    market: str  # 마켓의 유일키
    created_at: str  # 주문 생성 시간
    volume: str  # 사용자가 입력한 주문 양
    remaining_volume: str  # 체결 후 남은 주문 양
    reserved_fee: str  # 수수료로 예약된 비용
    remaining_fee: str  # 남은 수수료
    paid_fee: str  # 사용된 수수료
    locked: str  # 거래에 사용중인 비용
    executed_volume: str  # 체결된 양
    trades_count: int  # 해당 주문에 걸린 체결 수


class PlaceOrderResponse(TypedDict):
    uuid: str  # 주문의 고유 아이디
    side: OrderSide  # 주문 종류
    ord_type: OrderType  # 주문 방식
    price: str  # 주문 당시 화폐 가격
    state: str  # 주문 상태
    market: str  # 마켓의 유일키
    created_at: str  # 주문 생성 시간
    volume: str  # 사용자가 입력한 주문 양
    remaining_volume: str  # 체결 후 남은 주문 양
    reserved_fee: str  # 수수료로 예약된 비용
    remaining_fee: str  # 남은 수수료
    paid_fee: str  # 사용된 수수료
    locked: str  # 거래에 사용중인 비용
    executed_volume: str  # 체결된 양
    trades_count: int  # 해당 주문에 걸린 체결 수


OrderBy = Literal[
    "asc",  # 오름차순
    "desc",  # 내림차순
]

"""
===========================
=== Quotation API Types ===
===========================
"""


class Market(TypedDict):
    market: str  # 업비트에서 제공중인 시장 정보
    korean_name: str  # 거래 대상 디지털 자산 한글명
    english_name: str  # 거래 대상 디지털 자산 영문명
    market_warning: NotRequired[Literal["NONE", "CAUTION"]]  # 유의 종목 여부


class TickerSnapshot(TypedDict):
    market: str  # 종목 구분 코드
    trade_date: str  # 최근 거래 일자(UTC)
    trade_time: str  # 최근 거래 시각(UTC)
    trade_date_kst: str  # 최근 거래 일자(KST)
    trade_time_kst: str  # 최근 거래 시각(KST)
    trade_timestamp: int  # 최근 거래 일시(UTC)
    opening_price: float  # 시가
    high_price: float  # 고가
    low_price: float  # 저가
    trade_price: float  # 종가(현재가)
    prev_closing_price: float  # 전일 종가(UTC 0시 기준)
    change: Literal["EVEN", "RISE", "FALL"]  # EVEN : 보합, RISE : 상승, FALL : 하락
    change_price: float  # 변화액의 절대값
    change_rate: float  # 변화율의 절대값
    signed_change_price: float  # 부호가 있는 변화액
    signed_change_rate: float  # 부호가 있는 변화율
    trade_volume: float  # 가장 최근 거래량
    acc_trade_price: float  # 누적 거래대금(UTC 0시 기준)
    acc_trade_price_24h: float  # 24시간 누적 거래대금
    acc_trade_volume: float  # 누적 거래량(UTC 0시 기준)
    acc_trade_volume_24h: float  # 24시간 누적 거래량
    highest_52_week_price: float  # 52주 신고가
    highest_52_week_date: str  # 52주 신고가 달성일
    lowest_52_week_price: float  # 52주 신저가
