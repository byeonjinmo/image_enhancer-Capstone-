import numpy as np
import cv2
from skimage.metrics import peak_signal_noise_ratio as psnr
import tkinter as tk
from tkinter import filedialog

def calculate_psnr(original_image_path, compressed_image_path):
    # 원본 및 압축된 이미지 로드 (그레이스케일로)
    original = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
    compressed = cv2.imread(compressed_image_path, cv2.IMREAD_GRAYSCALE)

    # 이미지가 제대로 로드되었는지 확인
    if original is None:
        raise ValueError(f"이미지를 열거나 찾을 수 없습니다: {original_image_path}")
    if compressed is None:
        raise ValueError(f"이미지를 열거나 찾을 수 없습니다: {compressed_image_path}")

    # 이미지의 차원이 같은지 확인
    if original.shape != compressed.shape:
        raise ValueError("원본 이미지와 압축 이미지의 차원이 동일해야 합니다.")

    # PSNR 계산
    psnr_value = psnr(original, compressed)

    return psnr_value

# 예제 사용법
if __name__ == "__main__":
    # 간단한 UI 생성
    root = tk.Tk()
    root.withdraw()  # 루트 창 숨기기

    # 원본 이미지 선택
    print("원본 이미지 파일을 선택하세요.")
    original_image_path = filedialog.askopenfilename()

    # 파일이 선택되었는지 확인
    if not original_image_path:
        print("원본 이미지 파일이 선택되지 않았습니다.")
        exit()

    # 압축 이미지 선택
    print("압축 이미지 파일을 선택하세요.")
    compressed_image_path = filedialog.askopenfilename()

    # 파일이 선택되었는지 확인
    if not compressed_image_path:
        print("압축 이미지 파일이 선택되지 않았습니다.")
        exit()

    # PSNR 값 계산 및 출력
    try:
        psnr_value = calculate_psnr(original_image_path, compressed_image_path)
        print(f'PSNR 값: {psnr_value:.6f} dB')
    except ValueError as e:
        print(e)
