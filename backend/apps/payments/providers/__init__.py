from .cod import CODProvider
from .stripe_provider import StripeProvider
from .tabby import TabbyProvider
from .tamara import TamaraProvider

_PROVIDERS = {p.key: p() for p in (CODProvider, StripeProvider, TamaraProvider, TabbyProvider)}


def get_provider(key: str):
    try:
        return _PROVIDERS[key]
    except KeyError:
        raise ValueError(f"Unknown payment provider: {key!r}")
