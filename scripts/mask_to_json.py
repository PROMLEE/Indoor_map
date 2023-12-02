import os
import cv2
import numpy as np
import math
import json


def is_boundary_pixel(x, y, mask, height, width):
    if x == 0 or x == width - 1 or y == 0 or y == height - 1:
        return True

    neighbors = [
        mask[y - 1, x - 1],
        mask[y - 1, x],
        mask[y - 1, x + 1],
        mask[y, x - 1],
        mask[y, x + 1],
        mask[y + 1, x - 1],
        mask[y + 1, x],
        mask[y + 1, x + 1],
    ]

    return not all(np.array_equal(val, white) for val in neighbors)


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def is_within_distance(point1, point2, max_distance):
    return (
        calculate_distance(point1[0], point1[1], point2[0], point2[1]) <= max_distance
    )


def get_diagonal_neighbors(x, y, labels, current_label):
    neighbors = []
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and labels[ny, nx] != current_label:
                neighbors.append((nx, ny))
    return neighbors


def draw_line(img, start, end, components):
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        img[y0, x0] = [0, 255, 0]
        components.setdefault(-2, []).append({"x": int(x0), "y": int(y0)})
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        elif e2 <= dx:
            err += dx
            y0 += sy


blue = np.array([255, 0, 0])
white = np.array([255, 255, 255])
# 이미지 불러오기
building_name = "CAU310"
mask_file_path = os.path.join("sources", building_name, "masks")
# file_list = [
#     f
#     for f in os.listdir(mask_file_path)
#     if os.path.isfile(os.path.join(mask_file_path, f))
# ]
json_file_path = os.path.join("result", building_name, "etc")
if not os.path.exists(json_file_path):
    os.makedirs(json_file_path, exist_ok=True)
# print(file_list)
file_list = [
    "CAU310_01.png",
]
for f in file_list:
    result_name = f.replace(".png", "")
    f_url = os.path.join(mask_file_path, f)
    mask = cv2.imread(f_url, cv2.IMREAD_COLOR)
    height, width = mask.shape[0:2]

    new_mask = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            if np.array_equal(mask[y, x], white) and is_boundary_pixel(
                x, y, mask, height, width
            ):
                new_mask[y, x] = 255
            elif np.array_equal(mask[y, x], blue):
                new_mask[y, x] = 255

    # 연결된 구성 요소 찾기
    num_labels, labels = cv2.connectedComponents(new_mask)

    # 새로운 마스크 준비
    new_mask = np.zeros((height, width, 3), dtype=np.uint8)

    # 각 구성 요소의 외곽선 찾기
    contours = {}
    for label in range(1, num_labels):
        component_mask = np.uint8(labels == label)
        contour, _ = cv2.findContours(
            component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours[label] = contour[0]

    components = {}
    # 외곽선 픽셀 간 거리 계산 및 채색
    max_distance = 15
    for label1 in contours:
        for label2 in contours:
            k = True
            if label1 != label2:
                for point1 in contours[label1]:
                    if k:
                        for point2 in contours[label2]:
                            if is_within_distance(point1[0], point2[0], max_distance):
                                draw_line(new_mask, point1[0], point2[0], components)
                                k = False
                                break

    # 원래 구성 요소 색상 적용
    for y in range(height):
        for x in range(width):
            label = labels[y, x]
            if label > 0:
                new_mask[y, x] = [255, 255, 255]  # 흰색으로 적용
                components.setdefault(int(label), []).append({"x": int(x), "y": int(y)})

    # 이미지 저장
    cv2.imwrite(os.path.join("result\CAU310\etc", result_name + ".png"), new_mask)

    # JSON 파일로 저장할 데이터 생성
    edge_data = []
    for id, pixels in components.items():
        edge_data.append(
            {
                "id": id,
                "caption": f"{id}",
                "pixels": pixels,
                "move_up": 0,
                "move_down": 0,
            }
        )

    # JSON 파일로 저장
    with open(os.path.join(json_file_path, result_name + ".json"), "w") as file:
        json.dump(edge_data, file, indent=4)
