# from PIL import Image


# def is_grayscale(rgb, tolerance=30):
#     """주어진 픽셀이 무채색인지 확인합니다."""
#     r, g, b = rgb
#     return max(r, g, b) - min(r, g, b) <= tolerance


# def remove_colored_pixels(image_path, output_path, tolerance=30):
#     """
#     무채색을 제외한 모든 색상을 제거합니다.

#     :param image_path: 입력 이미지의 경로입니다.
#     :param output_path: 출력 이미지를 저장할 경로입니다.
#     :param tolerance: 무채색으로 간주되는 RGB 성분 간의 최대 차이입니다.
#     """
#     # 이미지를 불러옵니다
#     with Image.open(image_path) as img:
#         # 이미지를 RGB로 변환합니다(그레이스케일도 지원합니다)
#         rgb_img = img.convert("RGB")

#         # 이미지의 크기를 가져옵니다
#         width, height = rgb_img.size

#         # 모든 픽셀을 처리합니다
#         for x in range(width):
#             for y in range(height):
#                 # 픽셀의 RGB 색상을 가져옵니다
#                 rgb = rgb_img.getpixel((x, y))

#                 # 픽셀이 무채색이 아닌 경우, 흰색으로 변경합니다
#                 if not is_grayscale(rgb, tolerance):
#                     rgb_img.putpixel((x, y), (255, 255, 255))

#         # 수정된 이미지를 저장합니다
#         rgb_img.save(output_path)


# # 함수를 테스트합니다
# remove_colored_pixels(
#     "Test\KakaoTalk_20231006_150844552.jpg", "output_image.png", tolerance=30
# )


# import cv2
# import numpy as np


# def black_and_white_image(image_path, output_path):
#     # 이미지를 읽는다
#     img = cv2.imread(image_path)

#     # BGR 범위를 정의하여 검은색만 선택한다
#     lower_bound = np.array([0, 0, 0], dtype=np.uint8)
#     upper_bound = np.array([50, 50, 50], dtype=np.uint8)

#     # 마스크를 생성한다
#     mask = cv2.inRange(img, lower_bound, upper_bound)
#     inverse_mask = cv2.bitwise_not(mask)

#     # 마스크를 사용하여 이미지의 검은색 부분만 가져온다
#     black_part = cv2.bitwise_and(img, img, mask=mask)

#     # 나머지 부분을 흰색으로 채운다
#     white_img = np.ones_like(img) * 255
#     white_part = cv2.bitwise_and(white_img, white_img, mask=inverse_mask)

#     # 두 부분을 합친다
#     result = cv2.add(black_part, white_part)

#     # 결과를 저장한다
#     cv2.imwrite(output_path, result)


# # 함수를 호출한다
# image_path = "Test\KakaoTalk_20231006_150844552.jpg"
# output_path = "output_image.jpg"
# black_and_white_image(image_path, output_path)


from PIL import Image
import os


def convert_to_black_and_white(input_image_path, output_image_path):
    # 이미지 열기
    with Image.open(input_image_path) as color_image:
        # 흑백으로 변환
        bw_image = color_image.convert("L")
        # 변환된 이미지 저장
        bw_image.save(output_image_path)
        print(
            f"The image has been successfully converted and saved as '{output_image_path}'"
        )


# 사용 예:
input_path = "Test\그림1.jpg"  # 원본 컬러 이미지 경로
output_path = "school.jpg"  # 흑백 이미지를 저장할 경로

# 함수 실행
convert_to_black_and_white(input_path, output_path)
