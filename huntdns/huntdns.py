import asyncio
import dns.resolver


HUNT_ID = "huntdns"


# target_r_types
def huntdns_get_defaults() -> list[str]:
    return ['A', 'AAAA', 'CNAME', 'TXT', 'HTTPS', 'CERT', 'SRV', 'CAA', 'MX',
            'SOA', 'NS', 'TLSA']


def huntdns_fieldnames() -> list[str]:
    return huntdns_get_defaults()


async def query_dns(hostname, r_type='A'):
    loop = asyncio.get_event_loop()
    
    # Use the default resolver (system resolver)
    resolver = dns.resolver.Resolver()

    try:
        answers = await loop.run_in_executor(None, resolver.query, hostname, r_type)
        rdatas = ", ".join([str(rdata) for rdata in answers])

        return (HUNT_ID, True, hostname, r_type, rdatas, "OK")

    except dns.resolver.NoAnswer as err:
        print(f"NoAnswer: ({hostname}:{r_type}) {err}")
        return (HUNT_ID, False, hostname, r_type, None, "Error: NoAnswer")
    except dns.resolver.NoNameservers as err:
        print(f"NoNameservers: ({hostname}:{r_type}) {err}")
        return (HUNT_ID, False, hostname, r_type, None, "Error: NoNameservers")
    except dns.resolver.NXDOMAIN as err:
        print(f"NXDOMAIN: ({hostname}:{r_type}) {err}")
        return (HUNT_ID, False, hostname, r_type, None, "Error: NXDOMAIN")
    except Exception as err:
        print(f"Unexpected ({hostname}:{r_type}) {err}, {type(err)}")
        return (HUNT_ID, False, hostname, r_type, None, f"Error: Unexpected: {err} :: {type(err)}")


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