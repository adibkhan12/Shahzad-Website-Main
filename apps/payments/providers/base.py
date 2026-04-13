from dataclasses import dataclass


@dataclass
class PaymentStart:
    redirect_url: str | None
    provider_ref: str = ""


class PaymentProvider:
    key: str = ""

    def start(self, order, request) -> PaymentStart:
        """Called after order is created. Returns redirect URL or None (immediate success)."""
        raise NotImplementedError

    def verify(self, order, request) -> bool:
        """Called on return from provider. Returns True if truly paid."""
        raise NotImplementedError
