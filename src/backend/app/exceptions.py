class AppError(Exception):
    def __init__(
        self,
        error: str,
        message: str,
        status_code: int,
        details: dict | None = None,
        **extra: str,
    ) -> None:
        self.error = error
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.extra = extra

    def to_dict(self) -> dict:
        body: dict = {
            "error": self.error,
            "message": self.message,
            "details": self.details,
        }
        body.update(self.extra)
        return body
