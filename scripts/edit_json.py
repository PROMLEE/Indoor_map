import json
import os


def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def update_caption( newdata, buildingname, floor):
    file_path=f"results/{buildingname}/data/{buildingname}_{floor}"
    data=load_json(file_path)
    for i in range(len(data)):
        if data[i]["id"] == newdata[i]["id"]:
            data[i]["caption"] = newdata[i]["caption"]
            return True
    save_json(file_path, newdata)
    return False


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


building_name = "CAU310"
json_file_path = os.path.join("result", building_name, "data")
file_list = [
    f
    for f in os.listdir(json_file_path)
    if os.path.isfile(os.path.join(json_file_path, f))
]

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
data = [{"id": 1, "caption": "dlkdll"}]
newdata = [{"id": 1, "caption": "ddddd"}]
update_caption(data, newdata)
print(data)
