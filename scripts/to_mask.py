import cv2
import numpy as np
import json
import os
from PIL import ImageFont, ImageDraw, Image


def myPutText(src, text, pos, font_size, font_color):
    img_pil = Image.fromarray(src)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype("./scripts/MaruBuri.ttf", font_size)
    draw.text(pos, text, font=font, fill=font_color)
    return np.array(img_pil)


url = "./result"
building_name = "CAU208"
way_file_path = os.path.join(url, building_name, "mask")
if not os.path.exists(way_file_path):
    os.makedirs(way_file_path, exist_ok=True)
# 파일명들을 나타내는 리스트
file_names = [
    f
    for f in os.listdir(os.path.join(url, building_name, "data"))
    if os.path.isfile(os.path.join(url, building_name, "data", f))
]
for file_name in file_names:
    floor = file_name[-7:-5]
    # JSON 파일에서 데이터 읽기
    with open(os.path.join(url, building_name, "data", file_name), "r") as file:
        data = json.load(file)

    # 마스크 이미지의 크기 설정
    mover = []
    board = [[0] * 1025 for _ in range(1025)]
    next = [[[0, 0] for _ in range(1025)] for _ in range(1025)]
    # JSON 파일의 데이터를 사용하여 각 픽셀 위치에 점 찍기
    height, width = 1024, 1024
    mask = np.zeros((height, width, 3), dtype=np.uint8)
    mask = myPutText(
        mask,
        building_name + " 건물 " + str(floor) + " 층입니다",
        (500, 20),
        30,
        (255, 0, 0),
    )
    for group in data:
        sum_x, sum_y, div = 0, 0, 0
        id = group["id"]
        caption = group["caption"]
        for pixel in group["pixels"]:
            x, y = pixel["x"], pixel["y"]
            if id != -2:
                mask[y, x] = 255
            sum_x += x
            sum_y += y
            div += 1
        if id != -2 and id != 1:
            mask = myPutText(
                mask,
                f"{str(id)}: {caption}",
                (sum_x // div - 15, sum_y // div - 15),
                15,
                (0, 255, 0),
            )
    mask_file_path = os.path.join(way_file_path, building_name + "_" + floor + ".png")
    cv2.imwrite(mask_file_path, mask)
