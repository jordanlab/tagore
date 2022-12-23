#!/bin/env python3
__author__ = "Aroon Chande"
__copyright__ = "Copyright 2019, Applied Bioinformatics Lab"
__license__ = "MIT"

import os

import click

commentBlock = """
# Each column is explained below:
# 1. chr - The chromosome on which a feature has to be drawn
# 2. start - Start position (in bp) for feature
# 3. stop - Stop position (in bp) for feature
# 4. feature - The shape of the feature to be drawn
# 	 0 - will draw a rectangle
# 	 1 - will draw a circle
# 	 2 - will draw a triangle pointing to the genomic location
# 	 3 - will draw a line at that genomic location
# 5. size - The horizontal size of the feature. Should range between 0 and 1.
# 6. color - Specify the color of the genomic feature with a hex value (#FF0000 for red, etc.)
# 7. chrCopy - Specify the chromosome copy on which the feature should be drawn (1 or 2).  To draw the same feature on both chromosomes, you must specify the feature twice
"""


@click.command()
@click.option(
    "--chr1",
    "-1",
    "chr1",
    default=None,
    type=click.File("r"),
    help="Chromosome 1 RFMix painting",
)
@click.option(
    "--chr2",
    "-2",
    "chr2",
    default=None,
    type=click.File("r"),
    help="Chromosome 2 RFMix painting",
)
@click.option("--afr", "afr", default="#0000ff ", help="Color for African blocks")
@click.option("--eur", "eur", default="#F4A500", help="Color for European blocks")
@click.option(
    "--nat", "nat", default="#D92414", help="Color for Native American / Asian blocks"
)
@click.option("--unk", "unk", default="#808080 ", help="Color for Unknown regions")
@click.option(
    "--out",
    "-o",
    "output",
    default=None,
    type=click.File("w"),
    help="Output da Vinci bed",
)
def main(chr1, chr2, afr, eur, nat, unk, output):
    colors = {"UNK": unk, "AFR": afr, "IBS": eur, "NAT": nat}
    output.write("#chr\tstart\tstop\tfeature\tsize\tcolor\tchrCopy")
    output.write(commentBlock)
    # chr1	10000000	20000000	0	1	#FF0000	1
    for line in chr1:
        line = line.split("\t")
        bedLine = f"chr{line[0]}\t{line[1]}\t{line[2]}\t0\t1\t{colors[line[3]]}\t1"
        output.write(bedLine + "\n")
    for line in chr2:
        line = line.split("\t")
        bedLine = f"chr{line[0]}\t{line[1]}\t{line[2]}\t0\t1\t{colors[line[3]]}\t2"
        output.write(bedLine + "\n")


if __name__ == "__main__":
    main()
