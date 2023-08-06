import logging
import os
from typing import List

import cv2

from kad2gp.logger import logger
from kad2gp.tools import load_area, make_path, make_gpl_content, init_logger


def convert_kad_number(
        kad_number: str,
        target_directory: str = None,
        file_name: str = None,
        media_path: str = None,
        epsilon: int = None,
        save_plot: bool = None,
        quiet: bool = None
):
    init_logger()

    if quiet is not True:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # Делаем запрос
    area = load_area(
        kad_number=kad_number,
        media_path=os.path.expanduser(media_path or "~/.kad2gp/"),
        epsilon=epsilon or 5,
        with_log=quiet is not True)

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
    target_directory = os.path.expanduser(target_directory or ".")
    target_name = file_name or ("kad_" + kad_number.replace(':', '_'))
    target_path = os.path.join(target_directory, target_name)

    # Сохраняем картинку
    gml_path = target_path + ".gml"
    logger.debug(f"Saving data to \"{gml_path}\"...")
    gpl_content = make_gpl_content(kad_number, coords_in_meters)
    with open(gml_path, 'wt') as fp:
        fp.write(gpl_content)

    # Если нужно, то сохраняем и картинку
    if save_plot:
        image_path = target_path + ".png"
        logger.debug(f"Saving image to \"{image_path}\"...")
        img = cv2.imread(area.image_path)
        for polygones in area.image_xy_corner:
            for corners in polygones:
                for x, y in corners:
                    cv2.circle(img, (x, y), 3, 255, -1)
        cv2.imwrite(image_path, img)
