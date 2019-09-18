#!/usr/bin/env python3
__author__ = ["Lavanya Rishishar", "Aroon Chande"]
__copyright__ = "Copyright 2019, Applied Bioinformatics Lab"
__license__ = "GPLv3"

import pickle
import re
import subprocess
import sys
from argparse import ArgumentParser, HelpFormatter


VERSION = 1.0
with open('base.svg.p', 'rb') as base:
	__CHR__ = pickle.load(base)

coordinates = {
	"1": {"cx": 1320.9, "cy": 1.5, "ht": 1654.5, "wd": 118.6},
	"2": {"cx": 1493.7, "cy": 43.6, "ht": 1612.4, "wd": 118.6},
	"3": {"cx": 1669.9, "cy": 341.4, "ht": 1314.7, "wd": 118.6},
	"4": {"cx": 1847.9, "cy": 517.9, "ht": 1138.1, "wd": 118.6},
	"5": {"cx": 2027.7, "cy": 461, "ht": 1195.1, "wd": 118.6},
	"6": {"cx": 2204.7, "cy": 524.2, "ht": 1131.8, "wd": 118.6},
	"7": {"cx": 2390.5, "cy": 608.5, "ht": 1047.5, "wd": 118.6},
	"8": {"cx": 2565.2, "cy": 692.8, "ht": 963.2, "wd": 118.6},
	"9": {"cx": 2746.8, "cy": 724.4, "ht": 931.6, "wd": 118.6},
	"10": {"cx": 2926.1, "cy": 766.6, "ht": 889.4, "wd": 118.6},
	"11": {"cx": 3103.8, "cy": 766.6, "ht": 889.4, "wd": 118.6},
	"12": {"cx": 3287.9, "cy": 769.7, "ht": 886.3, "wd": 118.6},
	"13": {"cx": 1321.6, "cy": 2068.8, "ht": 766.1, "wd": 118.6},
	"14": {"cx": 1493.9, "cy": 2121.5, "ht": 713.4, "wd": 118.6},
	"15": {"cx": 1669.8, "cy": 2153.1, "ht": 681.8, "wd": 118.6},
	"16": {"cx": 1849, "cy": 2232.2, "ht": 602.8, "wd": 118.6},
	"17": {"cx": 2033.5, "cy": 2290.7, "ht": 544.3, "wd": 118.6},
	"18": {"cx": 2208, "cy": 2313.9, "ht": 521.1, "wd": 118.6},
	"19": {"cx": 2391.8, "cy": 2437.2, "ht": 397.8, "wd": 118.6},
	"20": {"cx": 2566.7, "cy": 2416.1, "ht": 418.9, "wd": 118.6},
	"21": {"cx": 2745.3, "cy": 2510.9, "ht": 324.1, "wd": 118.6},
	"22": {"cx": 2929.2, "cy": 2489.8, "ht": 345.1, "wd": 118.6},
	"X": {"cx": 3103.3, "cy": 1799.6, "ht": 1035.4, "wd": 59},
}

chromSizes = {
	"1": 249250621, "2": 243199373, "3": 198022430, "4": 191154276,
	"5": 180915260, "6": 171115067, "7": 159138663, "8": 146364022,
	"9": 141213431, "10": 135534747, "11": 135006516, "12": 133851895,
	"13": 115169878, "14": 107349540, "15": 102531392, "16": 90354753,
	"17": 81195210, "18": 78077248, "19": 59128983, "20": 63025520,
	"21": 48129895, "22": 51304566, "X": 155270560, "Y": 59373566
}


def draw(opts):
	try:
		input = open(opts.input, 'r')
	except (IOError, EOFError) as e:
		print("Error opening input file!")
		raise(e)
	svg_fn = f"{opts.prefix}.svg"
	try:
		svg_fh = open(svg_fn, 'w')
		svg_fh.write(__CHR__)
	except (IOError, EOFError) as e:
		print("Error opening output file!")
		raise(e)
	lineNum = 1
	for entry in input:
		if entry.startswith("#"): continue
		entry = entry.rstrip().split("\t")
		if len(entry) != 7:
			print(f"Line number {lineNum} does not have 7 columns")
			os.exit()
		chrm, start, stop, feature, size, col, chrCopy = entry
		chrm = chrm.replace('chr', '')
		start = int(start); stop = int(stop); size = float(size); feature = int(feature); chrCopy = int(chrCopy)
		if 0 > size > 1:
			print(f"Feature size, {size},on line {lineNum} unclear. Please bound the size between 0 (0%) to 1 (100%). Defaulting to 1.")
			size = 1
		if not re.match("^#.{6}", col):
			print(f"Feature color, {col}, on line {lineNum} unclear.  Please define the color in hex starting with #.  Defaulting to #000000.")
			col = "#000000"
		if chrCopy not in [1,2]:
			print(f"Feature chromosome copy, {chrCopy}, on line {lineNum} unclear.  Skipping...")
			lineNum = lineNum + 1
			continue
		lineNum = lineNum + 1
		if feature == 0: # Rectangle
			ftStart = start*coordinates[chrm]["ht"]/chromSizes[chrm]
			ftEnd   = stop*coordinates[chrm]["ht"]/chromSizes[chrm]
			wd = coordinates[chrm]["wd"]*size/2
			if chrCopy == 1:
				x  = coordinates[chrm]["cx"] - wd
			else:
				x  = coordinates[chrm]["cx"]
			y  = coordinates[chrm]["cy"] + ftStart
			ht = ftEnd-ftStart
			svg_fh.write(f"<rect x=\"{x}\" y=\"{y}\" fill=\"{col}\" width=\"{wd}\" height=\"{ht}\"/>" + "\n")
		elif feature == 1: # Circle
			ftStart = start*coordinates[chrm]["ht"]/chromSizes[chrm]
			ftEnd   = stop*coordinates[chrm]["ht"]/chromSizes[chrm]
			r  = coordinates[chrm]["wd"]*size/4
			if chrCopy == 1:
				x  = coordinates[chrm]["cx"] - coordinates[chrm]["wd"]/4
			else:
				x  = coordinates[chrm]["cx"] + coordinates[chrm]["wd"]/4
			y  = coordinates[chrm]["cy"]+(ftStart+ftEnd)/2
			svg_fh.write(f"<circle fill=\"{col}\" cx=\"{x}\" cy=\"{y}\" r=\"{r}\"/>" + "\n")
		elif feature == 2: # Triangle
			ftStart = start*coordinates[chrm]["ht"]/chromSizes[chrm]
			ftEnd   = stop*coordinates[chrm]["ht"]/chromSizes[chrm]
			if chrCopy == 1:
				x  = coordinates[chrm]["cx"] - coordinates[chrm]["wd"]/2
				sx = 38.2*size
			else:
				x  = coordinates[chrm]["cx"] + coordinates[chrm]["wd"]/2
				sx = -38.2*size
			y  = coordinates[chrm]["cy"]+(ftStart+ftEnd)/2
			sy = 21.5*size
			svg_fh.write(f"<polygon fill=\"{col}\" points=\"{x-sx},{y-sy} {x},{y} {x-sx},{y+sy}\"/>" + "\n")
		elif feature == 3: # Line
			y1 = start*coordinates[chrm]["ht"]/chromSizes[chrm]
			y2 = stop*coordinates[chrm]["ht"]/chromSizes[chrm]
			y  = (y1+y2)/2
			y += coordinates[chrm]["cy"]
			miter = size*50
			if chrCopy == 1:
				x1 = coordinates[chrm]["cx"] - coordinates[chrm]["wd"]/2
				x2 = coordinates[chrm]["cx"]
				svg_fh.write(f"<line fill=\"none\" stroke=\"{col}\" stroke-miterlimit=\"10\" x1=\"{x1}\" y1=\"{y}\" x2=\"{x2}\" y2=\"{y}\"/>" + "\n")
			else:
				x1 = coordinates[chrm]["cx"]
				x2 = coordinates[chrm]["cx"] + coordinates[chrm]["wd"]/2
				svg_fh.write(f"<line fill=\"none\" stroke=\"{col}\" stroke-miterlimit=\"10\" x1=\"{x1}\" y1=\"{y}\" x2=\"{x2}\" y2=\"{y}\"/>" + "\n")
		else:
			print(f"Feature type, {feature}, unclear.  Please use either 0, 1, 2 or 3.  Skipping...")
			continue
	svg_fh.write("</svg>")
	print(f"\033[92mSuccessfully created SVG\033[0m")


if __name__ == "__main__":
	parser = ArgumentParser(prog="daVinci.py",
							add_help=True,
							description='''
							da Vinci: a utility for illustrating human chromosomes
							''',
							formatter_class=lambda prog: HelpFormatter(prog, width=120, max_help_position=120))

	parser.add_argument('--version', action='version',
						help='Print the software version.',
						version='da Vinci (version {})'.format(VERSION))

	# Input arguments
	parser.add_argument('--input', required=True, default=None, metavar='<input.bed>',
							help='Input BED-like file')
	parser.add_argument('--prefix', required=False, default="out", metavar='[output file prefix]',
							help='Output prefix [Default: "out"]')
	opts, unknown_args = parser.parse_known_args()
	if unknown_args:
		print("Unknown arguments were supplied: {}".format(' '.join(unknown_args)))
	print(f"\033[94mDrawing SVG using {opts.input}\033[0m")
	print(f"\033[94mSaving to {opts.prefix}.svg\033[0m")
	draw(opts)
	print(f"\033[94mConverting to PNG...\033[0m")
	try:
		subprocess.check_output(f"rsvg {opts.prefix}.svg {opts.prefix}.png", shell=True)
	except subprocess.CalledProcessError as e:
		print(f"\033[91mFailed SVG to PNG conversion...\033[0m")
		raise e
	finally:
		print(f"\033[92mSuccessfully converted SVG to PNG\033[0m")




