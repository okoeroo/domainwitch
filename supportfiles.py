import csv
from huntdns import huntdns_fieldnames
from hunttcp import hunttcp_fieldnames
from huntredirect import huntredirect_fieldnames


def openfile(filename: str) -> list:
    lines = tuple(open(filename, 'r'))
    with open(filename) as f:
        lines = f.read().splitlines()

    return lines


def write_csv(outputfile: str, output_dict_list: dict) -> None:
    if not output_dict_list and len(output_dict_list) == 0:
        raise RuntimeError("There is no output to write.")

    # Fetch fieldnames from first line of the dict keys
    fieldnames = ['FQDN'] + \
                    huntdns_fieldnames() + \
                    hunttcp_fieldnames() + \
                    huntredirect_fieldnames()

    # write csv
    with open(outputfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                quotechar='\"', quoting=csv.QUOTE_STRINGS)
        writer.writeheader()
        for d_line in output_dict_list:
            writer.writerow(d_line)

