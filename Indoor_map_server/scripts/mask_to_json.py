import os
import cv2
import numpy as np
import math
import json
from PIL import ImageFont, ImageDraw, Image, ExifTags
from scripts.firebase import put_firebase


def myPutText(src, text, pos, font_size, font_color):
    img_pil = Image.fromarray(src)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype("./scripts/MaruBuri.ttf", font_size)
    draw.text(pos, text, font=font, fill=font_color)
    return np.array(img_pil)


def to_mask(buildingname):
    inputurl = f"result/{buildingname[:-3]}/data/{buildingname}.json"
    outputurl = f"result/{buildingname[:-3]}/mask"
    if not os.path.exists(outputurl):
        os.makedirs(outputurl, exist_ok=True)
    floor = buildingname[-2:]
    with open(inputurl, "r") as file:
        data = json.load(file)
    height, width = 1024, 1024
    mask = np.zeros((height, width, 3), dtype=np.uint8)
    mask = myPutText(
        mask,
        buildingname[:-3] + " 건물 " + str(floor) + " 층입니다",
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
    cv2.imwrite(outputurl + f"/{buildingname}.png", mask)


def is_grayscale(rgb):
    r, g, b = rgb
    return max(r, g, b) - min(r, g, b) <= 30


def rotate_image_based_on_exif(img):
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == "Orientation":
            break
    exif = img._getexif()

    if exif is not None:
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    return img


def remove_colored_pixels(buildingname):
    inputurl = f"sources/{buildingname[:-3]}/images/{buildingname}.png"
    outputurl = f"sources/{buildingname[:-3]}/gray"
    if not os.path.exists(outputurl):
        os.makedirs(outputurl, exist_ok=True)
    with Image.open(inputurl) as img:
        img = rotate_image_based_on_exif(img)
        rgb_img = img.convert("RGB")
        width, height = rgb_img.size
        for x in range(width):
            for y in range(height):
                rgb = rgb_img.getpixel((x, y))
                if not is_grayscale(rgb):
                    rgb_img.putpixel((x, y), (255, 255, 255))
        rgb_img.save(outputurl + f"/{buildingname}.png")


def size_convert(buildingname):
    inputurl = f"sources/{buildingname[:-3]}/masks/{buildingname}.png"
    # 해당 경로의 파일 리스트 가져오기
    image = cv2.imread(inputurl)
    image = cv2.resize(image, (1024, 1024), interpolation=cv2.INTER_AREA)
    cv2.imwrite(inputurl, image)


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


# for f in file_list:
def mask_to_json(buildingname):
    inputurl = f"sources/{buildingname[:-3]}/masks/{buildingname}.png"
    outputurl = f"result/{buildingname[:-3]}/data"
    if not os.path.exists(outputurl):
        os.makedirs(outputurl, exist_ok=True)
    mask = cv2.imread(inputurl, cv2.IMREAD_COLOR)
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
    # cv2.imwrite(os.path.join("result\CAU310\etc", result_name + ".png"), new_mask)

    # JSON 파일로 저장할 데이터 생성
    edge_data = []
    dict = {}
    for id, pixels in components.items():
        if id not in [-2, 1]:
            dict[str(id)] = f"{id}"
        edge_data.append(
            {
                "id": id,
                "caption": f"{id}",
                "pixels": pixels,
                "move_up": 0,
                "move_down": 0,
            }
        )
    put_firebase(buildingname, dict)
    # JSON 파일로 저장
    with open(os.path.join(outputurl, buildingname + ".json"), "w") as file:
        json.dump(edge_data, file, indent=4)


if __name__ == "__main__":
    # remove_colored_pixels("동훈궁_01")
    # size_convert("동훈궁_01")
    # mask_to_json("동훈궁_01")
    to_mask("동훈궁_01")
