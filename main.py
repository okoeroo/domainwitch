#!/usr/bin/env python3

import sys

from support import write_csv, openfile
from huntdns import huntdns
from hunttcp import hunttcp


def witchhunt(targets) -> None:
    out = []

    for target in targets:
        # Prep results
        prey = {}
        prey['FQDN'] = target

        # Add types of hunts here
        target_r_types = ['A', 'AAAA', 'CNAME', 'TXT', 'ALIAS', 'HTTPS', 'CERT', 'SRV', 'CAA', 'MX', 'SOA', 'NS', 'RRSIG', 'TLSA']
        prey = huntdns(prey, target_r_types, target)

        # Gather output per target
        out.append(prey)

    return out


def main() -> None:
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    lines = openfile(inputfile)
    out = witchhunt(lines)

    write_csv(outputfile, out)


if __name__ == '__main__':
    main()
