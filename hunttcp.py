import asyncio


PREFIX = "port_"


def hunttcp_get_defaults() -> list[int]:
    return [21, 22, 25, 53, 67, 68, 69, 80, 110, 111, 123, 135, 137, 138, 139,
    161, 179, 389, 443, 445, 465, 514, 515, 548, 587, 636, 666, 993, 995, 1352,
    1433, 1434, 1521, 1524, 1701, 1720, 1723, 1900, 2000, 3306, 3389, 3456,
    3457, 4444, 5060, 5061, 5555, 5900, 6000, 6666, 6667, 6668, 6669, 7000,
    7001, 8000, 8080, 8081, 8088, 8181, 8443, 8888, 9100, 9876, 9898, 9999,
    11211, 17185, 27374, 27375, 27376, 27377, 27378, 27379, 31337]


def hunttcp_fieldnames() -> list[str]:
    return [f"{PREFIX}{x}" for x in hunttcp_get_defaults()]


async def check_service(host, port, timeout=5):
    try:
        # Connect with a specified timeout
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        print(f"Service at {host}:{port} is up")
        return (True, host, port)

    except (ConnectionRefusedError, asyncio.TimeoutError):
        print(f"Service at {host}:{port} is down")
        return (False, host, port)
    except Exception as err:
        print(f"TCP error: ({host}:{port}) {err}")
        return (False, host, port)


async def check_services(services, timeout=5):
    tasks = [check_service(host, port, timeout) for host, port in services]
    return await asyncio.gather(*tasks)


def reformat_results(results: list[tuple], prey):
    for r in results:
        # Format is connection booling, target host, port
        id = PREFIX + str(r[2])
        # Note: it is vital for other modules to use bool
        prey[id] = r[0]

    return prey


def hunttcp(prey: dict, target: str):
    target_tcp_ports = hunttcp_get_defaults()

    services = []
    for p in target_tcp_ports:
        services.append((target, p))

    timeout = 3
    results = asyncio.run(check_services(services, timeout))
    prey = reformat_results(results, prey)

    return prey