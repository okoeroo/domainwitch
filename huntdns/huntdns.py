import asyncio
from huntsupport.supportdns import query_dns, get_hostname, get_r_type, get_rdatas


HUNT_ID = "huntdns"


# target_r_types
def huntdns_get_defaults() -> list[str]:
    return ['A', 'AAAA', 'CNAME', 'TXT', 'HTTPS', 'CERT', 'SRV', 'CAA', 'MX',
            'SOA', 'NS', 'TLSA']


def huntdns_fieldnames() -> list[str]:
    return huntdns_get_defaults()


def huntdns_reformat_results_into_bag(results: list[tuple], bag):
    for b in bag:
        for res in results:
            if get_hostname(res) == b['FQDN']:
                b[get_r_type(res)] = get_rdatas(res)
    return bag


async def huntdns_multi_target(targets):
    target_r_types = huntdns_get_defaults()
    tasks = [query_dns(HUNT_ID, target, r_type) for target in targets for r_type in target_r_types]
    return await asyncio.gather(*tasks)