import asyncio


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
        print(f"Generic exception: {err}")
        return (False, host, port)


async def check_services(services, timeout=5):
    tasks = [check_service(host, port, timeout) for host, port in services]
    return await asyncio.gather(*tasks)


def reformat_results(results: list[tuple], prey: str):
    for r in results:
        # Format is connection booling, target host, port
        id = 'port_' + str(r[2])
        # Note: it is vital for other modules to use bool
        prey[id] = r[0]

    return prey


def hunttcp(prey: dict, target_tcp_ports: list[int], target: str):
    services = []
    for p in target_tcp_ports:
        services.append((target, p))

    timeout = 4
    results = asyncio.run(check_services(services, timeout))
    prey = reformat_results(results, prey)

    return prey