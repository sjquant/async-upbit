class APIError(Exception):

    def __init__(self, status_code: int, name: str, message: str):
        self.status_code = status_code
        self.name = name
        self.message = message

    def __str__(self):
        return f"{self.status_code}: {self.name} - {self.message}"


class CreateOrderError(APIError):

    def __init__(self, status_code: int, name: str, message: str):
        super().__init__(status_code, name, message)


class InsufficientFundsError(APIError):

    def __init__(self, status_code: int, name: str, message: str):
        super().__init__(status_code, name, message)


class UnderMinTotalOrderError(APIError):
    def __init__(self, status_code: int, name: str, message: str):
        super().__init__(status_code, name, message)
