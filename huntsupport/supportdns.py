import asyncio
import dns.resolver


async def query_dns(hunt_id, hostname, r_type='A'):
    loop = asyncio.get_event_loop()
    
    # Use the default resolver (system resolver)
    resolver = dns.resolver.Resolver()

    try:
        answers = await loop.run_in_executor(None, resolver.query, hostname, r_type)
        rdatas = ", ".join([str(rdata) for rdata in answers])

        return (hunt_id, True, hostname, r_type, rdatas, "OK")

    except dns.resolver.NoAnswer as err:
        print(f"NoAnswer: ({hostname}:{r_type}) {err}")
        return (hunt_id, False, hostname, r_type, None, "Error: NoAnswer")
    except dns.resolver.NoNameservers as err:
        print(f"NoNameservers: ({hostname}:{r_type}) {err}")
        return (hunt_id, False, hostname, r_type, None, "Error: NoNameservers")
    except dns.resolver.NXDOMAIN as err:
        print(f"NXDOMAIN: ({hostname}:{r_type}) {err}")
        return (hunt_id, False, hostname, r_type, None, "Error: NXDOMAIN")
    except Exception as err:
        print(f"Unexpected ({hostname}:{r_type}) {err}, {type(err)}")
        return (hunt_id, False, hostname, r_type, None, f"Error: Unexpected: {err} :: {type(err)}")