from httpx import Response
from hunthttp.supporthttp import build_url, fetch_http
from hunttcp.hunttcp import PREFIX as PREFIX_TCP


PREFIX = "redirect_http_"


def huntredirect_get_defaults() -> dict:
    return {"80": "http", "443": "https", "8000": "http", "8080": "http",
    "8081": "http", "8088": "http", "8181": "http", "8443": "https", "8888":
    "http"}


def huntredirect_fieldnames() -> list[str]:
    fieldnames = []
    port_list = huntredirect_get_defaults()
    for port, scheme in port_list.items():
        fieldnames.append(f"{PREFIX}{port}")
    return fieldnames


# Returns a list of tuples with url, http status_code, location/None
def analyse_http(url: str):
    r = fetch_http(url, timeout=4)
    if type(r) is not Response:
        return r

    if r.status_code >= 300 and r.status_code < 400:
        # tup = analyse_http(r.headers['Location'])
        return (url, r.status_code, r.headers['Location'])

    return (url, r.status_code, None)


def huntredirect(prey: dict, target: str):
    port_list = huntredirect_get_defaults()

    for port, scheme in port_list.items():
        if f"{PREFIX_TCP}{port}" not in prey:
            continue

        if not prey[f"{PREFIX_TCP}{port}"]:
            prey[f"{PREFIX}{port}"] = f"n/a: no TCP to {port}"
            continue

        # Start scan
        url = build_url(scheme=scheme, host=target, port=port)
        res = analyse_http(url)

        if res is None:
            prey[f"{PREFIX}{port}"] = None
        elif type(res) is str:
            prey[f"{PREFIX}{port}"] = res
        else:
            res_txt = f"url: {res[0]} :: status: {res[1]} -> location: {res[2]}"
            prey[f"{PREFIX}{port}"] = res_txt

    return prey