import logging
import math
from typing import List, Tuple

from rosreestr2coord import Area
from rosreestr2coord.logger import logger as rosreestr2coord_logger

from kad2gp.logger import logger


def init_logger():
    for handler in rosreestr2coord_logger.root.handlers[:]:
        rosreestr2coord_logger.root.removeHandler(handler)
    pil_logger = logging.getLogger('PIL')
    pil_logger.setLevel(logging.INFO)


def load_area(
        kad_number: str,
        media_path: str,
        epsilon: int,
        with_log: bool
) -> Area:
    logger.debug(f"Loading data for {kad_number}...")
    return Area(
        code=kad_number,
        epsilon=epsilon,
        media_path=media_path,
        with_log=with_log)


def geo_len(lat1, lon1, lat2, lon2):  # generally used geo measurement function
    r = 6378.137  # Radius of earth in km
    d_lat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    d_lon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(lat1 * math.pi / 180) * math.cos(
        lat2 * math.pi / 180) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = r * c
    return d * 1000  # meters


def pic_len(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# size: [width, height]
# coord: coordinates in image
# coord_geo: coordinates on the earth
def make_path(
        size: Tuple[float, float],
        coord_img: List[List[float]],
        coord_geo: List[List[float]]
) -> List[List[float]]:
    s = 0
    for i in range(len(coord_geo)):
        a = coord_geo[i]
        b = coord_geo[(i + 1) % len(coord_geo)]
        m_geo = geo_len(a[1], a[0], b[1], b[0])
        a = coord_img[i]
        b = coord_img[(i + 1) % len(coord_img)]
        m_pic = pic_len(a[0], a[1], b[0], b[1])
        k = m_geo / m_pic
        s += k
        logger.debug(f'{i:2}: {k:22.20} m/px = {m_geo:.5} m / {m_pic:.5} px')
    k_mean = s / len(coord_geo)
    logger.debug(f"Meters in 1 pixel: {k_mean}")
    logger.debug(f"Width & hheight of the image in meters: {size[0] * k_mean} m * {size[1] * k_mean} m")

    path: List[List[float]] = []
    logger.debug('Coordinates in meters:')
    for i in range(len(coord_img)):
        a = coord_img[i]
        a_map = [a[0] * k_mean, a[1] * k_mean]
        path.append(a_map)
        logger.debug(f"{i:2}: {a_map} m")
    return path


# title - заголовок
# path - точки границы участка с координатами в метрах: [[x1,y1], [x2,y2], ..., [xn,yn]]
def make_gpl_content(title: str, path: List[List[float]]) -> str:
    gp_meter = 400.0 / 9.0  # GPm - длина одного метра в макетах GardenPlanner
    count = len(path)  # Число вершин участка
    b_min = path[0].copy()  # Минимальный угол
    b_max = path[0].copy()  # Максимальный угол
    for p in path[1:]:
        if b_min[0] > p[0]: b_min[0] = p[0]
        if b_min[1] > p[1]: b_min[1] = p[1]
        if b_max[0] < p[0]: b_max[0] = p[0]
        if b_max[1] < p[1]: b_max[1] = p[1]
    # Ширина и высота объекта в метрах
    width = b_max[0] - b_min[0]
    height = b_max[1] - b_min[1]
    cx = width / 2
    cy = height / 2
    tool_array_x = []  # x-точки GP
    tool_array_y = []  # y-точки GP
    for p in path:
        tool_array_x.append((p[0] - b_min[0] - cx) * gp_meter)
        tool_array_y.append((p[1] - b_min[1] - cy) * gp_meter)
    tool_array_x.append(tool_array_x[0])
    tool_array_y.append(tool_array_y[0])
    tool_array_x = ','.join([f'{a}' for a in tool_array_x])
    tool_array_y = ','.join([f'{a}' for a in tool_array_y])

    return f'''
<gardenplan>
  <plan title="template" description="" gridSize="{gp_meter / 4}" gridWidth="{(width + 2) * gp_meter}" gridHeight="{(height + 2) * gp_meter}" gridScale="3" backgroundTexture="0" backgroundColour="16777215" shadowDirection="45" gridLinesOff="0" newGroupNum="0" measurementFontSize="12" platform="desktop" version="3.73"/>
  <objects>
    <item obType="tool" id="-1" x="{(cx + 1) * gp_meter}" y="{(cy + 1) * gp_meter}" width="{width * gp_meter}" height="{height * gp_meter}" heightVert="1" rotation="0" title="{title}" description="" currentFillColour="10140771" depth="0" depthType="0" groupNum="0" currentFlowerColour="-1" wPrec="2" lPrec="2" hPrec="2" locked="true" transparent="false" inReport="true" autoLabel="false" autoLabelx="10" autoLabely="40" noteRef="-1" followTerrain="true" data3d="0,0,0,0,0" plantType="ground" toolMode="line" toolNum="1" numTools="1" shapeType="0" toolStyle="0" distBetweenObjects="0" styleWidth="0" toolArrayX="{tool_array_x}" toolArrayY="{tool_array_y}" curveArrayX="{',' * count}" curveArrayY="{',' * count}" toolArrayH=""/>
  </objects>
  <notes/>
  <vegbed>
    <plantinglist/>
    <bedlayouts numberOfBeds="0" layoutIndexMax="0"/>
  </vegbed>
  <groupData>
    <groups/>
  </groupData>
</gardenplan>
'''.strip()
