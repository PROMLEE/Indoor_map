import cv2
import numpy as np
import json

# JSON 파일 경로
json_file_path = "data.json"

# JSON 파일에서 데이터 읽기
with open(json_file_path, "r") as file:
    data = json.load(file)

# 마스크 이미지의 크기 설정
height, width = 512, 512  # 실제 이미지 크기에 맞게 조정해야 합니다.
mask = np.zeros((height, width), dtype=np.uint8)

# JSON 파일의 데이터를 사용하여 각 픽셀 위치에 점 찍기
for group in data["EdgeData"]:
    for pixel in group["pixels"]:
        x, y = pixel["x"], pixel["y"]
        mask[y, x] = 255

# 마스크 이미지 저장
mask_file_path = "edge.png"
cv2.imwrite(mask_file_path, mask)
