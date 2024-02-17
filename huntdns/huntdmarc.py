import asyncio
from huntsupport.supportdns import query_dns


HUNT_ID = "huntdmarc"


# target_r_types
def huntdns_get_defaults() -> list[str]:
    return ['DMARC']


def huntdns_fieldnames() -> list[str]:
    return huntdns_get_defaults()


def huntdns_reformat_results_into_bag(results: list[tuple], bag):
    for b in bag:
        for res in results:
            if res[2] == b['FQDN']:
                b[res[3]] = res[4]
    return bag


async def huntdns_multi_target(targets):
    target_r_types = huntdns_get_defaults()
    tasks = [query_dns(target, r_type) for target in targets for r_type in target_r_types]
    return await asyncio.gather(*tasks)