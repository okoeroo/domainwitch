import csv


def openfile(filename) -> list:
    lines = tuple(open(filename, 'r'))
    with open(filename) as f:
        lines = f.read().splitlines()

    return lines


def write_csv(outputfile, output_dict_list) -> None:
    if not output_dict_list and len(output_dict_list) == 0:
        raise RuntimeError("There is no output to write.")

    # Fetch fieldnames from first line of the dict keys
    fieldnames = [x for x in output_dict_list[0].keys()]

    # reorder fields: FQDN in front
    old_index = fieldnames.index('FQDN')
    fieldnames.insert(0, fieldnames.pop(old_index))

    # write csv
    with open(outputfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                quotechar='\"', quoting=csv.QUOTE_STRINGS)
        writer.writeheader()
        for d_line in output_dict_list:
            writer.writerow(d_line)

