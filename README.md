# da Vinci
da Vinci is a simple way to visualize features on human chromosome ideograms as shown in this article https://www.nature.com/articles/srep12376

### Script for creating pretty chromosome paintings

##### Author: Lavanya Rishishwar (Lrishishwar@ihrc.com)


## Requirements
* [RSVG](https://developer.gnome.org/rsvg/stable/)
* python-rsvg, available in most package managers

## Basic usage

./daVinci.pl -i input.bed -o outputPrefix

input.bed has to be be in a bed-like format, described below.  If an output prefix is not specified, the scripts uses "out" as the default prefix.

## Input file description
```
#chr	start	stop	feature	size	color	chrCopy
chr1	10000000	20000000	0	1	#FF0000	1
chr2	20000000	30000000	0	1	#FF0000	2
chr2	40000000	50000000	0	0.5	#FF0000	1
```

Each column is explained below:
1. *chr* - The chromosome on which a feature has to be drawn
2. *start* - Start position (in bp) for feature
3. *stop* - Stop position (in bp) for feature
4. *feature* - The shape of the feature to be drawn
	* 0 will draw a rectangle
	* 1 will draw a circle
	* 2 will draw a triangle pointing to the genomic location
	* 3 will draw a line at that genomic location
5. *size* - The horizontal size of the feature. Should range between 0 and 1.
6. *color* - Specify the color of the genomic feature with a hex value (#FF0000 for red, etc.)
7. *chrCopy* - Specify the chromosome copy on which the feature should be drawn (1 or 2).  To draw the same feature on both chromosomes, you must specify the feature twice
