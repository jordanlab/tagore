#!/usr/bin/env python3
"""
tagore: a utility for illustrating human chromosomes
https://github.com/jordanlab/tagore
"""
__author__ = ["Lavanya Rishishar", "Aroon Chande"]
__copyright__ = "Copyright 2019, Applied Bioinformatics Lab"
__license__ = "GPLv3"

import os
import pickle
import pkgutil
import re
import shutil
import subprocess
import sys
from argparse import ArgumentParser, HelpFormatter

VERSION = "1.1.2"

COORDINATES = {
    "1": {"cx": 128.6, "cy": 1.5, "ht": 1654.5, "width": 118.6},
    "2": {"cx": 301.4, "cy": 43.6, "ht": 1612.4, "width": 118.6},
    "3": {"cx": 477.6, "cy": 341.4, "ht": 1314.7, "width": 118.6},
    "4": {"cx": 655.6, "cy": 517.9, "ht": 1138.1, "width": 118.6},
    "5": {"cx": 835.4, "cy": 461, "ht": 1195.1, "width": 118.6},
    "6": {"cx": 1012.4, "cy": 524.2, "ht": 1131.8, "width": 118.6},
    "7": {"cx": 1198.2, "cy": 608.5, "ht": 1047.5, "width": 118.6},
    "8": {"cx": 1372.9, "cy": 692.8, "ht": 963.2, "width": 118.6},
    "9": {"cx": 1554.5, "cy": 724.4, "ht": 931.6, "width": 118.6},
    "10": {"cx": 1733.8, "cy": 766.6, "ht": 889.4, "width": 118.6},
    "11": {"cx": 1911.5, "cy": 766.6, "ht": 889.4, "width": 118.6},
    "12": {"cx": 2095.6, "cy": 769.7, "ht": 886.3, "width": 118.6},
    "13": {"cx": 129.3, "cy": 2068.8, "ht": 766.1, "width": 118.6},
    "14": {"cx": 301.6, "cy": 2121.5, "ht": 713.4, "width": 118.6},
    "15": {"cx": 477.5, "cy": 2153.1, "ht": 681.8, "width": 118.6},
    "16": {"cx": 656.7, "cy": 2232.2, "ht": 602.8, "width": 118.6},
    "17": {"cx": 841.2, "cy": 2290.7, "ht": 544.3, "width": 118.6},
    "18": {"cx": 1015.7, "cy": 2313.9, "ht": 521.1, "width": 118.6},
    "19": {"cx": 1199.5, "cy": 2437.2, "ht": 397.8, "width": 118.6},
    "20": {"cx": 1374.4, "cy": 2416.1, "ht": 418.9, "width": 118.6},
    "21": {"cx": 1553, "cy": 2510.9, "ht": 324.1, "width": 118.6},
    "22": {"cx": 1736.9, "cy": 2489.8, "ht": 345.1, "width": 118.6},
    "X": {"cx": 1915.7, "cy": 1799.21, "ht": 1035.4, "width": 118.6},
    "Y": {"cx": 2120.9, "cy": 2451.6, "ht": 382.7, "width": 118.6},
}

CHROM_SIZES = {
    "hg37": {
        "1": 249250621,
        "2": 243199373,
        "3": 198022430,
        "4": 191154276,
        "5": 180915260,
        "6": 171115067,
        "7": 159138663,
        "8": 146364022,
        "9": 141213431,
        "10": 135534747,
        "11": 135006516,
        "12": 133851895,
        "13": 115169878,
        "14": 107349540,
        "15": 102531392,
        "16": 90354753,
        "17": 81195210,
        "18": 78077248,
        "19": 59128983,
        "20": 63025520,
        "21": 48129895,
        "22": 51304566,
        "X": 155270560,
        "Y": 59373566,
    },
    "hg38": {
        "1": 248956422,
        "2": 242193529,
        "3": 198295559,
        "4": 190214555,
        "5": 181538259,
        "6": 170805979,
        "7": 159345973,
        "8": 145138636,
        "9": 138394717,
        "10": 133797422,
        "11": 135086622,
        "12": 133275309,
        "13": 114364328,
        "14": 107043718,
        "15": 101991189,
        "16": 90338345,
        "17": 83257441,
        "18": 80373285,
        "19": 58617616,
        "20": 64444167,
        "21": 46709983,
        "22": 50818468,
        "X": 156040895,
        "Y": 57227415,
    },
}


def printif(statement, condition):
    """
    Print statements if a boolean (e.g. verbose) is true
    """
    if condition:
        print(statement)


def draw(arguments, svg_header, svg_footer):
    """
    Create the SVG object
    """
    polygons = ""
    try:
        input_fh = open(arguments.input, "r")
    except (IOError, EOFError) as input_fh_e:
        print("Error opening input file!")
        raise input_fh_e
    svg_fn = f"{arguments.prefix}.svg"
    try:
        svg_fh = open(svg_fn, "w")
        svg_fh.write(svg_header)
    except (IOError, EOFError) as svg_fh_e:
        print("Error opening output file!")
        raise svg_fh_e
    line_num = 1
    for entry in input_fh:
        if entry.startswith("#"):
            continue
        entry = entry.rstrip().split("\t")
        if len(entry) != 7:
            print(f"Line number {line_num} does not have 7 columns")
            sys.exit()
        chrm, start, stop, feature, size, col, chrcopy = entry
        chrm = chrm.replace("chr", "")
        start = int(start)
        stop = int(stop)
        size = float(size)
        feature = int(feature)
        chrcopy = int(chrcopy)
        if 0 > size > 1:
            print(
                f"Feature size, {size},on line {line_num} unclear. \
                Please bound the size between 0 (0%) to 1 (100%). Defaulting to 1."
            )
            size = 1
        if not re.match("^#.{6}", col):
            print(
                f"Feature color, {col}, on line {line_num} unclear. \
                Please define the color in hex starting with #. Defaulting to #000000."
            )
            col = "#000000"
        if chrcopy not in [1, 2]:
            print(
                f"Feature chromosome copy, {chrcopy}, on line {line_num}\
             unclear. Skipping..."
            )
            line_num = line_num + 1
            continue
        line_num = line_num + 1
        if feature == 0:  # Rectangle
            feat_start = (
                start * COORDINATES[chrm]["ht"] / CHROM_SIZES[arguments.build][chrm]
            )
            feat_end = (
                stop * COORDINATES[chrm]["ht"] / CHROM_SIZES[arguments.build][chrm]
            )
            width = COORDINATES[chrm]["width"] * size / 2
            if chrcopy == 1:
                x_pos = COORDINATES[chrm]["cx"] - width
            else:
                x_pos = COORDINATES[chrm]["cx"]
            y_pos = COORDINATES[chrm]["cy"] + feat_start
            height = feat_end - feat_start
            svg_fh.write(
                f'<rect x="{x_pos}" y="{y_pos}" fill="{col}" width="{width}"\
             height="{height}"/>'
                + "\n"
            )
        elif feature == 1:  # Circle
            feat_start = (
                start * COORDINATES[chrm]["ht"] / CHROM_SIZES[arguments.build][chrm]
            )
            feat_end = (
                stop * COORDINATES[chrm]["ht"] / CHROM_SIZES[arguments.build][chrm]
            )
            radius = COORDINATES[chrm]["width"] * size / 4
            if chrcopy == 1:
                x_pos = COORDINATES[chrm]["cx"] - COORDINATES[chrm]["width"] / 4
            else:
                x_pos = COORDINATES[chrm]["cx"] + COORDINATES[chrm]["width"] / 4
            y_pos = COORDINATES[chrm]["cy"] + (feat_start + feat_end) / 2
            svg_fh.write(
                f'<circle fill="{col}" cx="{x_pos}" cy="{y_pos}"\
             r="{radius}"/>'
                + "\n"
            )
        elif feature == 2:  # Triangle
            feat_start = (
                start * COORDINATES[chrm]["ht"] / CHROM_SIZES[arguments.build][chrm]
            )
            feat_end = (
                stop * COORDINATES[chrm]["ht"] / CHROM_SIZES[arguments.build][chrm]
            )
            if chrcopy == 1:
                x_pos = COORDINATES[chrm]["cx"] - COORDINATES[chrm]["width"] / 2
                sx_pos = 38.2 * size
            else:
                x_pos = COORDINATES[chrm]["cx"] + COORDINATES[chrm]["width"] / 2
                sx_pos = -38.2 * size
            y_pos = COORDINATES[chrm]["cy"] + (feat_start + feat_end) / 2
            sy_pos = 21.5 * size
            polygons += (
                f'<polygon fill="{col}" points="{x_pos-sx_pos},{y_pos-sy_pos} \
            {x_pos},{y_pos} {x_pos-sx_pos},{y_pos+sy_pos}"/>'
                + "\n"
            )
        elif feature == 3:  # Line
            y_pos1 = (
                start * COORDINATES[chrm]["ht"] / CHROM_SIZES[arguments.build][chrm]
            )
            y_pos2 = stop * COORDINATES[chrm]["ht"] / CHROM_SIZES[arguments.build][chrm]
            y_pos = (y_pos1 + y_pos2) / 2
            y_pos += COORDINATES[chrm]["cy"]
            if chrcopy == 1:
                x_pos1 = COORDINATES[chrm]["cx"] - COORDINATES[chrm]["width"] / 2
                x_pos2 = COORDINATES[chrm]["cx"]
                svg_fh.write(
                    f'<line fill="none" stroke="{col}" stroke-miterlimit="10" \
                    x1="{x_pos1}" y1="{y_pos}" x2="{x_pos2}" y2="{y_pos}"/>'
                    + "\n"
                )
            else:
                x_pos1 = COORDINATES[chrm]["cx"]
                x_pos2 = COORDINATES[chrm]["cx"] + COORDINATES[chrm]["width"] / 2
                svg_fh.write(
                    f'<line fill="none" stroke="{col}" stroke-miterlimit="10" \
                    x1="{x_pos1}" y1="{y_pos}" x2="{x_pos2}" y2="{y_pos}"/>'
                    + "\n"
                )
        else:
            print(
                f"Feature type, {feature}, unclear. Please use either 0, 1, 2 or 3. Skipping..."
            )
            continue
    svg_fh.write(svg_footer)
    svg_fh.write(polygons)
    svg_fh.write("</svg>")
    svg_fh.close()
    printif(f"\033[92mSuccessfully created SVG\033[0m", arguments.verbose)


def run():
    parser = ArgumentParser(
        prog="tagore",
        add_help=True,
        description="""
                            tagore: a utility for illustrating human chromosomes
                            https://github.com/jordanlab/tagore
                            """,
        formatter_class=lambda prog: HelpFormatter(
            prog, width=120, max_help_position=120
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        help="Print the software version",
        version="tagore (version {})".format(VERSION),
    )

    # Input arguments
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        default=None,
        metavar="<input.bed>",
        help="Input BED-like file",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        required=False,
        default="out",
        metavar="[output file prefix]",
        help='Output prefix [Default: "out"]',
    )
    parser.add_argument(
        "-b",
        "--build",
        required=False,
        default="hg38",
        metavar="[hg78/hg38]",
        help="Human genome build to use [Default: hg38]",
    )
    parser.add_argument(
        "-f",
        "--force",
        required=False,
        default=False,
        help="Overwrite output files if they exist already",
        action="store_true",
    )
    parser.add_argument(
        "-ofmt",
        "--oformat",
        required=False,
        default="png",
        help="Output format for conversion (pdf requires rsvg-convert)",
        metavar="[png/pdf]",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        default=False,
        help="Display verbose output",
        action="store_true",
    )
    parsed_args, unknown_args = parser.parse_known_args()
    if unknown_args:
        print(
            f"\033[93mOne or more unknown arguments were supplied:\033[0m {' '.join(unknown_args)}\n"
        )
        parser.print_help()
        sys.exit()
    if parsed_args.build not in ["hg37", "hg38"]:
        print(
            f"\033[91mBuild must be either 'hg37' or 'hg38', you supplied {parsed_args.build}.\033[0m"
        )
        sys.exit()

    if shutil.which("rsvg-convert", mode=os.X_OK) is None:
        if shutil.which("rsvg", mode=os.X_OK) is None:
            print(f"\033[91mCould not find `rsvg` or `rsvg-convert` in PATH.\033[0m")
            sys.exit()
        else:
            is_rsvg_installed = True
            if parsed_args.oformat != "png":
                print(f"\033[93m`rsvg` only supports PNG output, using png\033[0m")
                parsed_args.oformat = "png"
    else:
        is_rsvg_installed = False
        if parsed_args.oformat not in ["png", "pdf"]:
            print(f"\033[93m{parsed_args.oformat} is not PNG or PDF, using PNG\033[0m")
            parsed_args.oformat = "png"
    svg_pkl_data = pkgutil.get_data("tagore", "base.svg.p")
    svg_header, svg_footer = pickle.loads(svg_pkl_data)
    printif(
        f"\033[94mDrawing chromosome ideogram using {parsed_args.input}\033[0m",
        parsed_args.verbose,
    )
    if os.path.exists(f"{parsed_args.prefix}.svg") and parsed_args.force is False:
        print(f"\033[93m'{parsed_args.prefix}.svg' already exists.\033[0m")
        OW = input(f"Overwrite {parsed_args.prefix}.svg? [Y/n]: ") or "y"
        if OW.lower() != "y":
            print(f"\033[93m'tagore will now exit...\033[0m")
            sys.exit()
        else:
            print(
                f"\033[94mOverwriting existing file and saving to: {parsed_args.prefix}.svg\033[0m"
            )
    else:
        printif(
            f"\033[94mSaving to: {parsed_args.prefix}.svg\033[0m", parsed_args.verbose
        )
    draw(parsed_args, svg_header, svg_footer)
    printif(
        f"\033[94mConverting {parsed_args.prefix}.svg -> {parsed_args.prefix}.{parsed_args.oformat} \033[0m",
        parsed_args.verbose,
    )
    try:
        if is_rsvg_installed:
            subprocess.check_output(
                f"rsvg {parsed_args.prefix}.svg {parsed_args.prefix}.{parsed_args.oformat} ",
                shell=True,
            )
        else:
            subprocess.check_output(
                f"rsvg-convert -o {parsed_args.prefix}.{parsed_args.oformat} -f {parsed_args.oformat} {parsed_args.prefix}.svg ",
                shell=True,
            )
    except subprocess.CalledProcessError as rsvg_e:
        printif(f"\033[91mFailed SVG to PNG conversion...\033[0m", parsed_args.verbose)
        raise rsvg_e
    finally:
        printif(
            f"\033[92mSuccessfully converted SVG to {parsed_args.oformat.upper()}\033[0m",
            parsed_args.verbose,
        )
