#!/usr/bin/env python3
"""Docstring."""

import sys
import my_module as mod

def get_args():
    """Get user arguments"""
    if not len(sys.argv) == 3:
        print("USAGE: python3 split_into_columns.py elements_per_read_file outfile")
        sys.exit()
    return sys.argv[1:]

def main():
    """Do the things."""
    results, outfile = get_args()
    newlines = ["experiment,read,promoter1,rbs1,cds1,terminator1,promoter2,rbs2,cds2,terminator2"]
    oldlines = mod.get_file_data(results)[1:]
    promoters = ["J23100", "J23102", "J23118", "J23107", "J23116", "J23113"]
    rbs = ["RBSc42", "RBSc36", "RBSc58", "RBSc44", "RBSc13", "RBSc33"]
    cds = ["lacZ", "pyrE", "pyrF", "sfGFP", "Mcherry", "symE", "pac", "igoT",
           "mdtM", "dctM:siaM", "G_24769", "nhaK", "siaT"]
    terminators = ["T1_L3S2P55", "T2_L3S2P21", "T3_ECK120033737",
                   "T4_ECK120029600"]

    lookup = {1 : promoters, 2 : rbs, 3 : cds, 4 : terminators,
              5 : promoters, 6 : rbs, 7 : cds, 8 : terminators}
    for line in oldlines:
        fields = line.split(",")
        sequence = line.split(",")[2].split(";")
        element_list = []
        if "US_marker_lvl2" in sequence and "DS_marker_lvl2" in sequence:
            for i in range(len(sequence)-1):
                if sequence[i] == "DS_marker_lvl2":
                    if sequence[i+1] == "US_marker_lvl2":
                        break
                    k = 8
                    j = 1
                    while len(element_list) < 8:
                        if sequence[i + j] in lookup[k]:
                            element_list.append(sequence[i + j])
                            j += 1
                        else:
                            element_list.append("")
                        k -= 1
                    #add the line
                    element_list.reverse()
                    newlines.append(",".join([fields[0], fields[1]]) + "," + ",".join(element_list))
                    break
                elif sequence[i] == "US_marker_lvl2":
                    if sequence[i+1] == "DS_marker_lvl2":
                        break
                    j = 1
                    k = 1
                    while len(element_list) < 8:
                        if sequence[i + j] in lookup[k]:
                            element_list.append(sequence[i + j])
                            j += 1
                        else:
                            element_list.append("")
                        k += 1
                    #add the line
                    newlines.append(",".join([fields[0], fields[1]]) + "," + ",".join(element_list))
                    break
    with open(outfile, "w", encoding = "utf8") as out:
        out.write("\n".join(newlines) + "\n")


                        
                    


if __name__ == "__main__":
    main()
