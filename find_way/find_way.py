import cv2
import numpy as np
import json
import os
from queue import Queue
from PIL import ImageFont, ImageDraw, Image


def myPutText(src, text, pos, font_size, font_color):
    img_pil = Image.fromarray(src)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype("C:/Windows/Fonts/batang.ttc", font_size)
    draw.text(pos, text, font=font, fill=font_color)
    return np.array(img_pil)


startPoint, startfloor = 4, 5
endPoint, endfloor = 27, 2
semipoint = startPoint
is_back = 1
if startfloor > endfloor:
    is_back = -1
elev_or_stair = False
dx = [1, 0, -1, 0, 1, 1, -1, -1]
dy = [0, 1, 0, -1, 1, -1, 1, -1]
# JSON 파일들의 기본 경로
url = "result"
building_name = "CAU310"
way_file_path = os.path.join(url, building_name, "way")
if not os.path.exists(way_file_path):
    os.makedirs(way_file_path, exist_ok=True)
# 파일명들을 나타내는 리스트
file_names = [
    f
    for f in os.listdir(os.path.join(url, building_name, "data"))
    if os.path.isfile(os.path.join(url, building_name, "data", f))
]
# 파일 경로 생성 및 처리를 위한 for문
for floor in range(startfloor, endfloor + is_back, is_back):
    for filename in file_names:
        if floor == int(filename[-7:-5]):
            f = filename
            break
    print(f)
    # JSON 파일에서 데이터 읽기
    with open(os.path.join(url, building_name, "data", f), "r") as file:
        data = json.load(file)

    # 마스크 이미지의 크기 설정
    mover = []
    board = [[0] * 1025 for _ in range(1025)]
    next = [[[0, 0] for _ in range(1025)] for _ in range(1025)]
    # JSON 파일의 데이터를 사용하여 각 픽셀 위치에 점 찍기
    height, width = 1024, 1024
    mask = np.zeros((height, width, 3), dtype=np.uint8)
    mask = myPutText(
        mask, building_name + " 건물 " + str(floor) + " 층입니다", (500, 20), 30, (255, 0, 0)
    )
    for group in data:
        sum_x, sum_y, div = 0, 0, 0
        id = group["id"]
        caption = group["caption"]
        if elev_or_stair and caption == "엘리베이터":
            mover.append(id)
        elif not elev_or_stair and caption == "계단":
            mover.append(id)
        for pixel in group["pixels"]:
            x, y = pixel["x"], pixel["y"]
            if id != semipoint:
                board[y][x] = id
            if id != -2:
                mask[y, x] = 255
            sum_x += x
            sum_y += y
            div += 1
        if id != -2 and id != 1:
            mask = myPutText(
                mask, caption, (sum_x // div - 7, sum_y // div - 5), 11, (0, 255, 0)
            )
        if id == semipoint:
            st_Averx, st_Avery = sum_x // div, sum_y // div
    print(mover)
    print(st_Averx, st_Avery)
    Q = Queue()
    Q.put((st_Averx, st_Avery))
    board[st_Averx][st_Avery] = -1
    escape = True

    if floor != endfloor and floor != startfloor:
        for item in data:
            if item["id"] == semipoint:
                if is_back == 1:
                    semipoint = item["move_up"]
                    break
                else:
                    semipoint = item["move_down"]
                    break
        mask_file_path = os.path.join(
            way_file_path, building_name + "_{:02d}".format(floor) + ".png"
        )
        cv2.imwrite(mask_file_path, mask)
        continue
    while escape:
        cur = Q.get()
        for dir in range(8):
            if not escape:
                break
            nx = cur[0] + dx[dir]
            ny = cur[1] + dy[dir]
            # print(nx, ny)
            if (floor == endfloor and board[ny][nx] == endPoint) or (
                (floor == startfloor and board[ny][nx] in mover)
                and endfloor != startfloor
            ):
                endX, endY = nx, ny
                escape = False
                next[ny][nx] = (cur[0], cur[1])
                for item in data:
                    if item["id"] == board[ny][nx]:
                        if is_back == 1:
                            semipoint = item["move_up"]
                            escape = False
                            break
                        else:
                            semipoint = item["move_down"]
                            escape = False
                            break
                if floor == startfloor and startfloor != endfloor:
                    if is_back == 1:
                        mask = myPutText(
                            mask,
                            str(endfloor) + "층으로 올라가세요!",
                            (nx, ny),
                            15,
                            (0, 0, 225),
                        )
                    else:
                        mask = myPutText(
                            mask,
                            str(endfloor) + "층으로 내려가세요!",
                            (nx, ny),
                            15,
                            (0, 0, 225),
                        )
                else:
                    mask = myPutText(mask, "도착!!!", (nx, ny), 15, (0, 0, 225))
                break
            elif 0 < nx < 1024 and 0 < ny < 1024 and board[ny][nx] == 0:
                Q.put((nx, ny))
                next[ny][nx] = (cur[0], cur[1])
                board[ny][nx] = -1
    if floor == endfloor or floor == startfloor:
        path = []
        st = (endX, endY)
        while st != (st_Averx, st_Avery):
            path.append(st)
            mask[st[1], st[0]] = [0, 0, 255]
            for dir in range(8):
                nx = st[1] + dx[dir]
                ny = st[0] + dy[dir]
                mask[nx, ny] = [0, 0, 255]
            st = next[st[1]][st[0]]
        path.append(st)
        mask[st[1], st[0]] = [0, 0, 255]
    mask_file_path = os.path.join(
        way_file_path, building_name + "_{:02d}".format(floor) + ".png"
    )
    cv2.imwrite(mask_file_path, mask)
