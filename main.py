#!/usr/bin/env python3

import sys
import asyncio

from huntsupport.supportfiles   import write_csv, openfile
from huntdns.huntdns            import huntdns, huntdns_multi_target, huntdns_reformat_results_into_bag
from hunttcp.hunttcp            import hunttcp, hunttcp_multi_target, hunttcp_reformat_results_into_bag
from hunthttp.huntredirect      import huntredirect, huntredirect_multi_target, huntredirect_reformat_results_into_bag


def init_prey(target: str) -> dict:
    prey = {}
    prey['FQDN'] = target
    return prey


def witchhunt(targets) -> None:
    bag = []
    for t in targets:
        bag.append(init_prey(t))

    # HuntDNS
    results = asyncio.run(huntdns_multi_target(targets))
    bag = huntdns_reformat_results_into_bag(results, bag)

    # HuntTCP
    results = asyncio.run(hunttcp_multi_target(targets))
    bag = hunttcp_reformat_results_into_bag(results, bag)

    #HuntRedirect
    results = huntredirect_multi_target(bag)
    bag = huntredirect_reformat_results_into_bag(results, bag)

    return bag


def main() -> None:
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    lines = openfile(inputfile)
    out = witchhunt(lines)

    write_csv(outputfile, out)


if __name__ == '__main__':
    main()
