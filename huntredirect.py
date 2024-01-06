from httpx import Response
from supporthttp import build_url, fetch_http


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
    port_list = {"80": "http", "443": "https", "8080": "http"}

    for port, scheme in port_list.items():
        if prey[f"port_{port}"]:
            url = build_url(scheme=scheme, host=target, port=port)
            res = analyse_http(url)

            if res is None:
                prey[f"redirect_http_{port}"] = None
            elif type(res) is str:
                prey[f"redirect_http_{port}"] = res
            else:
                res_txt = f"url: {res[0]} :: status: {res[1]} -> location: {res[2]}"
                prey[f"redirect_http_{port}"] = res_txt

    return prey