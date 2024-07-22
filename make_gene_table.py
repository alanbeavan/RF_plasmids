#!/usr/bin/env python3
"""Docstring."""

import my_module as mod

def main():
    """Do the things."""
    experiments = ["M", "EF1", "EF2"]
    genes = ["pac", "symE", "G_24769", "dctM:siaM", "igoT", "siaT"]
    lengths = {"EF1" : 1633, "EF2" : 793, "M" : 580}
    table_lines = ["experiment,gene_set,count,total,%"]
    for exp in experiments:
        combos = {}
        for line in mod.get_file_data(exp + "_hits.csv")[1:]:
            fields = line.split(",")
            if fields[0] not in combos:
                combos[fields[0]] = [fields[1]]
            elif fields[1] not in combos[fields[0]]:
                combos[fields[0]].append(fields[1])
                combos[fields[0]] = sorted(combos[fields[0]])
        combos_reversed = {}
        total = 0
        for key, value in combos.items():
            if ";".join(value) not in combos_reversed:
                combos_reversed[";".join(value)] = 1
            else:
                combos_reversed[";".join(value)] += 1
            total += 1
        combos_reversed["none"] = lengths[exp] - total
        for key, value in combos_reversed.items():
            table_lines.append(exp + "," + key + "," + str(value) + "," + str(lengths[exp]) + "," + str(value/lengths[exp]))
    with open("gene_table.csv", "w", encoding = "utf8") as out:
        out.write("\n".join(table_lines) + "\n")



if __name__ == "__main__":
    main()
