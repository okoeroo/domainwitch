import asyncio
from huntsupport.supportdns import query_dns, get_hostname, get_rdatas


HUNT_ID = "huntdmarc"


# target_r_types
def huntdmarc_get_defaults() -> list[str]:
    return ['TXT']


def huntdmarc_fieldnames() -> list[str]:
    return ['DMARC']


def huntdmarc_reformat_results_into_bag(results: list[tuple], bag):
    for b in bag:
        for res in results:
            if get_hostname(res) == "_dmarc." + b['FQDN']:
                b['DMARC'] = get_rdatas(res)
    return bag


async def huntdmarc_multi_target(targets):
    tasks = [query_dns(HUNT_ID, "_dmarc." + target, "TXT") for target in targets]
    return await asyncio.gather(*tasks)