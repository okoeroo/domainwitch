#!/usr/bin/env python3

import sys
import asyncio

from huntsupport.supportfiles   import write_csv, openfile
from huntdns.huntdns            import huntdns_multi_target, huntdns_reformat_results_into_bag, huntdns_fieldnames
from huntdns.huntdmarc          import huntdmarc_multi_target, huntdmarc_reformat_results_into_bag, huntdmarc_fieldnames
from hunttcp.hunttcp            import hunttcp_multi_target, hunttcp_reformat_results_into_bag, hunttcp_fieldnames
from hunthttp.huntredirect      import huntredirect_multi_target, huntredirect_reformat_results_into_bag, huntredirect_fieldnames


def init_prey(target: str) -> dict:
    prey = {}
    prey['FQDN'] = target
    return prey


def witchhunt(targets) -> None:
    bag = []
    for t in targets:
        bag.append(init_prey(t))


    # Fetch fieldnames from first line of the dict keys
    fieldnames = ['FQDN'] + \
                    huntdns_fieldnames() + \
                    huntdmarc_fieldnames() + \
                    hunttcp_fieldnames() + \
                    huntredirect_fieldnames()

    # HuntDNS
    results = asyncio.run(huntdns_multi_target(targets))
    bag = huntdns_reformat_results_into_bag(results, bag)

    # HuntDMARC
    results = asyncio.run(huntdmarc_multi_target(targets))
    bag = huntdmarc_reformat_results_into_bag(results, bag)

    # HuntTCP
    results = asyncio.run(hunttcp_multi_target(targets))
    bag = hunttcp_reformat_results_into_bag(results, bag)

    #HuntRedirect
    results = huntredirect_multi_target(bag)
    bag = huntredirect_reformat_results_into_bag(results, bag)

    return fieldnames, bag


def main() -> None:
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    lines = openfile(inputfile)
    fieldnames, out = witchhunt(lines)

    write_csv(fieldnames, outputfile, out)


if __name__ == '__main__':
    main()
