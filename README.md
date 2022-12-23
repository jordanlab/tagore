   * [tagore](#tagore)  
      * [Installation](#installation)  
         * [Requirements](#requirements)  
      * [Quick start](#quick-start)  
      * [Usage](#usage)  
      * [Input file description](#input-file-description)  
      * [Etymology](#etymology)  

# tagore

`tagore` is a simple way to visualize features on human chromosome ideograms as shown in this article: https://www.nature.com/articles/srep12376

`tagore` was designed to allow everyone to create 23andMe style chromosome painting diagrams.

![tagore](https://github.com/jordanlab/tagore/raw/master/tagore.png)

## Installation

`tagore` is a simple Python script that uses the RSVG library and has no other depenendies.

```bash
pip install tagore
tagore --version
# tagore (version 1.1.2)
```

### Requirements
* Python 3.6+
* [RSVG](https://developer.gnome.org/rsvg/stable/)
* [Click](https://click.palletsprojects.com/en/7.x/) (automatically installed if `pip` is used)

## Quick start

The demo data consists of [Catalogue of Somatic Mutations in Cancer (COSMIC) Cancer Gene Census](https://www.nature.com/articles/s41568-018-0060-1) genes and 100 randomly simulated mutations.  Points represent single nucleotide variants (i.e. variant present in <3 samples); triangles represent single nucleotide polymorphisms (i.e. variants found in many samples); and short lines (single chromosome) represent known INDEL sites.

```bash
tagore --input example_ideogram/test.bed --prefix example_ideogram/example -vf
```

## Usage
```
usage: tagore [-h] [--version] -i <input.bed> [-p [output file prefix]] [-b [hg78/hg38]] [-f] [-v]

tagore: a utility for illustrating human chromosomes https://github.com/jordanlab/tagore

optional arguments:
  -h, --help                                              show this help message and exit
  --version                                               Print the software version
  -i <input.bed>, --input <input.bed>                     Input BED-like file
  -p [output file prefix], --prefix [output file prefix]  Output prefix [Default: "out"]
  -b [hg78/hg38], --build [hg78/hg38]                     Human genome build to use [Default: hg38]
  -f, --force                                             Overwrite output files if they exist already
  -v, --verbose                                           Display verbose output

```
The input file is a bed-like format, described below.  If an output prefix is not specified, the scripts uses "out" as the default prefix.

Helper scripts for converting RFMix and ADMIXTURE outputs are included in the `scripts/` folder.

A more complete example of a full chromosome painting using an RFMix output can be seen by running:

```bash
rfmix2tagore --chr1 example_ideogram/1KGP-MXL104_chr1.bed \
	--chr2 example_ideogram/1KGP-MXL104_chr2.bed \
	--out example_ideogram/1KGP-MXL104_tagore.bed

tagore --input example_ideogram/1KGP-MXL104_tagore.bed \
	--prefix example_ideogram/1KGP-MXL104 \
  --build hg37 \
  --verbose

```

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


## Etymology

[Tagore](https://en.wikipedia.org/wiki/Rabindranath_Tagore) (/tæˈgɔːr/) was a prolific songwriter,
 artist, and influential poet of 19th and 20th century India.  Notably, Tagore spoke out against
 racial prejudice and espoused the princple respect for all people, regardless of ancestry or
 ethnic bacground.
