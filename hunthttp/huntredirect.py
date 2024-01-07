from httpx import Response
from hunthttp.supporthttp import build_url, fetch_http
from hunttcp.hunttcp import PREFIX as PREFIX_TCP


PREFIX = "redirect"


def huntredirect_get_defaults() -> dict:
    return {"80": "http", "443": "https", "8000": "http", "8080": "http",
    "8081": "http", "8088": "http", "8181": "http", "8443": "https", "8888":
    "http"}


def huntredirect_fieldnames() -> list[str]:
    fieldnames = []
    port_list = huntredirect_get_defaults()
    for port, scheme in port_list.items():
        id = gen_field_id(scheme, port)
        fieldnames.append(id)
    return fieldnames


def gen_field_id(scheme:str, port:int) -> str:
    return f"{PREFIX}_{scheme}_{port}"


# Returns a tuple:
# 0. True (on successful HTTP interaction)
# 1. scheme
# 2. hostname
# 3. port
# 4. url
# 5. http status code
# 6. location, when redirected
# 7. error string
def analyse_http(scheme: str, hostname: str, port: int):
    url = build_url(scheme=scheme, host=hostname, port=port)

    r = fetch_http(url, timeout=10)
    if type(r) is not Response:
        print(f"http redirect: {url} :: Error: not responding.")
        return (False, scheme, hostname, port, 
                url, None, None, r)

    if r.status_code >= 300 and r.status_code < 400:
        print(f"http redirect: {url} :: redirect to: {r.headers['Location']}")
        return (True, scheme, hostname, port, 
                url, r.status_code, r.headers['Location'],
                None)

    print(f"http redirect: {url} :: no redirect")
    return (True, scheme, hostname, port, 
            url, r.status_code, None, None)


def huntredirect_filter_targets(bag) -> list[tuple]:
    target_http_endpoint_list = huntredirect_get_defaults()

    # Filter targets: no TCP port open? No target for redirect.
    filtered_tuple_targets = []
    for b in bag:
        for port, scheme in target_http_endpoint_list.items():
            if f"{PREFIX_TCP}{port}" not in b:
                continue

            if not b[f"{PREFIX_TCP}{port}"]:
                id = gen_field_id(scheme, port)
                b[id] = f"n/a: no TCP to {port}"
                continue

            # Output is a list of tuple with url, scheme, hostname, port
            filtered_tuple_targets.append((scheme, b['FQDN'], port))

    return filtered_tuple_targets


def huntredirect_multi_target(bag):
    filtered_tuple_targets = huntredirect_filter_targets(bag)

    results = []

    # Start scan
    for target_tuple in filtered_tuple_targets:
        scheme, hostname, port = target_tuple
        res_tuple = analyse_http(scheme, hostname, port)
        results.append(res_tuple)

    return results
                

def huntredirect_reformat_results_into_bag(results, bag):
    for b in bag:
        for res_success, res_scheme, res_hostname, \
                res_port, res_url, res_status_code, \
                res_location, error_str in results:

            id = gen_field_id(res_scheme, res_port)

            if b['FQDN'] == res_hostname:
                if not res_success:
                    b[id] = f"url: {res_url} :: error: {error_str}"
                else:
                    res_txt = f"url: {res_url} :: status: {res_status_code} -> location: {res_location}"
                    b[id] = res_txt

    return bag