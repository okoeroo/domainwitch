#!/usr/bin/env python3

import sys

from supportfiles   import write_csv, openfile
from huntdns        import huntdns, huntdns_get_defaults
from hunttcp        import hunttcp, hunttcp_get_defaults
from huntredirect   import huntredirect


def witchhunt(targets) -> None:
    out = []

    for target in targets:
        # Prep results
        prey = {}
        prey['FQDN'] = target

        # Hunt DNS
        target_r_types = huntdns_get_defaults()
        prey = huntdns(prey, target_r_types, target)

        # Hunt TCP
        target_tcp_ports = hunttcp_get_defaults()
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
