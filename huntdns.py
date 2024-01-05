import dns.resolver


def resolver(fqdn, r_type) -> str:
    try:
        answers = dns.resolver.resolve(fqdn, r_type)
        rdatas = ", ".join([str(rdata) for rdata in answers])
        
        return rdatas

    except dns.resolver.NoAnswer as err:
        print(f"NoAnswer: {err}")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

    return None


def huntdns(prey, target_r_types, target) -> None:
    for r_type in target_r_types:
        prey[r_type] = resolver(target, r_type)

    return prey
