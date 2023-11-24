import cv2
import os

# 폴더 경로 지정
folder_path = 'algorithm\sources'
building_name = "CAU310"
folder_path = os.path.join(folder_path, building_name, "masks")
# 해당 경로의 파일 리스트 가져오기
file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
for f in file_list:
  f_url = os.path.join(folder_path, f)
  image = cv2.imread(f_url)
  image = cv2.resize(image, (1024, 1024), interpolation=cv2.INTER_AREA)
  cv2.imwrite(f_url, image)
