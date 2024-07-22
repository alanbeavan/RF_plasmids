#!/usr/bin/env python3
"""Work out the order of the elements in each read based on the blast hit results."""

import my_module as mod

def main():
    """
    Alright.
    fields 6 and 7 are the start and end of the hit on the query (plasmid read)
    fields 8 and 9 are the start and end of the hit on the subject (genetic element)
    It would be nice to have a secondary file with each promotor-rbs-gene-terminator sequence in each plasmid
    """
    runs = ["M", "EF1", "EF2"]
    elements = ["promotors", "rbs", "genes", "terminators"]
    outlines = ["experiment,read,sequence(; separated),positions (;spearated),order_doesn't_quite_work"]
    four_ele_combos_lines = ["experiment,read,promoter,rbs,gene,terminator"]
    genes = ["igoT", "mdtM", "dctM:siaM", "G_24769", "nhaK", "siaT", "symE", "pac"]
    for run in runs:
        hits_per_run = {}
        for ele in elements:
            results = mod.get_file_data(run + "_" + ele + "_hits.csv")[1:]
            for line in results:
                fields = line.split(",")
                read = fields[0]
                hit = fields[1]
                plasmid_hit_start = fields[6]
                plasmid_hit_end = fields[7]
                gene_hit_start = fields[8]
                gene_hit_end = fields[9]
                if gene_hit_start > gene_hit_end:
                    reverse = 1
                else:
                    reverse = 0
                if reverse:
                    plasmid_hit_start = str(0 - int(plasmid_hit_start))
                    plasmid_hit_end = str(0 - int(plasmid_hit_end))
                if read in hits_per_run:
                    hits_per_run[read][hit] = [plasmid_hit_start, plasmid_hit_end]
                else:
                    hits_per_run[read] = {hit : [plasmid_hit_start, plasmid_hit_end]}
        for key, value in hits_per_run.items():
            #get the order
            order = []
            for key1, value1 in value.items():
                if len(order) == 0:
                    order.append(key1)
                else:
                    flag = 0
                    for i in range(len(order)):
                        if abs(int(value1[1])) < abs(int(value[order[i]][0])):
                            order.insert(i, key1)
                            flag = 1
                            break
                    if not flag:
                        order.append(key1)
            indices = []
            funky_order = 0
            for ele in order:
                indices.append(str(hits_per_run[key][ele][0]) + ":" + str(hits_per_run[key][ele][1]))
                if len(indices) >= 2:
                    if abs(int(hits_per_run[key][ele][0])) <= abs(int(indices[-2].split(":")[1])):
                        funky_order = 1
            outlines.append(run + "," + key + "," + ";".join(order) + "," + ";".join(indices) + "," + str(funky_order))
            #now get the sequences
            for i in range(len(order) - 3):
                if order[i].startswith("J23") and order[i+1].startswith("RBS") and order[i+2] in genes and order[i+3].startswith("T"):
                    four_ele_combos_lines.append(run + "," + key + "," + ",".join(order[i:i+4]))
                elif order[i+3].startswith("J23") and order[i+2].startswith("RBS") and order[i+1] in genes and order[i].startswith("T"):
                    four_ele_combos_lines.append(run + "," + key + "," + ",".join(reversed(order[i:i+4])))


    #write results
    with open("elements_per_read.csv", "w", encoding = "utf8") as out:
        out.write("\n".join(outlines) + "\n")
    with open("four_element_strings.csv", "w", encoding = "utf8") as out:
        out.write("\n".join(four_ele_combos_lines) + "\n")





if __name__ == "__main__":
    main()
