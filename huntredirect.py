from supporthttp import build_url, fetch_http


# Returns a list of tuples with url, http status_code, location/None
def analyse_http(url: str):
    r = fetch_http(url, timeout=4)
    if r is None:
        return None

    if r.status_code >= 300 and r.status_code < 400:
        tup = analyse_http(r.headers['Location'])
        return (url, r.status_code, r.headers['Location'])
    else:
        return (url, r.status_code, None)


def huntredirect(prey: dict, target: str):
    urls = [] # str
    http_results = [] # list of tuple: url, status code, location

    if prey['port_80']:
        url = build_url(scheme='http', host=target, port=80)
        urls.append(url)
    elif prey['port_443']:
        url = build_url(scheme='https', host=target, port=443)
        urls.append(url)

    for url in urls:
        tup = analyse_http(url)
        http_results.append(tup)
        res_txt = f"url: {tup[0]} :: status: {tup[1]} -> location: {tup[2]}"
        print(res_txt)

    prey['redirect'] = res_txt
    return prey