#!/usr/bin/env python3
"""Work out the order of the elements in each read based on the blast hit results."""

import glob
import sys
import my_module as mod

def get_args():
    """Get user arguments"""
    if not len(sys.argv) == 2:
        print("USAGE: python3 get_order_of_elements.py experiment_dir")
        sys.exit()
    return sys.argv[1:]

def main():
    """
    Alright.
    fields 6 and 7 are the start and end of the hit on the query (plasmid read)
    fields 8 and 9 are the start and end of the hit on the subject (genetic element)
    It would be nice to have a secondary file with each promotor-rbs-gene-terminator sequence in each plasmid
    """
    direc = get_args()[0]
    runs = glob.glob(direc + "/*")
    runs = [run for run in runs if not "/_" in run]
    runs = [run for run in runs if not ".csv" in run]
    elements = ["promotors", "rbs", "cds", "terminators", "flankers"]
    outlines = ["experiment,read,sequence(; separated),positions (;spearated),order_doesn't_quite_work"]
    four_ele_combos_lines = ["experiment,read,promoter,rbs,gene,terminator"]
    genes = ["Mcherry", "sfGFP", "pyrE", "pyrF", "symE", "pac", "igoT",
             "mdtM", "dctM:siaM", "G_24769", "nhaK", "siaT", "lacZ"]
    for run in runs:
        if "/" in run:
            exp = run.split("/")[-1]
        else:
            exp = run
        hits_per_run = {}
        for ele in elements:
            results = mod.get_file_data(run + "/blast_hits_" + ele + ".tab")
            i = 1
            for line in results:
                fields = line.split("\t")
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
                #if reverse:
                    #plasmid_hit_start = str(0 - int(plasmid_hit_start))
                    #plasmid_hit_end = str(0 - int(plasmid_hit_end))
                if read in hits_per_run:
                    if hit in hits_per_run[read]:
                        hits_per_run[read][hit + "__" + str(i)] = [plasmid_hit_start, plasmid_hit_end]
                        i += 1
                    else:
                        hits_per_run[read][hit] = [plasmid_hit_start, plasmid_hit_end]
                else:
                    hits_per_run[read] = {hit : [plasmid_hit_start, plasmid_hit_end]}


        #OK - need to sort dictionary according to order of cooridnates.
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
                            #order.insert(i, without_underscores)
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
            for i in range(len(order)):
                if "__" in order[i]:
                    order[i] = order[i].split("__")[0]
            outlines.append(exp + "," + key + "," + ";".join(order) + "," + ";".join(indices) + "," + str(funky_order))
            #now get the sequences
            for i in range(len(order) - 3):
                if order[i].startswith("J23") and order[i+1].startswith("RBS") and order[i+2] in genes and order[i+3].startswith("T"):
                    four_ele_combos_lines.append(exp + "," + key + "," + ",".join(order[i:i+4]))
                elif order[i+3].startswith("J23") and order[i+2].startswith("RBS") and order[i+1] in genes and order[i].startswith("T"):
                    four_ele_combos_lines.append(exp + "," + key + "," + ",".join(reversed(order[i:i+4])))


    #write results
    with open(direc + "/elements_per_read.csv", "w", encoding = "utf8") as out:
        out.write("\n".join(outlines) + "\n")
    with open(direc + "/four_element_strings.csv", "w", encoding = "utf8") as out:
        out.write("\n".join(four_ele_combos_lines) + "\n")





if __name__ == "__main__":
    main()
