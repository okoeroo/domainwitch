import csv


def openfile(filename: str) -> list:
    lines = tuple(open(filename, 'r'))
    with open(filename) as f:
        lines = f.read().splitlines()

    return lines


def write_csv(outputfile: str, output_dict_list: dict) -> None:
    if not output_dict_list and len(output_dict_list) == 0:
        raise RuntimeError("There is no output to write.")

    # Fetch fieldnames from first line of the dict keys
    fieldnames = [x for x in output_dict_list[0].keys()]

    # reorder fields: FQDN in front
    old_index = fieldnames.index('FQDN')
    fieldnames.insert(0, fieldnames.pop(old_index))

    # HACK
    port_list = {"80": "http", "443": "https", "8080": "http"}
    for port, scheme in port_list.items():
        fieldnames.append(f"redirect_http_{port}")

    # write csv
    with open(outputfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                quotechar='\"', quoting=csv.QUOTE_STRINGS)
        writer.writeheader()
        for d_line in output_dict_list:
            writer.writerow(d_line)

