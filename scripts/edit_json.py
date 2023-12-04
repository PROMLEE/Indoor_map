import json
import os
import cv2
import numpy as np

from PIL import ImageFont, ImageDraw, Image


def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def update_caption(newdata, buildingname):
    file_path = f"result/{buildingname[:-3]}/data/{buildingname}.json"
    data = load_json(file_path)
    newdata = newdata["newData"]
    for i in range(len(data)):
        if data[i]["id"] == newdata[i]["id"]:
            data[i]["caption"] = newdata[i]["caption"]
            data[i]["move_up"] = newdata[i]["move_up"]
            data[i]["move_down"] = newdata[i]["move_down"]
    save_json(file_path, data)
    return False


def myPutText(src, text, pos, font_size, font_color):
    img_pil = Image.fromarray(src)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype("./scripts/MaruBuri.ttf", font_size)
    draw.text(pos, text, font=font, fill=font_color)
    return np.array(img_pil)


def create_mask(buildingname):
    floor = buildingname[-2:]
    json_file_path = f"result/{buildingname[:-3]}/data/{buildingname}.json"
    mask_file_path = f"result/{buildingname[:-3]}/mask/{buildingname}.png"
    # JSON 파일에서 데이터 읽기
    with open(os.path.join(json_file_path), "r") as file:
        data = json.load(file)
    # JSON 파일의 데이터를 사용하여 각 픽셀 위치에 점 찍기
    height, width = 1024, 1024
    mask = np.zeros((height, width, 3), dtype=np.uint8)
    mask = myPutText(
        mask,
        f"{buildingname[:-3]}건물 {floor} 층입니다",
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
    cv2.imwrite(mask_file_path, mask)


def update_move_up(data, id):
    new_caption = int(input("위층 객체(엘리베이터, 계단)의 id를 입력하세요(없으면 0): "))
    for item in data:
        if item["id"] == id:
            item["move_up"] = new_caption
            return True
    return False


def update_move_down(data, id):
    new_caption = int(input("아래층 객체(엘리베이터, 계단)의 id를 입력하세요(없으면 0): "))
    for item in data:
        if item["id"] == id:
            item["move_down"] = new_caption
            return True
    return False


# building_name = "CAU310"
# json_file_path = os.path.join("result", building_name, "data")
# file_list = [
#     f
#     for f in os.listdir(json_file_path)
#     if os.path.isfile(os.path.join(json_file_path, f))
# ]

# while True:
#     # for i in range(len(file_list)):
#     #     print(i + 1, "번 파일: ", file_list[i])
#     # print()
#     # floor = int(input("수정할 파일의 번호를 선택하세요(종료시 0을 입력하세요): "))
#     # if floor == 0:
#     #     break
#     # filename = os.path.join(json_file_path, file_list[floor - 1])
#     filename = os.path.join(json_file_path, file_list[3])
#     data = load_json(filename)

#     id_to_update = int(input("수정할 데이터의 ID를 입력하세요: "))
#     new_caption = input("새로운 캡션을 입력하세요: ")

#     if update_caption(data, id_to_update, new_caption):
#         if new_caption in ["엘리베이터", "계단", "elevator", "stair"]:
#             update_move_up(data, id_to_update)
#             update_move_down(data, id_to_update)
#         print("데이터가 성공적으로 업데이트되었습니다.")
#         save_json(filename, data)
#     else:
#         print("해당 ID를 가진 데이터를 찾을 수 없습니다.")
#     print("--------------------------------------------------------------\n")
# data = [{"id": 1, "caption": "dlkdll"}]
# newdata = [{"id": 1, "caption": "ddddd"}]
# update_caption(data, newdata)
# print(data)
# building_name = "CAU310_B4"
# create_mask(building_name)
