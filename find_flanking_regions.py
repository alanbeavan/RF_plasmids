#!/usr/bin/env python3
"""
Find the distance between the start of the read, the first element and the
last element and the end of the read. Maybe this could be extended to have
little genome browser type figures.

   || | |||| || 
--------------------------------------------
                     || ||||||| | ||

this sort of thing^ but I don't know how to do that. I guess first, each could
be written as 0-X nothing important X-X+n prototor X+n X+n+m RBS etc etc.
"""

import my_module as mod
import matplotlib
from dna_features_viewer import GraphicFeature, GraphicRecord

def read_fasta(filename):
    lines = mod.get_file_data(filename)
    seqs = {}
    key = ""
    value = ""

    for line in lines:
        line = line.rstrip("\n")
        if line.startswith(">"):
            if key:
                seqs[key] = value
                key = line[1:]
            else:
                key = line[1:]
            value = ""
        else:
            value = value + line
    seqs[key] = value
    return seqs


def main():
    """Do the things."""
    seqs = {}
    seqs["M"] = read_fasta("sequencing_1/M/M_raw.fasta")
    seqs["EF1"] = read_fasta("sequencing_2/EF1/EF1_raw.fasta")
    seqs["EF2"] = read_fasta("sequencing_2/EF2/EF2_raw.fasta")
    for reads in seqs.values():
        headers = list(reads.keys())
        for header in headers:
            reads[header.split()[0]] = reads.pop(header)

    new_table = ["experiment,read,sequence,start_flank,end_flank,read_length"]
    read_structures = {}
    for line in mod.get_file_data("elements_per_read.csv")[1:]:
        start_flank = 0
        end_flank = 0
        fields = line.split(",")
        seq = seqs[fields[0]][fields[1]]
        features = []
        non_graphic = {}
        for i in range(len(fields[2].split(";"))):
            element = fields[2].split(";")[i]
            span = fields[3].split(";")[i]
            start = span.split(":")[0]
            end = span.split(":")[1]
            if "-" in start and "-" in end:
                strand = "-1"
                start = start[1:]
                end = end[1:]
            elif "-" not in start and "-" not in end:
                strand = "+1"
            else:
                print("Uh Oh")
                exit()
                
            #colour by element type
            if element.startswith("J23"):
                colour = "#cffccc"
            elif element.startswith("RBS"):
                colour = "#ffd700"
            elif element.startswith("T"):
                colour = "#ffcccc"
            else:
                colour = "#ccccff"
            
            features.append(GraphicFeature(start=int(start), end=int(end),
                                           strand=int(strand), color=colour,
                                           label=element))
            if i == 0 and start != "1":
                non_graphic["1:" + str(int(start) - 1)] = "no_hits"
                start_flank = int(start) - 1
            non_graphic[start + ":" + end] = element
            if i == len(fields[2].split(";")) - 1 and end != len(seq):
                non_graphic[str(int(end)+1) + ":" + str(len(seq))] = "no_hits"
                end_flank = len(seq) - int(end)

        #write the graphic file and add line to table
        record = GraphicRecord(sequence_length=len(seq), features=features)
        ax, _ = record.plot(figure_width=25)
        ax.figure.savefig("graphics/" + fields[0] + "_" + fields[1] + ".pdf", bbox_inches='tight')
        matplotlib.pyplot.close()
        sequence_string = []
        for key, value in non_graphic.items():
            sequence_string.append(key + "-" + value)
        sequence_string = ";".join(sequence_string)
        new_table.append(fields[0] + "," + fields[1] + "," + sequence_string +
                         "," + str(start_flank) + "," + str(end_flank) + "," +
                         str(len(seq)))
    with open("full_read_structures.csv", "w", encoding = "utf8") as out:
        out.write("\n".join(new_table) + "\n")
                

            
            
        


if __name__ == "__main__":
    main()
