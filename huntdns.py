import asyncio
import dns.resolver


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

        return (True, hostname, r_type, rdatas, "OK")

    except dns.resolver.NoAnswer as err:
        print(f"NoAnswer: {err}")
        return (False, hostname, r_type, None, "Error: NoAnswer")
    except dns.resolver.NoNameservers as err:
        print(f"NoNameservers: {err}")
        return (False, hostname, r_type, None, "Error: NoNameservers")
    except dns.resolver.NXDOMAIN as err:
        print(f"NXDOMAIN: {err}")
        return (False, hostname, r_type, None, "Error: NXDOMAIN")
    except Exception as err:
        print(f"Unexpected ({fqdn}:{r_type}) {err}, {type(err)}")
        return (False, hostname, r_type, None, f"Error: Unexpected: {err} :: {type(err)}")


async def start_dns_scan(target: str, target_r_types: list[str]):
    tasks = [query_dns(target, r_type) for r_type in target_r_types]
    return await asyncio.gather(*tasks)
 

def reformat_results(results: list[tuple], prey):
    for res in results:
        if res[0]:
            prey[res[2]] = res[3]
    return prey

    
def huntdns(prey, target_r_types, target) -> None:
    target_r_types = huntdns_get_defaults()
    results = asyncio.run(start_dns_scan(target, target_r_types))
    prey = reformat_results(results, prey)

    return prey