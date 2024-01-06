import httpx

def fetch_http(url: str, timeout: int = 3):
    try:
        return httpx.get(url, timeout=timeout)
    except httpx.ConnectTimeout as err:
        print(f"HTTPX Connection Timeout: {err}")
    except Exception as err:
        print(f"HTTPX Certificate Verification Error: {err}")


def build_url(scheme: str = 'http', host: str = "", port: int = 80, path: str = '/'):
    return f"{scheme}://{host}:{port}{path}"