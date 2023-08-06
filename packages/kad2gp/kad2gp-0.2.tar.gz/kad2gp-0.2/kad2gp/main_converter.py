import argparse
import sys
from typing import List

from kad2gp.converter import convert_kad_number


def parse_args(argv: List[str]):
    parser = argparse.ArgumentParser(
        description="A python3 script to get queues lengths from mail's dinner room")
    parser.add_argument(
        '-k', '--kad-number', type=str, required=True,
        help='Kadastr number from http://pkk.rosreestr.ru')
    parser.add_argument(
        '-d', '--target-directory', type=str, required=False,
        help='Target directory to save file (default is current)')
    parser.add_argument(
        '-f', '--file-name', type=str, required=False,
        help='File name (default is kad_<number_>)')
    parser.add_argument(
        '-m', '--media-path', type=str, required=False,
        help='Temporary files (default is ~/.kad2gp/)')
    parser.add_argument(
        '-e', '--epsilon', type=int, required=False,
        help='Prrecision of approximation (1 - the strogest, default is 5)')
    parser.add_argument(
        '-s', '--save-plot', action='store_true', required=False,
        help='Save the plot of the map (default false)')
    parser.add_argument(
        '-q', '--quiet', action='store_true', required=False,
        help='Do not print extrra information into console (default false)')
    return parser.parse_args(argv[1:])


def main():
    prms = parse_args(sys.argv)
    convert_kad_number(
        kad_number=prms.kad_number,
        target_directory=prms.target_directory,
        file_name=prms.file_name,
        media_path=prms.media_path,
        epsilon=prms.epsilon,
        save_plot=prms.save_plot,
        quiet=prms.quiet,
    )
