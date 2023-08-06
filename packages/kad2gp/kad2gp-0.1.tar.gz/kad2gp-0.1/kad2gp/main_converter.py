import argparse
import logging
import os
import sys
from typing import List

import cv2

from kad2gp.logger import logger
from kad2gp.tools import load_area, make_path, make_gpl_content, init_logger


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
        '-e', '--epsilon', type=int, default=5, required=False,
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

    init_logger()

    if prms.quiet is not True:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # Делаем запрос
    area = load_area(
        kad_number=prms.kad_number,
        media_path=prms.media_path or os.path.expanduser('~/.kad2gp/'),
        epsilon=prms.epsilon,
        with_log=prms.quiet is not True)

    # Берем данные
    coord_raw = area.get_image_geometry()
    coord_geo: List[List[float]] = coord_raw[0][0]

    coord_raw = area.get_image_xy_corner()
    coord: List[List[float]] = coord_raw[0][0]

    # Calculate Garden Planner's coordinates
    coords_in_meters = make_path(
        size=(area.width, area.height),
        coord_img=coord,
        coord_geo=coord_geo)

    # Путь, куда сохранить картинку
    target_directory = prms.target_directory or '.'
    target_name = "kad_" + prms.kad_number.replace(':', '_')
    target_path = os.path.join(target_directory, target_name)

    # Сохраняем картинку
    gml_path = target_path + ".gml"
    logger.debug(f"Saving data to \"{gml_path}\"...")
    gpl_content = make_gpl_content(prms.kad_number, coords_in_meters)
    with open(gml_path, 'wt') as fp:
        fp.write(gpl_content)

    # Если нужно, то сохраняем и картинку
    if prms.save_plot:
        image_path = target_path + ".png"
        logger.debug(f"Saving image to \"{image_path}\"...")
        img = cv2.imread(area.image_path)
        for polygones in area.image_xy_corner:
            for corners in polygones:
                for x, y in corners:
                    cv2.circle(img, (x, y), 3, 255, -1)
        cv2.imwrite(image_path, img)
