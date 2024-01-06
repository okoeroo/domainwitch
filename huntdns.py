import dns.resolver


# target_r_types
def huntdns_get_defaults() -> list[str]:
    return ['A', 'AAAA', 'CNAME', 'TXT', 'HTTPS', 'CERT', 'SRV', 'CAA', 'MX',
            'SOA', 'NS', 'TLSA']


def resolver(fqdn, r_type) -> str:
    try:
        answers = dns.resolver.resolve(fqdn, r_type)
        rdatas = ", ".join([str(rdata) for rdata in answers])
        
        return rdatas

    except dns.resolver.NoAnswer as err:
        print(f"NoAnswer: {err}")
        return "Error: NoAnswer"
    except dns.resolver.NoNameservers as err:
        print(f"NoNameservers: {err}")
        return "Error: NoNameservers"
    except dns.resolver.NXDOMAIN as err:
        print(f"NXDOMAIN: {err}")
        return "Error: NXDOMAIN"
    except Exception as err:
        print(f"Unexpected ({fqdn}:{r_type}) {err}, {type(err)}")
        return f"Error: Unexpected: {err} :: {type(err)}"

    return None


def huntdns(prey, target_r_types, target) -> None:
    for r_type in target_r_types:
        prey[r_type] = resolver(target, r_type)

    return prey
