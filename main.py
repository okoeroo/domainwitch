#!/usr/bin/env python3

import sys

from supportfiles   import write_csv, openfile
from huntdns        import huntdns
from hunttcp        import hunttcp
from huntredirect   import huntredirect


def witchhunt(targets) -> None:
    out = []

    for target in targets:
        # Prep results
        prey = {}
        prey['FQDN'] = target

        # Hunt DNS
        target_r_types = ['A', 'AAAA', 'CNAME', 'TXT', 'HTTPS', 'CERT',
                          'SRV', 'CAA', 'MX', 'SOA', 'NS', 'TLSA']
        prey = huntdns(prey, target_r_types, target)

        # Hunt TCP
        target_tcp_ports = [21, 22, 25, 53, 80, 111, 135, 139, 443, 445, 465, 587,
                            993, 995, 1723, 3306, 3389, 5900, 8080, 5060, 5061]
        prey = hunttcp(prey, target_tcp_ports, target)

        # Hunt HTTP redirect
        prey = huntredirect(prey, target)

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
