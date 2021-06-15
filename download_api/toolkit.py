from urllib.parse import urlparse
import url_normalize

def parse_defaults(_args: dict, _defaults: dict) -> dict:
    out = _args.copy()

    for k, v in _defaults.items():

        if k not in _args:
            out[k] = v

    return out

def clean_url(_url: str) -> str:
    return url_normalize.url_normalize(urlparse(_url).geturl().strip("/"))

